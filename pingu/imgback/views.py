from django.shortcuts import render, redirect
import spacy
from django.conf import settings
import numpy as np
from roboflow import Roboflow
from django.http import HttpResponse
from django.http import JsonResponse
import os
from .forms import ImageUploadForm
from .models import ImageUpload
from .module_ocr import CLOVA_api, imageOCR, predict2crop  # OCR 모듈
from .module_crawler import NaverShoppingCrawler, SsgCrawler, MusinsaCrawler  # 크롤링 함수


# NLP앙상블 모델 구현중. 이환님 코드 기반으로 수정필요
nlp = spacy.load('content/Pingu_model_1_17_500')
nlp2 = spacy.load('content/Pingu_model_1_19_150_sm')
nlp3 = spacy.load('content/Pingu_model_1_19_150_product')
nlp3 = spacy.load('content/Pingu_model_1_19_150_price')

# img/upload
def image_upload_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()
            return redirect('ocr_view', image_id=image_instance.id)
    else:
        form = ImageUploadForm()
    return render(request, 'imgback/image_upload.html', {'form': form})

# img /upload -> 알아서넘어가기
def ocr_view(request, image_id):
    image_instance = ImageUpload.objects.get(id=image_id)
    image_path = os.path.join(settings.MEDIA_ROOT, str(image_instance.image))

    # Roboflow model 로드
    rf = Roboflow(api_key=settings.ROBOFLOW_API_KEY)
    project = rf.workspace().project(settings.ROBOFLOW_PROJECT)
    model = project.version(settings.ROBOFLOW_VERSION).model

    # 이미지에 OCR 적용
    cropped_img = predict2crop(model, image_path)

    if cropped_img is None:
        print("No valid image to process")
        return HttpResponse("No valid image to process")

    response = CLOVA_api(settings.CLOVA_API_KEY, settings.CLOVA_API_URL, cropped_img)
    ocr_result, processed_img = imageOCR(response, cropped_img) # // OCR





    # Spacy 모델을 사용하여 상품명과 가격 추출
    doc = nlp(ocr_result)
    product_name, price = None, None
    for ent in doc.ents:
        if ent.label_ == "상품명":
            product_name = ent.text
        elif ent.label_ == "가격":
            price = ent.text

    '''
    case = 0
    while product_name is None or price is None or case < 5:
        case += 1
        doc = nlp(ocr_result)
        for ent in doc.ents:
            if ent.label_ == "상품명" and product_name is None:
                product_name = ent.text
            elif ent.label_ == "가격" and price is None:
                price = ent.text
    '''

    return render(request, 'imgback/ocr_result.html', {
        'ocr_result' : ocr_result,
        'image_path': processed_img,
        'product_name': product_name,
        'price': price
    })

# 크롤링뷰. 아현님코드기반으로 수정필요.
def crawling_results_view(request):
    product_name = request.GET.get('product_name', '')
    site = request.GET.get('site', '')  # 사이트 선택 파라미터 추가

    # 초기화
    musinsa_results = naver_results = ssg_results = None

    # 선택된 사이트에 따라 해당 크롤러 실행
    if site == 'musinsa':
        musinsa_crawler = MusinsaCrawler(product_name)
        musinsa_results = musinsa_crawler.scrape()
    elif site == 'naver':
        naver_crawler = NaverShoppingCrawler(settings.NAVER_API_ID, settings.NAVER_API_SECRET, product_name)
        naver_results = naver_crawler.run()
    elif site == 'ssg':
        ssg_crawler = SsgCrawler()
        ssg_results = ssg_crawler.get_data(product_name)

    # 결과 반환
    return JsonResponse({
        'musinsa': musinsa_results.to_json(orient='records') if musinsa_results is not None else '',
        'naver': naver_results.to_json(orient='records') if naver_results is not None else '',
        'ssg': ssg_results if ssg_results is not None else ''
    })
