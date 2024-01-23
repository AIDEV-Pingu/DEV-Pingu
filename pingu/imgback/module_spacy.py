import re


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

# 문장을 단어로 분리하는 함수
def tokenize(sentence):
    # 간단하게 공백을 기준으로 단어 분리
    return sentence.split()

'''
def predict_product(text, model_lst):
  from collections import Counter

  for idx, model in enumerate(model_lst):
    globals()['words' + f'{idx}'] = tokenize(predict_entities(text, globals()[model],'상품명'))
  word_counts = Counter(words1 + words2 + words3)
  top_words = ' '.join([word[0] for word in word_counts.most_common(5)])

  top_words = delete_product(top_words)
  return top_words

## price predict
### 여기서 text는 OCR을 통해 얻은 문장
predict_entities(text, Pingu_model_1_19_150_price,'가격')
'''