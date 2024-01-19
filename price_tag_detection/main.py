from modules import *

'''data load'''
# 데이터가 존재하는 폴더 경로 지정
IMG_FOLDER = '' # for test
#files = os.listdir(IMG_FOLDER)

##### input data 입력 #####
INPUT_IMG = '/Users/jykim/myWS/Dev_AI_6/proJects/Pingu_Dev_JPG_Data/common-6.jpeg'

# r
"""model load"""
rf = Roboflow(api_key="MUs7pvPAXmkOJGSMZ9dm")
project = rf.workspace().project("wow-2ysdx")
model = project.version(1).model

# OCR api
secret_key = "Y0l6ZHF1Um9CSWp3aHpJU3JDeFdpUGp1cG16T3hFQkg="
api_url = 'https://p0fsnflvaw.apigw.ntruss.com/custom/v1/27259/8a921c4c7d4e552c974b102e64c6227f3a2995ca938c066ddeb1442d6bf4b67c/general'

# IMG -> Object Detections 
original_img, cropped_img = predict2crop(model, image_path= INPUT_IMG)

response = CLOVA_api(secret_key ,api_url ,image = cropped_img)
texts, img = imageOCR(response, cropped_img)

result = ' '.join(texts)
print(result)
