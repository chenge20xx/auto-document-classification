# auto-document-classification

## 主要功能：

支持多种文件格式：txt, pdf, docx, xlsx/xls
通过API进行文档分类
通过API生成中文文件名
自动创建分类文件夹并移动文件
使用方法：

将需要处理的文档放入documents文件夹
运行脚本时会提示输入API Key
输入要处理的文件夹路径
程序会自动处理所有文档
注意：

需要替换API URL为实际地址
需要根据实际API响应调整classify_document和generate_filename方法
确保已安装所有依赖库
处理大量文件时可能需要考虑API调用频率限制
