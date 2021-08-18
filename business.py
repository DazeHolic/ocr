import sqlite3
import time

import pandas as pd
import os
from predict import reg
import cv2
from copy import deepcopy
import json
import tools.infer.utility as utility
from config import template
import pymysql.cursors


class OCR:

    def __init__(self):
        self.con = sqlite3.connect(".\db.sqlite", check_same_thread=False)
        self.base_dir = "./"
        self.img_dir = "./imgs"
        self.output_dir = "./output"
        self.url_path = "/output"
        self.connection = pymysql.connect(
                            host='localhost',
                            user='root',
                            password='root',
                            database='ocr',
                            cursorclass=pymysql.cursors.DictCursor)

    def _save_template(self, template):
        df = pd.DataFrame(template)
        name1 = template[0]['name1']
        name2 = template[0]['name2']
        cur = self.con.cursor()
        sql = "delete from o_template where name1='%s' and name2='%s'" % (name1, name2)
        cur.execute(sql)
        self.con.commit()
        cur.close()

        df.to_sql("o_template", self.con, if_exists="append", index=False)
        return 1

    def _export(self):
        cur = self.con.cursor()
        tables = cur.execute("select * from o_template")
        df = pd.DataFrame(tables, columns=["name1", "name2", "field1", "position1", "field2", "position2",
                                           "field3", "position3", "field4", "position4", "field5", "field6", "type"])

        names = df.iloc[-1:, :2].values[0].tolist()

        export_path = "\\".join(names)

        dir_path = os.path.join(self.base_dir, names[0])

        save_file = os.path.join(self.base_dir, export_path)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        save_file = save_file + ".csv"
        df[(df["name1"] == names[0]) & (df["name2"] == names[1])].to_csv(save_file, index=False, encoding='utf8')
        cur.close()
        print(save_file)
        return save_file

    def _export_all(self):

        cur = self.con.cursor()
        tables = cur.execute("select * from o_template")
        df = pd.DataFrame(tables, columns=["name1", "name2", "field1", "position1", "field2", "position2",
                                           "field3", "position3", "field4", "position4", "field5", "field6", "type"])

        files = []
        for path in df.path.unique():
            save_path = "/".join(path.split())
            dir_path = os.path.join(self.base_dir, path.split()[0])

            save_file = os.path.join(self.base_dir, save_path)
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)

            df[df["path"] == path].to_csv(save_file + ".csv", index=False)
            files.append(save_file)

        cur.close()
        return files

    def _import_template(self, stream):
        # filename=stream.filename
        csv_line = [line.decode().replace('\n', '') for line in stream]
        data = list(map(lambda x: str(x).split(","), csv_line[1:]))
        frame = pd.DataFrame(data, columns=csv_line[0][:-1].split(","))
        frame.to_sql("template", self.con, if_exists="append", index=False)
        return 'success'

    def _import_imgs(self, stream, tm):
        cur = self.con.cursor()
        cur.execute("update cache set status = 0 where time <> %d" % tm)
        cur.execute("""insert into cache (time, status, name) VALUES (%d, %d, '%s')""" %
                    (tm, 1, stream.filename))
        self.con.commit()

        cur.close()

        save_dir = os.path.join(self.img_dir, str(tm))
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

        stream.save(os.path.join(save_dir, stream.filename))
        return 'success'

    def _tables(self):
        cur = self.con.cursor()
        tables = cur.execute("select name1, name2 from template")
        df = pd.DataFrame(tables, columns=["name1", "name2"])
        cur.close()
        df['route'] = df['name1'] + '_' + df['name2']
        routes = df['route'].unique().tolist()

        return [route.split('_') for route in routes]

    def _reg(self, name1, name2):
        cur = self.con.cursor()
        tables = cur.execute("select time, name from cache where status = 1")
        target_set = []
        tm = 0
        for table in tables:
            tm = table[0]
            target_set.append((table[0], table[1]))
        cur.close()
        target_set = set(target_set)
        img_paths = []
        names = []
        for tm, name in target_set:
            path = os.path.join(self.img_dir, str(tm))
            path = os.path.join(path, name)
            img_paths.append(path)
            names.append(name)

        data = {}
        for path, name in zip(img_paths, names):
            det = os.path.join(self.base_dir, "inference/det/")
            rec = os.path.join(self.base_dir, "inference/rec/")
            cls = os.path.join(self.base_dir, "inference/cls/")
            recs, boxes = reg(args, det, rec, cls)
            data[name] = zip(recs, boxes)

        cur = self.con.cursor()
        tables = cur.execute("select * from template where name1='%s' and name2='%s'" % (name1, name2))
        templates = []
        for table in tables:
            tmp = {
                'in': [],
                'out': []
            }
            field1, position1 = table[2], table[3]
            if position1 > 0:
                tmp['in'].append((field1, position1))
            field2, position2 = table[4], table[5]
            if position2 > 0:
                tmp['in'].append((field2, position2))
            field3, position3 = table[6], table[7]
            if position3 > 0:
                tmp['in'].append((field3, position3))
            field4, position4 = table[8], table[9]
            if position4 > 0:
                tmp['in'].append((field4, position4))
            field5, field6, typ = table[10], table[11], table[12]
            tmp['out'] = [field5, field6, typ]
            templates.append(tmp)
        cur.close()

        x = 0
        output = []
        l = 0
        for name, regs in data.items():
            print(name)
            labels = []
            output.append({
                'name': name,
                'data': []
            })
            for recs, boxes in regs:
                for n, rec in enumerate(recs):
                    for y in templates:
                        for _ in y['in']:
                            d = self.distance(set(_[0]), set(rec[0]))
                            if d >= 0.7:
                                m = n + _[1]
                                r = recs[m][0]
                                label = deepcopy(y['out'])
                                label[2] = r
                                label.append(rec[1])
                                path = self.save(str(tm), str(x), boxes)
                                label.append(path)
                                labels.append(label)
                                x += 1

            df = pd.DataFrame(labels, columns=["class1", "class2", "result", "prob", "img_path"])
            df['prob'] = df['prob'].apply(str)
            data = df.to_json(orient='records')
            output[l]['data'] = json.loads(data)
            l += 1

        return output

    def get_result(self, args):
        occ = reg(args)
        data = dict()
        for d in occ:
            name, recs, boxes = d
            name = os.path.basename(name)
            data[name] = zip(recs, boxes)

            tid = name.split('_')[1]
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM tbl_template WHERE `template_id`= '%s'" % tid
                cursor.execute(sql)
                result = cursor.fetchall()

                templates = []
                for table in result:
                    tmp = {
                        'in': [],
                        'out': []
                    }
                    field1, position1 = table.get('field1'), table.get('position1')
                    if position1 > 0:
                        tmp['in'].append((field1, position1))
                    field2, position2 = table.get('field2'), table.get('position2')
                    if position2 > 0:
                        tmp['in'].append((field2, position2))
                    field3, position3 = table.get('field3'), table.get('position3')
                    if position3 > 0:
                        tmp['in'].append((field3, position3))
                    field4, position4 = table.get('field4'), table.get('position4')
                    if position4 > 0:
                        tmp['in'].append((field4, position4))
                    field5, field6, typ = table.get('field5'), table.get('field6'), table.get('type')
                    tmp['out'] = [field5, field6, typ]
                    templates.append(tmp)


        x = 0
        output = []
        l = 0
        tm = str(time.time()).split('.')[0]

        for name, regs in data.items():
            print(name)
            labels = []
            output.append({
                'name': name,
                'data': []
            })
            for recs, boxes in regs:
                for n, rec in enumerate(recs):
                    for y in templates:
                        for _ in y['in']:
                            d = self.distance(set(_[0]), set(rec[0]))
                            if d >= 0.7:
                                m = n + _[1]
                                r = recs[m][0]
                                label = deepcopy(y['out'])
                                label[2] = r
                                label.append(rec[1])
                                path = self.save(tm, str(x), boxes)
                                label.append(path)
                                labels.append(label)
                                x += 1

            df = pd.DataFrame(labels, columns=["class1", "class2", "result", "prob", "img_path"])
            df['prob'] = df['prob'].apply(str)
            data = df.to_json(orient='records')
            output[l]['data'] = json.loads(data)
            l += 1

        return output


    def save_to_db(self, output):
        with self.connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `tb_ocr_record_log` (`ocr_log_id`,`resident_id`,`parameter_id`,`parameter`,`picture`,`accuracy`,`Identification_time`, `is_delete`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            for data in output:
                name = data['name']
                attrs = name.split('_')
                for one in data['data']:
                    cursor.execute(sql, (attrs[2], attrs[0], one['class2'], one['result'], one['img_path'], one['prob'], self._timestamp(), '0'))
            self.connection.commit()

    def save(self, tm, img_name, img):
        draw_img_save = os.path.join(self.output_dir, tm)
        url_path = os.path.join(self.url_path, tm)
        if not os.path.exists(draw_img_save):
            os.makedirs(draw_img_save)
        path = os.path.join(draw_img_save, 'check_' + img_name + '.PNG')
        url_path = os.path.join(url_path, 'check_' + img_name + '.PNG')

        cv2.imwrite(path, img)
        print('save successful', path)
        print('save successful', url_path)

        return url_path

    def distance(self, a, b):
        return len(a & b) / len(a | b)

    def _flush(self):
        template = [
            {
                "field5": "报告",
                "field6": "白细胞计数",
                "result": "1",
                "img_path": os.path.join(self.base_dir, 'img_crop_0.jpg')
            },
            {
                "field5": "报告",
                "field6": "白细胞计数",
                "result": "2",
                "img_path": os.path.join(self.base_dir, 'img_crop_0.jpg')
            }
        ]
        return template

    def _download(self, template):
        df = pd.DataFrame(template)
        print(df.head())
        path = os.path.join(self.base_dir, 'excel/tmp.xlsx')
        df.to_excel(path)

        return path

    def _index_result(self):
        # 当前结果
        cur = self.con.cursor()

        tables = cur.execute("select img_name, name1, name2 from result where rowid = (select max(rowid) from result);")
        img_name, name1, name2 = None, None, None
        for table in tables:
            img_name, name1, name2 = table

        r = None
        if img_name is not None:
            sql = "select img_name, name1, name2, field5, field6, result from result where img_name='%s' and name1='%s' and name2='%s'" % (
                img_name, name1, name2)
            tables = cur.execute(sql)
            df = pd.DataFrame(tables, columns=['img_name', 'name1', 'name2', 'field5', 'field6', 'result'])
            r = df.to_json(orient="records")
        cur.close()

        return r

    def _index(self):
        # 当前模板
        cur = self.con.cursor()

        tables = cur.execute("select name1, name2 from o_template where rowid = (select max(rowid) from o_template);")
        name1, name2 = None, None
        for table in tables:
            name1, name2 = table

        r = None
        if name1 and name2 is not None:
            sql = "select name1, name2, field1, position1, field2, position2, field3, position3, field4, position4, field5, field6, type from template where name1='%s' and name2='%s'" % (
                name1, name2)
            tables = cur.execute(sql)
            df = pd.DataFrame(tables, columns=["name1", "name2", "field1", "position1", "field2", "position2",
                                               "field3", "position3", "field4", "position4", "field5", "field6",
                                               "type"])
            r = df.to_json(orient="records")
        cur.close()

        return r

    def _timestamp(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


if __name__ == "__main__":
    ocr = OCR()
    args = utility.parse_args()
    output = ocr.get_result(args)
    ocr.save_to_db(output)