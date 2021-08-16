import os
import sys
import subprocess

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, '')))

os.environ["FLAGS_allocator_strategy"] = 'auto_growth'

import cv2
import copy
import numpy as np
import time
from PIL import Image
import tools.infer.predict_rec as predict_rec
import tools.infer.predict_det as predict_det
import tools.infer.predict_cls as predict_cls
from ppocr.utils.utility import get_image_file_list, check_and_read_gif
from ppocr.utils.logging import get_logger
from tools.infer.utility import draw_ocr_box_txt

logger = get_logger()


class TextSystem(object):
    def __init__(self, args):
        self.text_detector = predict_det.TextDetector(args)
        self.text_recognizer = predict_rec.TextRecognizer(args)
        self.use_angle_cls = args.use_angle_cls
        self.drop_score = args.drop_score
        if self.use_angle_cls:
            self.text_classifier = predict_cls.TextClassifier(args)

    def get_rotate_crop_image(self, img, points):
        '''
        img_height, img_width = img.shape[0:2]
        left = int(np.min(points[:, 0]))
        right = int(np.max(points[:, 0]))
        top = int(np.min(points[:, 1]))
        bottom = int(np.max(points[:, 1]))
        img_crop = img[top:bottom, left:right, :].copy()
        points[:, 0] = points[:, 0] - left
        points[:, 1] = points[:, 1] - top
        '''
        img_crop_width = int(
            max(
                np.linalg.norm(points[0] - points[1]),
                np.linalg.norm(points[2] - points[3])))
        img_crop_height = int(
            max(
                np.linalg.norm(points[0] - points[3]),
                np.linalg.norm(points[1] - points[2])))
        pts_std = np.float32([[0, 0], [img_crop_width, 0],
                              [img_crop_width, img_crop_height],
                              [0, img_crop_height]])
        M = cv2.getPerspectiveTransform(points, pts_std)
        dst_img = cv2.warpPerspective(
            img,
            M, (img_crop_width, img_crop_height),
            borderMode=cv2.BORDER_REPLICATE,
            flags=cv2.INTER_CUBIC)
        dst_img_height, dst_img_width = dst_img.shape[0:2]
        if dst_img_height * 1.0 / dst_img_width >= 1.5:
            dst_img = np.rot90(dst_img)
        return dst_img

    def print_draw_crop_rec_res(self, img_crop_list, rec_res):
        bbox_num = len(img_crop_list)
        for bno in range(bbox_num):
            cv2.imwrite("./output/img_crop_%d.jpg" % bno, img_crop_list[bno])
            logger.info(bno, rec_res[bno])

    def __call__(self, img):
        ori_im = img.copy()
        dt_boxes, elapse = self.text_detector(img)
        logger.info("dt_boxes num : {}, elapse : {}".format(
            len(dt_boxes), elapse))
        if dt_boxes is None:
            return None, None
        img_crop_list = []

        dt_boxes = sorted_boxes(dt_boxes)

        for bno in range(len(dt_boxes)):
            tmp_box = copy.deepcopy(dt_boxes[bno])
            img_crop = self.get_rotate_crop_image(ori_im, tmp_box)
            img_crop_list.append(img_crop)
        if self.use_angle_cls:
            img_crop_list, angle_list, elapse = self.text_classifier(
                img_crop_list)
            logger.info("cls num  : {}, elapse : {}".format(
                len(img_crop_list), elapse))

        rec_res, elapse = self.text_recognizer(img_crop_list)
        logger.info("rec_res num  : {}, elapse : {}".format(
            len(rec_res), elapse))
        # self.print_draw_crop_rec_res(img_crop_list, rec_res)
        filter_boxes, filter_rec_res = [], []
        for box, rec_reuslt in zip(dt_boxes, rec_res):
            text, score = rec_reuslt
            if score >= self.drop_score:
                filter_boxes.append(box)
                filter_rec_res.append(rec_reuslt)
        return filter_boxes, filter_rec_res


def sorted_boxes(dt_boxes):
    """
    Sort text boxes in order from top to bottom, left to right
    args:
        dt_boxes(array):detected text boxes with shape [4, 2]
    return:
        sorted boxes(array) with shape [4, 2]
    """
    num_boxes = dt_boxes.shape[0]
    sorted_boxes = sorted(dt_boxes, key=lambda x: (x[0][1], x[0][0]))
    _boxes = list(sorted_boxes)

    for i in range(num_boxes - 1):
        if abs(_boxes[i + 1][0][1] - _boxes[i][0][1]) < 10 and \
                (_boxes[i + 1][0][0] < _boxes[i][0][0]):
            tmp = _boxes[i]
            _boxes[i] = _boxes[i + 1]
            _boxes[i + 1] = tmp
    return _boxes

def get_row_boxes(stop_words, dt_boxes, rec_res):
    row_tmp_boxes = []
    row_boxes = []
    rows_res = []
    for box, res in zip(dt_boxes, rec_res):

        stop = 0
        for words in stop_words:
            if len(set(words)) - len(set(words) & set(res[0])) <= 1:
                stop = 1
                break
        if stop == 1:
            continue

        if len(row_tmp_boxes) == 0:
            row_tmp_boxes.append(box)

            rows_res.append([res])
            row_boxes.append([box])
            continue
        else:
            _last = row_tmp_boxes[-1]

        _max = _last[:,1].max()
        _min = _last[:,1].min()


        pos_max = box[:,1].max()
        pos_min = box[:,1].min()

        for n, pos in enumerate(box[:, -1]):
            if _min <= pos and pos <= _max:
                rows_res[-1].append(res)
                row_boxes[-1].append(box)
                break
            elif pos_min <= _max and _max <= pos_max:
                rows_res[-1].append(res)
                row_boxes[-1].append(box)
                break
            if n == 3:
                row_boxes.append([box])
                rows_res.append([res])
        row_tmp_boxes.append(box)
    return rows_res, row_boxes


def get_col_boxes(rows_res, row_boxes):
    col_recs = []
    col_boxes = []
    for res, box in zip(rows_res, row_boxes):

        lefts = []
        for d in box:
            left = d[0, 0]
            lefts.append(left)

        _ = zip(res, lefts, box)

        _ = sorted(_, key=lambda x: x[1])

        col_res = []
        col_box = []
        for r, left, box in _:
            col_res.append(r)
            col_box.append(box)
        col_recs.append(col_res)
        col_boxes.append(col_box)
    return col_recs, col_boxes


def review_img(col_boxes, img):
    out_imgs = []
    for box in col_boxes:
        tmp = np.vstack(box)
        h_max = tmp[:, 1].max()
        h_min = tmp[:, 1].min()
        w_max = tmp[:, 0].max()
        w_min = tmp[:, 0].min()
        # tmp_box = np.array([[w_min, h_min], [w_max, h_min], [w_max, h_max], [w_min, h_max]])
        new_img = img[int(h_min): int(h_max), int(w_min): int(w_max)]
        out_imgs.append(new_img)
    return out_imgs


def reg(args):
    args.det_model_dir = "inference/det/"
    args.rec_model_dir = "inference/rec/"
    args.cls_model_dir = "inference/cls/"
    args.use_angle_cls = True
    args.use_space_char = True
    args.drop_score = 0
    args.use_angle_cls = True
    args.use_space_char = True
    args.drop_score = 0

    image_file_list = get_image_file_list(args.image_dir)
    text_sys = TextSystem(args)
    is_visualize = True
    font_path = args.vis_font_path
    drop_score = args.drop_score
    data = []
    for image_file in image_file_list:
        img, flag = check_and_read_gif(image_file)
        if not flag:
            img = cv2.imread(image_file)
        if img is None:
            logger.info("error in loading image:{}".format(image_file))
            continue
        starttime = time.time()
        dt_boxes, rec_res = text_sys(img)
        elapse = time.time() - starttime
        logger.info("Predict time of %s: %.3fs" % (image_file, elapse))

        for text, score in rec_res:
            logger.info("{}, {:.3f}".format(text, score))

        if is_visualize:
            image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            boxes = dt_boxes
            txts = [rec_res[i][0] for i in range(len(rec_res))]
            scores = [rec_res[i][1] for i in range(len(rec_res))]

            draw_img = draw_ocr_box_txt(
                image,
                boxes,
                txts,
                scores,
                drop_score=drop_score,
                font_path=font_path)
            draw_img_save = "./inference_results/"
            if not os.path.exists(draw_img_save):
                os.makedirs(draw_img_save)
            cv2.imwrite(
                os.path.join(draw_img_save, os.path.basename(image_file)),
                draw_img[:, :, ::-1])
            logger.info("The visualized image saved in {}".format(
                os.path.join(draw_img_save, os.path.basename(image_file))))

        stop_words = ['脏器功能']

        rows_res, row_boxes = get_row_boxes(stop_words, dt_boxes, rec_res)
        col_recs, col_boxes = get_col_boxes(rows_res, row_boxes)
        single = (image_file, col_recs, review_img(col_boxes, img))
        data.append(single)
    return data


