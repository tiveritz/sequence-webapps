from django.shortcuts import render, reverse
from django.conf import settings
import requests
from django.http import HttpResponseRedirect
from ..forms import UploadImage


API_URL = settings.API_URL
RSV = settings.REQUESTS_SSL_VERIFICATION
API_IMAGE = API_URL + '/sequence/media/images/'


def images(request):
    r = requests.get(API_IMAGE, verify = RSV)
    images = r.json()

    print(images)

    return render(request, 'pages/modules_images.html', {
        'menu' : 'pictures',
        'images' : images
        })

def image_upload(request):
    if request.method == 'POST':
        form = UploadImage(request.POST, request.FILES)
        if form.is_valid():
            payload = {'title': '-'}
            files = {'image': request.FILES['image']}
            requests.post(API_IMAGE, data=payload, files=files, verify = RSV)

        return HttpResponseRedirect(reverse('images'))

    form = UploadImage()
    return render(request, 'pages/image_upload.html', {'form': form})
