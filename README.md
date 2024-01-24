# Pingu's Price Analysis Portal (PPAP)
Programmers Dev코스 4조 핑구입니당~~

### 진열대 상품 가격표 인식을 통한 최저가 사이트 제공

- 프로젝트 기간 : 2023.12.20.(금)  ~ 2024.01.26.(목)



### 🤝팀원

| 이름   | 담당 영역                                                    | Github                        |
| ------ | ------------------------------------------------------------ | ----------------------------- |
| 최갑주 | | |
| 성현규 | | |
| 서이환 | 전처리, 모델링 | https://github.com/kawaipato |
| 김정연 | 전처리, YOLOv8 및 OCR 모델링, 웹 프론트 | https://github.com/JY-maru |
| 강아현 | | |




### 📝Description

- [상세화면]() 
- OCR로 진열대 상품 가격표 인식 후 해당 상품의 최저가 사이트를 제공한다.
- 기획의도: 오프라인 매장에서 물건을 구매할 때 해당 상품의 최저가가 궁금할 때가 많다.
    - 오프라인 매장별로도 할인율이 제각각이다.
    - 어느 매장은 정가 어느 매장은 할인을 하는 경우가 있는데 이는 온라인에서 편차가 더욱 크다.




### 🥇GOAL

- 사용자의 이미지 내 가격표만 인식한다.
- 인식된 가격표에서 텍스트만 추출한다.
- 추출된 텍스트에서 상품명과 가격을 뽑아와서 해당 상품의 최저가 가격 정보를 제공한다.
- Django, React 등을 활용한 실제 서비스 설계


### 💻 필수 요구사항

| No.  | 구분               | 기능                                 | 구현 정도(⭐⭐⭐⭐⭐)                                            |
| ---- | ------------------ | ------------------------------------ | ----------------------------------------------------------- |
|    1 |이미지 업로드 및 처리    | 사용자의 가격표 이미지 업로드             | |
|    2 |가격표 탐지(YOLOv8)    |  가격표 탐지 및 이미지 크롭 | | ⭐⭐⭐⭐ |
|    3 |OCR                 | 이미지에서 텍스트를 추출                 | | ⭐⭐⭐⭐|
|    4 |NER                 | 추출된 텍스트 중에서 상품명을 식별         | ⭐⭐⭐⭐ |
|    5 |상품명 검색 기능        | 사용자가 제공한 정보를 처리 (상품명, 가격)  | |
|    6 |가격 비교 및 표시       | 추출한 상품명을 기반으로 크롤링 후 최저가 제공 | |
|    7 |                    | 검색 결과를 사용자에게 제공하는 인터페이스   | |



### 🛠Tech Stack

![image](https://github.com/AIDEV-Pingu/DEV-Pingu/assets/128393917/8c0cf0b1-3e0d-4ab3-94fe-09c607d2808a)





### 🏔컴포넌트 구조

이미지



### 🎮 서비스 플로우 차트

![pingu_flow](https://github.com/AIDEV-Pingu/DEV-Pingu/assets/70644095/0ee465ab-f40e-411e-a304-60ce706e6868)



### 📅개발일지

| No.  | Date     | Category   | Function                                                         | Done                                                         |
| ---- | -------- | ------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
|     1|2024/01/05|  CV   | 가격표 크롭 | 직접 찍은 이미지에서 가격표만 크롭하기 구현 - Roboflow API 사용 |
|     2|2024/01/05|  CV   | 가격표 크롭 | 가격표만 추출하는 모델 추가적으로 서치 |
|     3|2024/01/05|  NLP   | 상품명 추출 | 가격표 내 텍스트 전체 불러오기 |
|     4|2024/01/08|  WEB   | 상품 정보 크롤링 | 쇼핑몰 사이트 크롤링해서 상품 정보 가져오기 |
|     5|2024/01/08|  CV   | 가격표 크롭 | Roboflow API로 크롭되지 않은 이미지는 contour로 가격표 인식해서 가져오도록 구현 |
|     6|2024/01/09|  CV   | 가격표 크롭 및 OCR | 가격표만 정교하게 크롭한 후 OCR API로 이미지 내 텍스트만 추출 |
|     7|2024/01/15|  NLP   | 상품명 추출 | 텍스트 내에서 상품명과 가격 추출 |
|     8|2024/01/16|  WEB   | 웹 구현 (프론트) | 이미지 업로드 및 업로드 된 이미지 불러오기 |
|     9|2024/01/17|  WEB   | 웹 구현 (백)    | 이미지에서 크롭 -> OCR -> NER 진행 후 <br /><상품명>과 <가격>, <크롭된 이미지> 보여주기 구현 |
|    10|2024/01/18|  NLP   | 상품명 추출 | ko_core_news_lg 모델, ner + attributer_ruler 학습한 모델<br />**- 추가적인 모델링 작업으로 모델 성능 높이는 중** |
|    11|2024/01/19|  NLP   | 상품명 추출 | 상품명만 인식하는 모델, 가격만 인식하는 모델 생성 |
|    12|2024/01/19|  WEB   | 웹 구현 | React, Django 연결 |
|    13|2024/01/22|  NLP   | 모델링 완성 | 성능이 높은 4가지의 모델을 결합하여 앙상블 모델 생성  |



### 💎배웠던 점

| Name   | Content                                                      |
| ------ | ------------------------------------------------------------ |




### 🔥이슈 관리

| No.  | Name   | Content                                                      | Solve    | follow-up                                                    |
| ---- | ------ | ------------------------------------------------------------ | -------- | ------------------------------------------------------------ |
|     1|        | 직접 찍은 이미지에서 가격표만 크롭하는데 어려움<br />- 가격표만 인식하는 모델들은 몇 개 있지만 대부분이 외국어 데이터 | 해결 완료 | |
|     2|        | 추출된 텍스트에서 NER로 상품명만 추출하는 것에 문제<br />- 다른 모델을 돌릴 떄는 train에 오버피팅되어 새로운 text에 적용하기 어려움<br />- train 시킬 데이터 부족<br />- 인식된 텍스트가 많은 경우 태깅 어려움<br />- roi 영역을 지정하기에는 가격표마다 디자인과 텍스트의 위치가 다른 문제 | | |
|     3|        | OCR 진행 후 띄어쓰기 문제<br />- 상품명을 하나로 묶어서 처리해야하는데<br />-텍스트를 추출하고 나서 상품명에 띄어쓰기가 있는 경우 처리 어려움 | 해결 완료 | OCR을 이미지 내 y축을 기준으로 그룹핑|
|     4|        | 가격을 태깅할 때 문제<br />- 가격이 텍스트의 앞쪽에 위치한 경우 가격 태그로 인식하지 못하는 문제<br />-가격 태그가 2개 이상 추출되는 경우가 발생 | 해결 완료 | 노이즈 데이터 생성 및 앙상블 모델 생성 |


### 🎨 서비스 구현
| No   | 기능                                                         | 기능 설명                                                    | 구현 정도 | 실제 구현 수준                             |
| ---- | ------------------------------------------------------------ | ------------------------------------------------------------ | ---------------- | ------------------------------------------ |
|     1| 이미지 업로드 | 사용자가 가격표를 인식하고 싶은 이미지를 업로드<br />- 가격을 비교하고 싶은 상품의 가격표를 포함하고 있는 이미지를 업로드 | | |
|     2| 가격표 추출 결과 | 크롭된 가격표 이미지<br />- 상품명, 가격 정보를 사용자에 제공 | | |
|     3| 최저가 정보 | 해당 상품의 최저가 사이트를 사용자에 제공 | | |
|     4| 쇼핑몰 선택 버튼 | 원하는 쇼핑몰을 선택하여 가격 비교 서비스 제공 | | |




### 🤔 느낀점

- #### 이름

- #### 이름

- #### 이름

- #### 이름

- #### 이름



---

[readme 참고 페이지 출처](https://github.com/siwon-park/Movie_Community_Web/blob/master/README.md)
