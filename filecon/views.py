from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse,JsonResponse
from .models import ImageCollection, ImageInstance
from .forms import ImageUploadFormSet
import img2pdf
import os
from django.conf import settings

@login_required
def upload_images(request):
    if request.method == 'POST':
        formset = ImageUploadFormSet(request.POST, request.FILES, queryset=ImageInstance.objects.none())
        if formset.is_valid():
            collection = ImageCollection.objects.create(folder_name=f"{request.user.username}_Uploaded_Collection")
            images_uploaded = False
            for form in formset.cleaned_data:
                if form:
                    imginst = form['imginst']
                    image_instance = ImageInstance.objects.create(imginst=imginst)
                    collection.collection.add(image_instance)
                    images_uploaded = True
            if not images_uploaded:
                return render(request,'no_images_uploaded.html',{'user': request.user})
            
            return redirect('convert_images_to_pdf',collection_id = collection.id)
    else:
        formset = ImageUploadFormSet(queryset=ImageInstance.objects.none())
    return render(request, 'upload_images.html', {'formset': formset,'user': request.user})

@login_required
def convert_images_to_pdf(request, collection_id):
    collection = get_object_or_404(ImageCollection, id=collection_id)
    image_instances = collection.collection.all()

    if not image_instances.exists():
        return render(request, 'no_images_uploaded.html',{'user': request.user})

    image_files = [img.imginst.path for img in image_instances]
    if not image_files:
        return render(request, 'no_images_uploaded.html',{'user': request.user})
    
    image_files.sort()
    pdf_bytes = img2pdf.convert(image_files)
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{collection.folder_name}.pdf"'
    return response

@login_required
def clear_media(request):
    media_root = settings.MEDIA_ROOT
    
    if os.path.isdir(media_root):
        try:
            for filename in os.listdir(media_root):
                file_path = os.path.join(media_root, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            return JsonResponse({'status': 'success', 'message': 'Media cleared successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Failed to clear media: {str(e)}'})
    
    return JsonResponse({'status': 'error', 'message': 'Media directory not found.'})