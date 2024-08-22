import requests
import base64

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

reference_image_base64 = image_to_base64("/root/workspace/Demo_Proj/agrirag/reranker/input.jpg")
image1_base64 = image_to_base64("/root/workspace/Demo_Proj/agrirag/reranker/cat.jpg")
image2_base64 = image_to_base64("/root/workspace/Demo_Proj/agrirag/reranker/cat2.jpg")
image3_base64 = image_to_base64("/root/workspace/Demo_Proj/agrirag/reranker/dog.jpg")
# chatanywhere api
url = "https://api.chatanywhere.tech/v1/chat/completions"
api_key = "sk-JYxUur2qWtLjVR6FI8EaVyKCD4MGfJHlk8gNfURwo4B5JLl5"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "gpt-4o",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "please tell me the difference between the following images,and this is picture 1:"},
                {"type": "image_url", "image_url": {
                    "url" : "http://pic.qingchengkg.cn/img/2020"}
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "this is picture 2:"},
                {"type": "image_url", "image_url": {
                    "url" : "http://pic.qingchengkg.cn/img/2021"}
                }
            ]
        }
    ],
    "max_tokens": 200,
    "temperature": 0.5
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}, {response.text}")

