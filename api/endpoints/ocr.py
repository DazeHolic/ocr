import sys
from flask_restplus import Namespace, Resource, Model, fields, reqparse
from api.serializers import (export_request_vm, export_response_vm, save_template_request_vm, save_template_response_vm,
                              tables_request_vm, tables_response_vm, reg_request_vm, reg_response_vm,
                             flush_request_vm, flush_response_vm, download_request_vm, download_response_vm,
                             index_request_vm, index_response_vm)
from api import ocr
from werkzeug.datastructures import FileStorage
import json
import os
from flask import send_from_directory

ns = Namespace('ocr', description='ocr', path='/')


def add_models(module_name: str, ns):
    references = sys.modules[module_name].__dict__
    for key in list(references):
        value = references.get(key)
        if isinstance(value, Model):
            _add_model(value, ns)


def _add_model(vm, ns):
    for key in vm:
        if isinstance(vm[key], fields.Nested):
            _add_model(vm[key].model, ns)
        elif isinstance(vm[key], fields.List):
            container = vm[key].container
            if isinstance(container, fields.Nested):
                _add_model(container.model, ns)
    if ns.models.get(vm.name) is None:
        ns.add_model(vm.name, vm)


add_models(__name__, ns)


# 确定模板
@ns.route('/save')
class Save(Resource):
    @ns.expect(save_template_request_vm)
    @ns.marshal_with(save_template_response_vm)
    @ns.doc(description="Please provide the input save parameter ocr")
    def post(self):
        try:
            payload = ns.payload
            template = payload["template"]
            result = ocr._save_template(template)
            if result:
                result = 'success'
            return {"status": result}, 200

        except Exception as exc:
            return {"status": "server error"}, 500

# 导出模板
@ns.route('/export')
class Export(Resource):
    @ns.expect(export_request_vm)
    @ns.marshal_with(export_response_vm)
    @ns.doc(description="Please provide the export parameter ocr")
    def post(self):
        try:
            payload = ns.payload
            export = payload.get("export")
            result = ocr._export()

            return {"filepath": result}, 200
        except Exception as exc:
            return {"filepath": "server error"}, 500


# 上传文件
upload_parser = ns.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)
parser = reqparse.RequestParser()
parser.add_argument('type', required=True)
parser.add_argument('time', required=True)

@ns.route('/upload')
@ns.expect(upload_parser)
class upload(Resource):
    @ns.expect(parser)
    @ns.doc(description="Please provide the export parameter ocr")
    def post(self):
        try:
            """
            extract the content
            """
            args = parser.parse_args()
            typ = args['type']
            tm = args['time']

            args = upload_parser.parse_args()
            uploaded_file = args['file']

            if typ == '1':
                status = ocr._import_template(uploaded_file)
            elif typ == '2':
                status = ocr._import_imgs(uploaded_file, int(tm))
            else:
                status = 'error type'
            return {"status": status}, 200

        except Exception as exc:
            return {"status": "server error"}, 500

# 模板列表
@ns.route('/tables')
class tables(Resource):
    @ns.expect(tables_request_vm)
    @ns.marshal_with(tables_response_vm)
    @ns.doc(description="Please provide the tables parameter ocr")
    def post(self):
        try:
            payload = ns.payload
            export = payload["type"]
            result = ocr._tables()
            return {"tables": result}, 200
        except Exception as exc:
            return {"tables": "server error"}, 500

# 全部识别
@ns.route('/reg')
class Reg(Resource):
    @ns.expect(reg_request_vm)
    @ns.marshal_with(reg_response_vm)
    @ns.doc(description="Please provide the reg parameter ocr")
    def post(self):
        try:
            payload = ns.payload
            name1 = payload["name1"]
            name2 = payload["name2"]
            result = ocr._reg(name1, name2)
            return {"result": result}, 200
        except Exception as exc:
            return {"result": "server error"}, 500

# 刷新
# 出参 [AIResult]
@ns.route('/flush')
class Flush(Resource):
    @ns.expect(flush_request_vm)
    @ns.marshal_with(flush_response_vm)
    @ns.doc(description="Please provide the flush parameter ocr")
    def post(self):
        try:
            payload = ns.payload
            typ = payload["type"]
            result = ocr._flush()
            return {"template": result}, 200
        except Exception as exc:
            return {"template": "server error"}, 500

# 导出文件
@ns.route('/download')
class Download(Resource):
    @ns.expect(download_request_vm)
    @ns.marshal_with(download_response_vm)
    @ns.doc(description="Please provide the flush parameter ocr")
    def post(self):
        try:
            payload = ns.payload
            template = payload["template"]
            result = ocr._download(template)
            return {"file_path": result}, 200
        except Exception as exc:
            return {"file_path": "server error"}, 500

# 当前模板
@ns.route('/index')
class Index(Resource):
    @ns.expect(index_request_vm)
    @ns.marshal_with(index_response_vm)
    @ns.doc(description="Please provide the index parameter ocr")
    def post(self):
        try:
            payload = ns.payload
            typ = payload["type"]
            result = ocr._index()
            print('result', result)
            return {"template": json.loads(result)}, 200
        except Exception as exc:
            return {"template": "server error"}, 500

@ns.route('/downloadfile')
class Downloadfile(Resource):
    def post(self):
        try:
            payload = ns.payload
            filepath,tempfilename = os.path.split(payload["filepath"])
            return send_from_directory(filepath, tempfilename, as_attachment=True)
        except Exception as exc:
            print(exc)
            return{"filepath":"servererror"}, 500

    # 到处结果
# @ns.route('/ouput')
# class Output(Resource):
#     @ns.expect(ouput_request_vm)
#     @ns.marshal_with(ouput_response_vm)
#     @ns.doc(description="Please provide the index parameter ocr")
#     def post(self):
#         try:
#             payload = ns.payload
#             typ = payload["type"]
#             result = ocr._index()
#             print('result', result)
#             return {"template": json.loads(result)}, 200
#         except Exception as exc:
#             return {"template": "server error"}, 500
