from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import ImageCollection, ImageInstance
from .forms import ImageUploadFormSet
import img2pdf
import os
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm

def upload_images(request):
    if request.method == 'POST':
        formset = ImageUploadFormSet(request.POST, request.FILES, queryset=ImageInstance.objects.none())
        if formset.is_valid():
            collection = ImageCollection.objects.create(folder_name="User_Uploaded_Collection")
            images_uploaded = False
            for form in formset.cleaned_data:
                if form:
                    imginst = form['imginst']
                    image_instance = ImageInstance.objects.create(imginst=imginst)
                    collection.collection.add(image_instance)
                    images_uploaded = True
            if not images_uploaded:
                return render(request,'no_images_uploaded.html')
            
            return redirect('convert_images_to_pdf',collection_id = collection.id)
    else:
        formset = ImageUploadFormSet(queryset=ImageInstance.objects.none())
    return render(request, 'upload_images.html', {'formset': formset})

def convert_images_to_pdf(request, collection_id):
    collection = get_object_or_404(ImageCollection, id=collection_id)
    image_instances = collection.collection.all()

    if not image_instances.exists():
        return render(request, 'no_images_uploaded.html')

    image_files = [img.imginst.path for img in image_instances]
    if not image_files:
        return render(request, 'no_images_uploaded.html')
    
    image_files.sort()
    pdf_bytes = img2pdf.convert(image_files)
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{collection.folder_name}.pdf"'
    return response

def clear_media(request):
    media_root = settings.MEDIA_ROOT
    
    if os.path.isdir(media_root):
        for filename in os.listdir(media_root):
            file_path = os.path.join(media_root, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")
    
    return redirect('upload_images')

