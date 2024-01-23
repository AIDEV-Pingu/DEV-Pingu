from django.shortcuts import render, redirect
import spacy
from django.conf import settings
import numpy as np
from roboflow import Roboflow
from django.http import HttpResponse
from django.http import JsonResponse
from .forms import ImageUploadForm
from .models import ImageUpload
from .module_ocr import CLOVA_api, imageOCR, predict2crop  # OCR 모듈
from .module_crawler import NaverShoppingCrawler, SsgCrawler, MusinsaCrawler  # 크롤링 함수
from .module_spacy import predict_entities, delete_product, tokenize
import pandas as pd
import os
from collections import Counter


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

    # spacy 앙상블
    folder_lst = [f for f in os.listdir(settings.CONTENT_ROOT) if os.path.isdir(os.path.join(settings.CONTENT_ROOT, f))]
    model_lst = []
    for l in folder_lst:
        if not l.endswith('.config') and l != 'sample_data':
            model_lst.append(l)

    for model in model_lst:
        globals()[model] = spacy.load('content/' + model)


    all_words = []  # 모든 단어를 저장할 리스트 초기화

    for _, model in enumerate(model_lst):
        words = tokenize(predict_entities(ocr_result, globals()[model], '상품명'))
        all_words.extend(words)  # all_words 리스트에 단어 추가

    # 단어의 등장 횟수를 세기
    word_counts = Counter(all_words)

    # 가장 많이 등장한 단어들 추출 (예: 상위 5개)
    top_words = ' '.join([word[0] for word in word_counts.most_common(5)])

    # 제품명 선별
    top_words = delete_product(top_words)
    
    # 가격 선별
    nlp = spacy.load('content/Pingu_model_1_19_150_price')
    is_price = predict_entities(ocr_result, nlp,'가격')

    return JsonResponse({
        'ocr_result': ocr_result,
        'image_path': processed_img,  # 이미지 URL로 변경
        'product_name': top_words,
        'price': is_price
    })


# 크롤링 뷰 - 수정
def crawling_results_view(request):
    product_name = request.GET.get('product_name', '')
    site = request.GET.get('site', '')  # 사이트 선택 파라미터 추가

    # 초기화
    musinsa_results = naver_results = ssg_results = None

    # 선택된 사이트에 따라 해당 크롤러 실행
    if site == 'musinsa':
        musinsa_crawler = MusinsaCrawler(product_name)
        musinsa_results = musinsa_crawler.scrape()
        # musinsa csv / json - file path
        musinsa_path = os.path.join(settings.MEDIA_ROOT, 'dataframes/musinsa_products.csv')
        musinsa_json_path = os.path.join(settings.MEDIA_ROOT, 'dataframes/musinsa_products.json')
        # 크롤링 결과 csv로 저장
        musinsa_results.to_csv(musinsa_path, index=False)
        # csv to json
        musinsa_csv = pd.read_csv(musinsa_path)
        musinsa_csv = musinsa_csv.sort_values(by=['Price'])
        musinsa_to_json = musinsa_csv[['Product_Name', 'Price']].to_json(musinsa_json_path, orient='records', force_ascii=False)

    elif site == 'naver':
        naver_crawler = NaverShoppingCrawler(settings.NAVER_API_ID, settings.NAVER_API_SECRET, product_name)
        naver_results = naver_crawler.run()
        # naver csv / json - file path
        naver_path = os.path.join(settings.MEDIA_ROOT, 'dataframes/naver_products.csv')
        naver_json_path = os.path.join(settings.MEDIA_ROOT, 'dataframes/naver_products.json')
        # 크롤링 결과 csv로 저장
        naver_results.to_csv(naver_path, index=False)
        # csv to json
        naver_csv = pd.read_csv(naver_path)
        naver_csv = naver_csv.sort_values(by=['lprice'])
        naver_to_json = naver_csv[['title', 'lprice']].to_json(naver_json_path, orient='records', force_ascii=False)

    elif site == 'ssg':
        ssg_crawler = SsgCrawler()
        ssg_results = ssg_crawler.get_data(product_name)
        # ssg csv / json - file path
        ssg_path = os.path.join(settings.MEDIA_ROOT, 'dataframes/ssg_products.csv')
        ssg_json_path = os.path.join(settings.MEDIA_ROOT, 'dataframes/ssg_products.json')
        # 크롤링 결과 csv로 저장
        ssg_results.to_csv(ssg_path, index=False)
        # csv to json
        ssg_csv = pd.read_csv(ssg_path)
        ssg_csv = ssg_csv.sort_values(by=['prices'])
        ssg_to_json = ssg_csv[['product_names', 'prices']].to_json(ssg_json_path, orient='records', force_ascii=False)

    # 결과 반환
    return JsonResponse({
        'musinsa': musinsa_to_json if musinsa_results is not None else '',
        'naver': naver_to_json if naver_results is not None else '',
        'ssg': ssg_to_json if ssg_results is not None else ''
    })