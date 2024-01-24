from django.urls import path
from . import views

urlpatterns = [
    path('', views.image_upload_view, name='image_upload'),
    path('ocr/<int:image_id>/', views.ocr_view, name='ocr_view'),
    path('ocr/crawling', views.crawling_results_view, name='crawling_results'),
    # Add other URL patterns here as needed
]