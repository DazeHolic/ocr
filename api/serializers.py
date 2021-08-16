from flask_restplus import Model
from werkzeug.datastructures import FileStorage
from flask_restplus import fields

save_template_request_vm_data = Model("save_template_request_vm_data", {
    "name1": fields.String(),
    "name2": fields.String(),
    "field1": fields.String(),
    "position1": fields.Integer(),
    "field2": fields.String(),
    "position2": fields.Integer(),
    "field3": fields.String(),
    "position3": fields.Integer(),
    "field4": fields.String(),
    "position4": fields.Integer(),
    "field5": fields.String(),
    "field6": fields.String(),
    "type": fields.Integer(),
})

save_template_request_vm = Model("save_template_request_vm", {
    "template": fields.List(fields.Nested(save_template_request_vm_data), description="import template"),
})


save_template_response_vm = Model("save_template_response_vm", {
    "status": fields.String(required=True, description="import template status")
})

export_request_vm = Model("export_request_vm", {
    "export": fields.Integer(description="1 is one 2 is all")
})

export_response_vm = Model("export_response_vm", {
    "filepath": fields.String(required=True, description="filepath")
})

tables_request_vm = Model("tables_request_vm", {
    "type": fields.Integer(description="1 is one 2 is all")
})

tables_response_vm = Model("tables_response_vm", {
    "tables": fields.List(fields.List(fields.String()), required=True, description="tables")
})

reg_request_vm = Model("reg_request_vm", {
    "name1": fields.String(description="一级类"),
    "name2": fields.String(description="二级类")
})

reg_response_vm_data = Model("reg_response_vm_data", {
    "class1": fields.String(),
    "class2": fields.String(),
    "result": fields.String(),
    'prob': fields.String(),
    "img_path": fields.String(),
})

reg_response_vm_single = Model("reg_response_vm_single", {
    "data": fields.List(fields.Nested(reg_response_vm_data), description="export template"),
    "name": fields.String(),
})

reg_response_vm = Model("reg_response_vm", {
    "result": fields.List(fields.Nested(reg_response_vm_single), description="export data"),
})

flush_request_vm = Model("flush_request_vm", {
    "type": fields.Integer(description="刷新"),
})


flush_response_vm_data = Model("flush_response_vm_data", {
    "field5": fields.String(),
    "field6": fields.String(),
    "result": fields.String(),
    "img_path": fields.String(),
})

flush_response_vm = Model("flush_response_vm", {
    "template": fields.List(fields.Nested(save_template_request_vm_data), description="export template"),
})

download_request_vm_data = Model("download_request_vm_data", {
    "field5": fields.String(),
    "field6": fields.String(),
    "result": fields.String(),
})

download_request_vm = Model("download_request_vm", {
    "template": fields.List(fields.Nested(download_request_vm_data), description="export template"),
})

download_response_vm = Model("download_response_vm", {
    "file_path": fields.String(description="下载文件路径"),
})


index_request_vm = Model("index_request_vm", {
    "type": fields.Integer(description="首页"),
})

index_response_vm_data = Model("index_response_vm_data", {
    "name1": fields.String(),
    "name2": fields.String(),
    "field1": fields.String(),
    "position1": fields.Integer(),
    "field2": fields.String(),
    "position2": fields.Integer(),
    "field3": fields.String(),
    "position3": fields.Integer(),
    "field4": fields.String(),
    "position4": fields.Integer(),
    "field5": fields.String(),
    "field6": fields.String(),
    "type": fields.Integer(),
})

index_response_vm = Model("index_response_vm", {
    "template": fields.List(fields.Nested(index_response_vm_data), description="index template"),
})



output_request_vm = Model("download_request_vm", {
    "template": fields.List(fields.Nested(download_request_vm_data), description="export template"),
})

ouput_response_vm = Model("download_response_vm", {
    "file_path": fields.String(description="下载文件路径"),
})
