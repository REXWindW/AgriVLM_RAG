import requests

# 使用图床：http://pic.qingchengkg.cn/

# Define the URL and token (if needed)
upload_url = "http://pic.qingchengkg.cn/api/upload/"
token = "02ff831de986fe56b8172db138acee32"  # Replace with your actual token, if necessary

# Prepare the image file
image_path = "/root/workspace/Demo_Proj/agrirag/reranker/cat.jpg"  # Replace with the path to your image

# Prepare the headers (if token is used)
headers = {}
if token:
    headers['Authorization'] = f'Bearer {token}'

# Prepare the file payload
files = {'fileupload': open(image_path, 'rb')}

# Make the POST request to upload the file
response = requests.post(upload_url, headers=headers, files=files)

# Check the response
if response.status_code == 200:
    json_response = response.json()
    if json_response.get("success"):
        print("Image uploaded successfully!")
        print("Image URL:", json_response.get("url"))
    else:
        print("Upload failed:", json_response.get("error"))
else:
    print("Failed to connect to the server. Status code:", response.status_code)
