
接口文档
=================
##接口响应通过格式
```
export interface HttpResponse {
    status: number;
    statusText: string;
    data: {
      code: number;
      desc: string;
      [key: string]: any;
    };
}

export class Template {
  category = '';
  name = '';
  rows: Array<TemplateRow> = [];

  constructor(rows: Array<TemplateRow>) {
    this.rows = rows;
  }
}

export class TemplateRow {
  field1 = '';
  position1 = 1;
  field2 = '';
  position2 = 1;
  field3 = '';
  position3 = 1;
  field4 = '';
  position4 = 1;
  field5 = '';
  field6 = '';
  type = 1;
}

export class AIResult {
  level1 = '';
  level2 = '';
  value = '';
  accuracy = 0;
  img = '';
}
```
## Api
>1.确定模板：
>>入参：Template

>2.导出模板
>>出参: 文件路径

>3.上传文件
>>入参：文件列表，也可以单个文件循环上传, 类型：模板/文件 

>4.模板列表
>>出参: [Template]

>5.全部识别
>>入参：template name

>6.刷新
>>出参 [AIResult]

>7.导出文件
>>入参: [AIResult]
>>出参: 文件路径

>8.当前模板
>>出参: Template