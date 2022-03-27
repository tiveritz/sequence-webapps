from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
import requests
import json


API_URL = settings.API_URL
RSV = settings.REQUESTS_SSL_VERIFICATION
API_SEQUENCE = API_URL + '/sequence/guides/sequence/{}/'
API_SEQUENCE_GUIDE = API_URL + '/sequence/guides/sequence/{}/public/'
API_STEP_GUIDE = API_URL + '/sequence/guides/sequence/{}/{}/{}/'


def home(request):
    return render(request, './home.html',{'version': settings.VERSION})

def viewer(request):
    url = API_SEQUENCE.format('public')
    r = requests.get(url, verify = RSV)
    sequences = r.json()
    
    return render(request, './viewer.html', {'sequences': sequences})

def view_sequence(request, api_id):
    r = requests.get(API_SEQUENCE_GUIDE.format(api_id), verify = RSV)
    sequence = r.json()

    return render(request, './view_sequence.html', {'sequence': sequence})

def view_step(request, sequence_api_id, step_api_id, ref_id):
    r = requests.get(API_STEP_GUIDE.format(sequence_api_id, step_api_id, ref_id), verify = RSV)

    if r.status_code == 200:
        step = r.json()
        return render(request, './view_step.html', {'sequence_api_id': sequence_api_id, 'step': step})
    else:
        return HttpResponseRedirect(reverse('view-sequence', args=[sequence_api_id]))