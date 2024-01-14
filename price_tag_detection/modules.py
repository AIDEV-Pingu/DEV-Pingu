from libs import *

"""
Modules
"""

def CLOVA_api(secret_key, api_url, image : np.array):
    """
    Usage : CLOVA api 호출

    Parameters
    ----------
    secret_key : api key
    api_url : api_url
    image : 크롭된 image

    Returns
    -------

    response : api 호출 결과 (ex. 200,400,404, ...)

    """
    # Error check
    if image is None : 
        # print('FileNotFoundError: image is None for request CLOVA_api')
        return

    # Convert np.ndarray to bytes
    _, buffer = cv2.imencode('.jpg', image)
    file_data = buffer.tobytes()

    request_json = {
        'images': [
            {
                'format': 'jpg',
                'name': 'demo',
                'data': base64.b64encode(file_data).decode()
                #'url': image_url
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }
    payload = json.dumps(request_json).encode('UTF-8')
    headers = {
      'X-OCR-SECRET': secret_key,
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", api_url, headers=headers, data = payload)

    return response



def imageOCR(response, img : np.array):
    """
    Usage : api 적용 결과 (OCR 결과) 시각화

    Parameters
    ----------
    response : api 호출 결과
    img : 크롭된 이미지

    Returns
    -------
    temp : 추출된 text
    image : 크롭된 이미지 내 OCR 적용 결과

    """
    try : result = response.json()
    except :
        print('AttributeError: Responsed \'int\' object' ,response)
        return

    with open('result.json', 'w', encoding='utf-8') as make_file:
        json.dump(result, make_file, indent="\t", ensure_ascii=False)

    # Error 처리
    try : print(result['images'][0]['message'])
    except : return None, None

    # respone.json()에서 띄어쓰기 처리
    texts = connectWord(result)

    # 이미지 시각화
    bBs = [b['boundingPoly'] for b in result['images'][0]['fields']]

    # bounding box 표시
    for box in bBs:
        vertices = np.array([(int(point['x']), int(point['y'])) for point in box['vertices']], np.int32)
        vertices = vertices.reshape((-1, 1, 2))
        img = cv2.polylines(img, [vertices], isClosed=True, color=(255, 0, 0), thickness=2)

    # 이미지 보여주기
    cv2.imshow('IMAGE',img) # only colab
    # print(text)

    return texts, img



def connectWord(ocr_json):
    """
    Usage : OCR 결과 내 띄어쓰기 처리

    Parameters
    ----------
    ocr_json : api 호출 결과

    Returns -> str
    -------
    detected_texts : 최종 결과

    """

    detected_texts = ''

    # 필드 정보 추출
    fields = ocr_json['images'][0].get('fields', [])

    # 각 필드에 대해 y좌표 계산
    word_list = []
    for field in fields:
        bounding_poly = field.get('boundingPoly')
        infer_text = field.get('inferText')

        if bounding_poly and infer_text:
            vertices = bounding_poly['vertices']
            y_coord = vertices[0]['y']  # 첫 번째 꼭짓점의 y좌표를 사용
            word = infer_text
            word_list.append({'word': word, 'y_coord': y_coord})

    # y좌표가 유사한 단어를 그룹화
    grouped_words = []
    if word_list:  # word_list가 비어있지 않은 경우에만 처리
        current_group = [word_list[0]]

        for i in range(1, len(word_list)):
            if abs(word_list[i]['y_coord'] - word_list[i-1]['y_coord']) < 10:
                current_group.append(word_list[i])
            else:
                grouped_words.append(current_group)
                current_group = [word_list[i]]

        if current_group:
            grouped_words.append(current_group)

    for group in grouped_words:
        # 그룹 내의 단어들을 하나의 문자열로 합침
        group_text = ' '.join([word_info['word'] for word_info in group])

        # 문자열이 정수로만 이루어져 있지 않은 경우에만 출력
        if not group_text.isdigit():
            detected_texts += group_text
            detected_texts += '\n'

    return detected_texts



def modelPredict(model, input_Data):
    try : predictions_data = model.predict(input_Data, confidence=50, overlap=50).json()
    except :
        print('Predict Error')
        return None
    # image_path = predictions_data['predictions'][0]['image_path']  # Assuming all predictions have the same image path

    return predictions_data



def predict2crop(model, folder_path, image_file, resize = 256):
    """
    Usage : 객체 탐지 후 Bounding Box 기준으로 이미지 Cropping

    Parameters
    ----------
    model : Object Detection Model
    folder_path : 데이터 폴더 경로
    image_file : 데이터 파일 경로

    Returns : (original_image, cropped_image)
    -------
    type : tuple
    original_image : 원본 이미지
    cropped_image : 크롭된 이미지

    """
    image_path = folder_path + image_file
    img_size = resize # img_size * img_size

    org_img = cv2.imread(image_path)
    if org_img is None:
        print(f"Error: Unable to read the image file {image_path}")
        return None, None

    rsz_img = cv2.resize(org_img, (img_size, img_size), interpolation= cv2.INTER_AREA)
    adc_img = auto_adjust_contrast(rsz_img)


    predictions_data = modelPredict(model, input_Data = adc_img) # resize된 img속에서 찾은 bbox 좌표

    print('Detected Obj : ', len(predictions_data['predictions']))

    if predictions_data is None :
        print('Detect Nothing. It\'s Too Close')
        return org_img, org_img

    if len(predictions_data['predictions']) > 1:
        print('! Error : Multiple detection Error. Take more closer')
        return None, None

    orgBBcoor = predBBcoor(org_img, predictions_data)
    cropped_img = imgCrop(org_img, orgBBcoor) #원본이미지에서 crop

    return org_img, cropped_img



def imgCrop(img, bbCoor):
    """
    Usage : resize된 이미지에서의 바운딩 박스 좌표를 원본 이미지의 바운딩 박스 좌표로 변환

    Parameters
    ----------
    img : 원본 이미지(no resize)
    bbCoor : (x, y, width, height) -> 원본 이미지에서의 bbox 좌표

    Returns : np.array
    -------
    cropped_img

    """
    if None in bbCoor : return img

    x, y, width, height = bbCoor # real coordinate

    half_w, half_h = round(width/2), round(height/2)

    cropped_img = img[abs(y-half_h) : y+half_h, abs(x-half_w ): x+half_w] # img crop

    # # 결과 시각화
    # cv2.rectangle(img, (x - half_w, y - half_h), (x + half_w, y + half_h), (0, 255, 0), 2)
    # print('\n Original')
    # cv2.imshow(img) # only colab
    # print('\n Cropped')
    # cv2.imshow(cropped_img) # only colab

    return cropped_img



def predBBcoor(org_img : np.array, pred_data : list, resize=256):
    """
    Usage : resize된 이미지에서의 바운딩 박스 좌표를 원본 이미지의 바운딩 박스 좌표로 변환

    Parameters
    ----------
    org_img : 원본 이미지(no resize)
    pred_data : list

    Returns : tuple
    -------
    x, y, width, height

    """
    try : prediction = pred_data['predictions'][0] # dict
    except : return None, None, None, None # 탐지 되지 않을 시

    # resized bbox coordinate
    rx, ry, rwidth, rheight = int(prediction['x']), int(prediction['y']), int(prediction['width']), int(prediction['height'])
    half_w, half_h = round(rwidth/2), round(rheight/2)

    # real h, w
    h, w, _ = org_img.shape
    # real bbox coordinate
    x, y, width, height = round((w*rx)/resize), round((h*ry)/resize), round((rwidth*w)/256), round((rheight*h)/256)

    return x, y, width, height



# preprocessing : auto_adjust_contrast
def auto_adjust_contrast(image : np.array):
    # Flatten the image to 1D array
    try : flat_image = image.flatten()
    except : return None

    # Compute the histogram
    histogram, bins = np.histogram(flat_image, bins=256, range=(0, 256))

    # Compute the cumulative distribution function (CDF)
    cdf = histogram.cumsum()

    # Normalize the CDF
    cdf_normalized = cdf / cdf.max()

    # Perform histogram equalization
    equalized_image = np.interp(flat_image, bins[:-1], cdf_normalized * 255).reshape(image.shape)

    return equalized_image.astype(np.uint8) # np.array
