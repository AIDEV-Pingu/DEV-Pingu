from django.shortcuts import render
import spacy

# Create your views here.
nlp = spacy.load('content/Pingu_model_1_15')

def index(request):
    if request.method == 'POST':
        input_text = request.POST.get('text')
        doc = nlp(input_text) # x => OCR처리된 문자열
    return render(request, 'spacyapp/spacy_index.html')

def result_view(request):
    analysis_result = ""
    price_result = ""
    if request.method == 'POST':
        input_text = request.POST.get('text')
        doc = nlp(input_text)
        for t in doc.ents:
            if t.label_ == "상품명":
                analysis_result = t.text
            else:
                analysis_result = None
            
            if t.label_ == "가격":
                price_result = t.text
            else:
                price_result = None
        
    return render(request, 'spacyapp/spacy_result.html', {'analysis_result': analysis_result, 'price_result' : price_result})