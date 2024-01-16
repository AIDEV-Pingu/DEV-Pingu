from django.shortcuts import render
from imgupload.models import ImageUpload  # imgupload 앱의 이미지 모델
from .ocr_module import CLOVA_api, imageOCR, predict2crop  # OCR 모듈
from pingu import settings
import numpy as np
from roboflow import Roboflow
import cv2
import base64
import uuid
import time
import json
import requests
from django.http import HttpResponse
import os

# Create your views here.

def ocr_view(request, image_id):

    rf = Roboflow(api_key=settings.ROBOFLOW_API_KEY)
    project = rf.workspace().project(settings.ROBOFLOW_PROJECT)
    model = project.version(settings.ROBOFLOW_VERSION).model

    # CLOVA API 사용
    secret_key = settings.CLOVA_API_KEY
    api_url = settings.CLOVA_API_URL

    # 이미지 모델에서 이미지 인스턴스를 가져옴
    image_instance = ImageUpload.objects.get(id=image_id)
    image_path = os.path.join(settings.MEDIA_ROOT, str(image_instance.image))

    # 이미지에 OCR 적용
    org_img, cropped_img = predict2crop(model, image_path)  # 객체 탐지 및 크롭

    # cropped_img의 상태 확인
    if cropped_img is not None:
        print("cropped_img type:", type(cropped_img))
        print("cropped_img shape:", cropped_img.shape)
    else:
        print("cropped_img is None")

    # cropped_img의 유효성 확인
    if cropped_img is None:
        print("No valid image to process")
        # 적절한 처리 또는 오류 메시지 반환
        return HttpResponse("No valid image to process")

    response = CLOVA_api(secret_key, api_url, cropped_img)
    ocr_result, processed_img = imageOCR(response, cropped_img)

    # 결과를 템플릿에 전달
    return render(request, 'ocrtool/ocr_result.html', {'ocr_result': ocr_result, 'image_path': processed_img})
