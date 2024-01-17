from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.image_upload_view, name='image_upload'),
    path('ocr/<int:image_id>/', views.ocr_view, name='ocr_view'),
    # Add other URL patterns here as needed
]