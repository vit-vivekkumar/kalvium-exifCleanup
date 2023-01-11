from django.shortcuts import render
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, HttpResponseNotModified
from django.utils.http import http_date
from django.contrib import messages
from django.views.static import was_modified_since

from PIL import Image


def home(request):
    if request.method == 'POST':
        img_file = request.FILES['img']
        img_name = request.FILES['img'].name

        if img_file.size > 2000000:
            messages.error(request, f"Unable to process, please try again!")
            return HttpResponseBadRequest()
        image = Image.open(img_file)
        data = list(image.getdata())
        image_without_exif = Image.new(image.mode, image.size)
        image_without_exif.putdata(data)
        # image_without_exif.save('without_exif-'+img_name)
        
        response = HttpResponse(content_type='image/jpeg')
        image_without_exif.save(response, 'jpeg')
        response['Content-Disposition'] = 'attachment; filename={0}'.format('without_exif-'+img_name)
        messages.success(request, f"Successfully! Exif Data Removed")
        return response
    return render(request, 'home.html')



