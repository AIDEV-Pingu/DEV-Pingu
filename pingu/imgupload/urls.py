from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.image_upload_view, name='image_upload'),
    path('image/<int:image_id>/', views.image_display_view, name='image_display'),
]