import requests
import base64


# get base64 image
def encode_image(image_path): # to encode image to base64
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')



class GPT_reranker:
    '''
    GPT reranker
    因为gpt只能以image_url的形式输入图片，所以需要另外写一个上传和拉取图片链接的函数
    '''
    def __init__(self,
                img_key="02ff831de986fe56b8172db138acee32",
                api_key="sk-JYxUur2qWtLjVR6FI8EaVyKCD4MGfJHlk8gNfURwo4B5JLl5"):
        self.api_key = api_key
        self.img_key = img_key

    def rerank(self,input_image, img_list:list):
        '''
        使用gpt进行rerank
        参数：
        img_list: 一个list，每个元素对应json中的一个dict，包含path, id, label
        返回值：
        rerank_list: rerank后的图片列表，为了统一格式，使用同样的dict的list返回
        '''
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # system prompt 参考：https://chatgptcn.readthedocs.io/zh-cn/latest/prompt/system_prompt_cn/
        history = [
            {
                "role": "system",
                "content": "你是一个农业的叶片图像比较器，你会被给予一张输入叶片图片，和几张从数据库中检索的叶片图像和对应描述。你需要从中找出和输入叶片图片在病害特征上最相似的叶片图像，并返回其id。"
            }
        ]

        for idx,row in enumerate(img_list):
            path = row['path']
            idx = row['id']
            description = row['label'] # 输入图像的description=None

            base64_image = encode_image(path) # get base64

            if idx==0: # 
                tmp = 
                {
                    "role": "user",
                    "content": [
                        {
                        "type": "text",
                        "text": f"输入叶片图片："
                        },
                        {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        }
                    ]
        }

            else:
                tmp = {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"image {idx}:"}, # 这个编号实际上还是从1开始的，因为0图是input image。
                        {"type": "image_url", "image_url": {"url" : url}}
                    ]
                }
                
            history.append(tmp)

        # gpt request
                
        data = {
            "model": "gpt-4o",
            "messages": history,
            "max_tokens": 200,
            "temperature": 0.5
        }

        response = requests.post(gpt_url, headers=headers, json=data)

        if response.status_code == 200:
            response_json = response.json()
            return response_json['choices'][0]['message']['content']
        else:
            print(f"Error: {response.status_code}, {response.text}")

    def get_img_url(self, img_path): # 暂时不需要了
        '''
        图像上传图床并且获取url
        使用图床：http://pic.qingchengkg.cn/
        参数：
        img_path: 图像路径
        返回值：
        url: 图像url
        '''
        # header
        headers = {}
        headers['Authorization'] = f'Bearer {self.img_key}'

        files = {'fileupload': open(image_path, 'rb')}
        response = requests.post(upload_url, headers=headers, files=files)# get response

        # deal with response
        if response.status_code == 200:
            json_response = response.json()
            if json_response.get("success"):
                # print("Image uploaded successfully!")
                # print("Image URL:", json_response.get("url"))
                url =  json_reponse.get("url")
            else:
                print("Upload failed:", json_response.get("error"))
        else:
            print("Failed to connect to the server. Status code:", response.status_code)

        return url


if __name__ == '__main__':
    reranker = GPT_reranker()
    # url_list = ["http://pic.qingchengkg.cn/img/2027","http://pic.qingchengkg.cn/img/2024", 
    #     "http://pic.qingchengkg.cn/img/2025", "http://pic.qingchengkg.cn/img/2026"]

    url_list = ["http://pic.qingchengkg.cn/img/2020","http://pic.qingchengkg.cn/img/2021","http://pic.qingchengkg.cn/img/2022"]

    rerank_result = reranker.rerank(url_list)
    print(rerank_result)