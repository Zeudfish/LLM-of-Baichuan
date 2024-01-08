'''
File        : app.py
Description : baichuan api接口
Date        : 2023/12/19
Author      : Feiyu Zhu
'''


from flask import Flask, request, jsonify
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import GenerationConfig

# 初始化 Flask 应用
app = Flask(__name__)

# 加载模型和分词器
tokenizer = AutoTokenizer.from_pretrained("baichuan-inc/Baichuan2-7B-Chat", use_fast=False, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("baichuan-inc/Baichuan2-7B-Chat", device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True)
model.generation_config = GenerationConfig.from_pretrained("baichuan-inc/Baichuan2-7B-Chat")

# 定义 API 端点
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    user_input = data.get("input")
    print(user_input)

    messages = [{"role": "user", "content": user_input}]
    response = model.chat(tokenizer, messages)
    
    return jsonify({"response": response})

# 运行 Flask 应用
if __name__ == '__main__':
     app.run(debug=True,host='0.0.0.0',port=8889)
    # app.run(debug=True)
