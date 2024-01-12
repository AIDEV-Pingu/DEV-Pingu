from modules import *

'''data load'''
# 데이터가 존재하는 폴더 경로 지정
IMG_FOLDER = '/Users/jykim/Downloads/Pingu_Dev_JPG_Data 3/'
files = os.listdir(IMG_FOLDER)

##### input data 입력 #####
INPUT_IMG = 'common-6.jpeg'

# re
"""model load"""
rf = Roboflow(api_key="eyKD4VJQ4nRqtosRytMg")
project = rf.workspace().project("price-tag-dxlmv")
model = project.version(15).model

# OCR api
secret_key = "Y0l6ZHF1Um9CSWp3aHpJU3JDeFdpUGp1cG16T3hFQkg="
api_url = 'https://p0fsnflvaw.apigw.ntruss.com/custom/v1/27259/8a921c4c7d4e552c974b102e64c6227f3a2995ca938c066ddeb1442d6bf4b67c/general'

# IMG -> Object Detections 
original_img, cropped_img = predict2crop(model, folder_path = IMG_FOLDER ,image_file = INPUT_IMG)

response = CLOVA_api(secret_key ,api_url ,image = cropped_img)
texts, img = imageOCR(response, img = cropped_img)

result = ' '.join(texts)

