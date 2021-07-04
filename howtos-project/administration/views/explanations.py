from django.shortcuts import redirect, render, reverse
from django.conf import settings
import requests
from django.http import HttpResponseRedirect
from ..forms import CreateText


API_URL = settings.API_URL
RSV = settings.REQUESTS_SSL_VERIFICATION
API_EXPLANATION_TEXT = API_URL + '/howtos/v1/explanation/'
API_EXPLANATION_CODE = API_URL + '/howtos/v1/explanation/'


def text(request):
    r = requests.get(API_EXPLANATION_TEXT, verify = RSV)
    texts = r.json()

    return render(request, 'pages/modules_text.html', {
        'menu' : 'steps',
        'texts' : texts
        })

def text_create(request):
    if request.method == 'POST':
        form = CreateText(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            payload = {
                'type' : 'text',
                'title' : title,
                'content' : content,
            }

            r = requests.post(API_EXPLANATION_TEXT, json = payload, verify = RSV)
            id = r.json()['uri_id']

            return HttpResponseRedirect(reverse('steps_edit', args=[id]))
    
    form = CreateText()

    return render(request, 'pages/text_create.html', {'form': form})

def code(request):
    r = requests.get(API_EXPLANATION_CODE, verify = RSV)
    codes = r.json()

    return render(request, 'pages/modules_code.html', {
        'menu' : 'steps',
        'codes' : codes
        })
