from django.urls import path
from .views import upload_images, convert_images_to_pdf,clear_media

urlpatterns = [
    path('upload/', upload_images, name='upload'),
    path('convert/<int:collection_id>/', convert_images_to_pdf, name='convert_images_to_pdf'),
    path('clear_media/', clear_media, name='clear_media'),
]
