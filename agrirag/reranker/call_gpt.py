# 输入message队列，返回输出text
import requests
import base64

def call_gpt(message_list):
    api_key = "sk-JYxUur2qWtLjVR6FI8EaVyKCD4MGfJHlk8gNfURwo4B5JLl5"
    gpt_url = "https://api.chatanywhere.tech/v1/chat/completions"
    headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"}

    data = {
            "model": "gpt-4o",
            "messages": message_list,
            "max_tokens": 200,
            "temperature": 0.5}

    response = requests.post(gpt_url, headers=headers, json=data)

    if response.status_code == 200:
        response_json = response.json()
        return response_json['choices'][0]['message']['content']
    else:
        print(f"Error: {response.status_code}, {response.text}")