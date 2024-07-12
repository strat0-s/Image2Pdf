from django.urls import path
from .views import upload_images, convert_images_to_pdf

urlpatterns = [
    path('upload/', upload_images, name='upload_images'),
    path('convert/<int:collection_id>/', convert_images_to_pdf, name='convert_images_to_pdf'),
]
