import re
import spacy


# spacy 앙상블 모델 구현중

for model in model_lst:
  globals()[model] = spacy.load('/content/' + model + '/content/' + model)

  
def jaccard(str1, str2):
    a = set(str1.lower().split())
    b = set(str2.lower().split())
    c = a.intersection(b)
    if len(a) == 0 or len(b) == 0:
      return 0
    else:
      return float(len(c)) / (len(a) + len(b) - len(c))
    

def predict_entities(text, model, label):
    doc = model(text)
    ent_array = []
    for ent in doc.ents:
        start = text.find(ent.text)
        end = start + len(ent.text)
        new_int = [start, end, ent.label_]
        if new_int not in ent_array:
            ent_array.append([start, end, ent.label_])
    ent_array = [t for t in ent_array if t[2] == label]
    selected_text = text[ent_array[0][0]: ent_array[0][1]] if len(ent_array) > 0 else ''
    return selected_text


def show_me_the_jaccard(model):
  jaccard_score1, jaccard_score2 = 0, 0
  for text, entity in tqdm(TRAIN_DATA):
    p1, p2 = [t for t in entity['entities'] if t[2] == '가격'], [t for t in entity['entities'] if t[2] == '상품명']
    jaccard_score1 += jaccard(predict_entities(text, model, '가격'), text[p1[0][0]:p1[0][1]] if len(p1) > 0 else '')
    jaccard_score2 += jaccard(predict_entities(text, model, '상품명'), text[p2[0][0]:p2[0][1]] if len(p2) > 0 else '')
  print(f'Average Price Jaccard Score is {jaccard_score1 / len(TRAIN_DATA)}')
  print(f'Average Product Jaccard Score is {jaccard_score2 / len(TRAIN_DATA)}')


for model in model_lst:
  print('#'*100)
  print(str(model))
  show_me_the_jaccard(globals()[model])
  print('\n')


def predict_entities(text, model, label):
    doc = model(text)
    ent_array = []

    for ent in doc.ents:
        start = text.find(ent.text)
        end = start + len(ent.text)
        new_int = [start, end, ent.label_]
        if new_int not in ent_array:
            ent_array.append([start, end, ent.label_])

    ent_array = [t for t in ent_array if t[2] == label]

    if len(ent_array) > 0 and label == '상품명':
        selected_texts = ' '.join([text[t[0]: t[1]] for t in ent_array])
    elif len(ent_array) > 0 and label == '가격':
        # 엔트리를 하나만 인식하는 경우
        if len(ent_array) == 1:
          ent_array = [text[t[0]: t[1]].split() for t in ent_array][0]
          ent_array = [sorted(ent_array,reverse=True)[0]]
          selected_texts = [re.sub(r'[^0-9]', '', t) for t in ent_array]

        # 엔트리를 두개 이상 인식하는 경우
        else:
          selected_texts = [re.sub(r'[^0-9]', '', text[t[0]: t[1]]) for t in ent_array]
        selected_texts = [int(price) for price in (delete_price(price) for price in selected_texts) if price is not None]
        selected_texts = sorted(selected_texts,reverse=True)

        if len(selected_texts) >= 2:
          selected_texts = selected_texts[1]
        elif len(selected_texts) == 1:
          selected_texts = selected_texts[0]
        else: selected_texts = 'No'

        ## 예외처리..
        if len(str(selected_texts)) == 8:
          if str(selected_texts)[:4] > str(selected_texts)[4:]:
            selected_texts = int(str(selected_texts)[4:])
          else: selected_texts = int(str(selected_texts)[:4])

    else:
        selected_texts = ''

    return selected_texts


def delete_product(sentence):
  sentence = re.sub(r'\b\d+원\b','',sentence)
  sentence = re.sub(r'[^a-zA-Z0-9가-힣\s]', '', sentence)
  words_to_remove = [')','NEW', 'ITEM', '교차상품', '기획상품', '행사', '할인', 'SALE',
                     '동일행사품목', '교차가능', '정상가', '동일품목', '가격할인', '추천',
                     '(','OPEN','특가행사','단독','상품','LAST','₩','단위','가격','구매시']
  for word in words_to_remove:
      sentence = sentence.replace(word, '')
  return sentence


def delete_price(sentence):
  sentence = re.findall(r'\b\d+00?(?:\b|,)', sentence)
  if sentence:
    return sentence[0]
  else:
    return None
  

### 상품명 추출
from collections import Counter

text = test_data[random.randint(0,len(test_data))]
print(text)

# 문장을 단어로 분리하는 함수
def tokenize(sentence):
    # 간단하게 공백을 기준으로 단어 분리
    return sentence.split()

for idx, model in enumerate(model_lst):
  globals()['words' + f'{idx}'] = tokenize(predict_entities(text, globals()[model],'상품명'))

# 단어의 등장 횟수를 세기
word_counts = Counter(words1 + words2 + words3)

# 가장 많이 등장한 단어들 추출 (예: 상위 5개)
top_words = ' '.join([word[0] for word in word_counts.most_common(5)])

top_words = delete_product(top_words)
print("추출된 문자:", top_words)


text = test_data[random.randint(0,len(test_data)-1)]
print(text)
predict_entities(text, Pingu_model_1_19_150_price,'가격')