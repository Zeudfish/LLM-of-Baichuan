'''
File        : Similar_Question.py
Description : 生成相似问
Date        : 2023/12/19 15:48:59
Author      : Feiyu Zhu
'''

import requests
import json
import pandas as pd
import re
# API 的 URL

def extract_questions_general(text):

    lines = text.split('\n')
    questions = []
    for line in lines:
        match = re.search(r'\d+\.\s(.+)', line)
        if match:
            questions.append(match.group(1))

    return questions
url = "http://127.0.0.1:5000/generate"

excel_file = "/zhufeiyu/baichuan/Baichuan2/simary.xlsx"
df=pd.read_excel(excel_file)
for index,row in df.iterrows():
    exceldata=row['Standard_Question']




# 要发送的数据
    excel_question = f""
    # 构建嵌套的 JSON 数据

    data = {"input": excel_question}
   # 发送请求
    session = requests.Session()
    response = session.post(url, json=data, headers={"Content-Type": "application/json", "Cache-Control": "no-cache"})

    # 检查响应状态码
    if response.status_code == 200:
        # 解析响应内容
        result = response.json()
        response_string = result['response']
        print(response_string)
        try:
            questions = extract_questions_general(response_string)
        

        except:
            questions = extract_questions_general(response_string)


        print(questions)   
        df.at[index, "Similar_Question"] = str(questions)
      
    else:
        print("请求失败，状态码:", response.status_code)
df.to_excel('/home/zhengm/testcode/zhufeiyu/baichuan/Baichuan2/simarychange.xlsx',index=False)