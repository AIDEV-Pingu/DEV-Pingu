from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import ImageUpload

# Create your views here.
def index(request):
    return render(request, "main/index.html")


def image_upload_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()
            return redirect('image_display', image_id=image_instance.id)
    else:
        form = ImageUploadForm()

    return render(request, 'imgupload/image_upload.html', {'form': form})

def image_display_view(request, image_id):
    image = ImageUpload.objects.get(id=image_id)
    return render(request, 'imgupload/image_display.html', {'image': image})

