from django.shortcuts import render
import spacy

# Create your views here.
nlp = spacy.load('content/Pingu_NER_model.spacy')

def index(request):
    analysis_result = ""
    if request.method == 'POST':
        input_text = request.POST.get('text')
        doc = nlp(input_text) # x => OCR처리된 문자열
        # spacy.displacy.render(doc, style='ent', jupyter=True)
        # doc.ents.label_
        # 분석 결과를 얻는 코드 작성
        analysis_result = doc.ents[0]

    return render(request, 'spacyapp/spacy_index.html', {'analysis_result': analysis_result})