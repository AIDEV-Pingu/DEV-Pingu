from django.shortcuts import render, redirect
import spacy
from django.conf import settings
import numpy as np
from roboflow import Roboflow
from django.http import HttpResponse
import os
from .module_ocr import CLOVA_api, imageOCR, predict2crop  # OCR 모듈
from .forms import ImageUploadForm
from .models import ImageUpload


# Create your views here.
nlp = spacy.load('content/Pingu_model_1_17_1000')

def image_upload_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()
            return redirect('ocr_view', image_id=image_instance.id)
    else:
        form = ImageUploadForm()
    return render(request, 'imgback/image_upload.html', {'form': form})

def ocr_view(request, image_id):
    image_instance = ImageUpload.objects.get(id=image_id)
    image_path = os.path.join(settings.MEDIA_ROOT, str(image_instance.image))

    # Roboflow model 로드
    rf = Roboflow(api_key=settings.ROBOFLOW_API_KEY)
    project = rf.workspace().project(settings.ROBOFLOW_PROJECT)
    model = project.version(settings.ROBOFLOW_VERSION).model

    # 이미지에 OCR 적용
    org_img, cropped_img = predict2crop(model, image_path)

    if cropped_img is None:
        print("No valid image to process")
        return HttpResponse("No valid image to process")

    response = CLOVA_api(settings.CLOVA_API_KEY, settings.CLOVA_API_URL, cropped_img)
    ocr_result, processed_img = imageOCR(response, cropped_img)

    # Spacy 모델을 사용하여 상품명과 가격 추출
    doc = nlp(ocr_result)
    product_name, price = None, None
    for ent in doc.ents:
        if ent.label_ == "상품명":
            product_name = ent.text
        elif ent.label_ == "가격":
            price = ent.text

    return render(request, 'imgback/ocr_result.html', {
        'image_path': processed_img,
        'product_name': product_name,
        'price': price
    })
