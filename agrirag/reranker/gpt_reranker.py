import requests
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

    def get_img_url(self, img_path):
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

    def rerank(self,url_list:list):
        '''
        使用gpt进行rerank
        参数：
        url_list: 图像url列表,需要另外写一个函数从img list转换到url list
        返回值：
        rerank_list: rerank后的图像列表
        '''
        # url_list = []
        # for img in img_list:
        #     img_url = self.get_img_url(img)
        #     url_list.append(img_url)

        gpt_url = "https://api.chatanywhere.tech/v1/chat/completions"

        # gpt header
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        history = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant to compare different images."
            }
        ]

        for idx,url in enumerate(url_list):
            if idx==0:
                tmp = {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Returns the ID of the most similar image without redundant output, reference image:"},
                        {"type": "image_url", "image_url": {"url" : url}}
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


if __name__ == '__main__':
    reranker = GPT_reranker()
    # url_list = ["http://pic.qingchengkg.cn/img/2027","http://pic.qingchengkg.cn/img/2024", 
    #     "http://pic.qingchengkg.cn/img/2025", "http://pic.qingchengkg.cn/img/2026"]

    url_list = ["http://pic.qingchengkg.cn/img/2020","http://pic.qingchengkg.cn/img/2021","http://pic.qingchengkg.cn/img/2022"]

    rerank_result = reranker.rerank(url_list)
    print(rerank_result)