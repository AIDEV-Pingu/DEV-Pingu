# ocrtool/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('<int:image_id>/', views.ocr_view, name='ocr_view'),
]