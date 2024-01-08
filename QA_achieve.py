from docx import Document
import requests
import json
import pandas as pd
import re
def clean_text(text):
    return text.strip().replace('\n', ' ')

#切分文档，当前为按照word标题切分
def split_document_by_headings(doc_path):
    doc = Document(doc_path)
    sections = []
    current_section = []

    for paragraph in doc.paragraphs:
        if paragraph.style.name.startswith('Heading'):
            if current_section:
                sections.append("\n".join(current_section))
                current_section = []
            print(paragraph.text)
             
            current_section.append(clean_text(paragraph.text))
        else:

            current_section.append(clean_text(paragraph.text))
        

    # Add the last section
    if current_section:
        sections.append("".join(current_section))

    return sections

url = "http://127.0.0.1:5000/generate"

sections = split_document_by_headings("zhufeiyu/baichuan/Baichuan2/test.docx")
# 调用函数并打印文档内容


excel_question = f""

data = {"input": excel_question}
# print("请求数据:", data)
# 发送请求
session = requests.Session()
response = session.post(url, json=data, headers={"Content-Type": "application/json", "Cache-Control": "no-cache"})

# 检查响应状态码
if response.status_code == 200:
    # 解析响应内容
    result = response.json()
    response_string = result['response']
    print(response_string)