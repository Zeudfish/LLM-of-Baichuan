'''
File        : CheckSim.py
Description : 检测相似问
Date        : 2023/12/22
Author      : Feiyu Zhu
'''

import requests
import json
import pandas as pd
import re
import ast 
# API 的 URL

def extract_individual_questions(text):

    # Regular expression to find the text within the outermost square brackets
    outer_brackets_pattern = r'\[(.*)\]'
    # Extract the text within the outermost square brackets
    outer_text = re.search(outer_brackets_pattern, text).group(1)

    # Split the extracted text by ', ' to get individual questions
    individual_questions = outer_text.split("', '")
    
    # Strip quotes from the first and last elements
    if individual_questions:
        individual_questions[0] = individual_questions[0].lstrip("'")
        individual_questions[-1] = individual_questions[-1].rstrip("'")

    return individual_questions
url = "http://127.0.0.1:5000/generate"

excel_file = "/home/zhengm/testcode/zhufeiyu/baichuan/Baichuan2/dataset_example.xlsx"
df=pd.read_excel(excel_file)
for index,row in df.iterrows():
    exceldata=row['Standard_Question']
    checkdata=row['Similar_Question']
    try:
        checkdata_list = ast.literal_eval(checkdata)
    except ValueError:
        # 如果转换失败，跳过此行或做其他处理
        continue

    checklist=checkdata_list

    updated_checkdata_list = []

    for i in checkdata_list:


    
        excel_question=f"你将要扮演一个相似问专家\r\n你需要判断两个问题是否是相似问,即这两个问题的语义是否相同。\r\n按照我给你的例子回答问题返回结果\r\n 例子：\r\n<\r\n问题1:\r\n 问题2:是\r\n 返回：“结论：是/不是相似问 \r\n>\r\n  问题:\r\n<\r\n问题1:{exceldata}\r\n 问题2:{i}\r\n“>"

        data = {"input": excel_question}

        # 发送请求
        session = requests.Session()
        response = session.post(url, json=data, headers={"Content-Type": "application/json", "Cache-Control": "no-cache"})

        # 检查响应状态码
        if response.status_code == 200:
            # 解析响应内容
            result = response.json()
            response_string = result['response'].strip().lower()
            print(response_string)
            if response_string in ["结论：不是相似问"]:

                updated_checkdata_list.append(i)
            else:
                continue
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        else:
            print("请求失败，状态码:", response.status_code)
    df.at[index, "Similar_Question"] = str(updated_checkdata_list)
df.to_excel('/home/zhengm/testcode/zhufeiyu/baichuan/Baichuan2/dataset_examplem.xlsx',index=False)