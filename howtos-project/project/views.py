from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
import requests
import json


API_URL = settings.API_URL
RSV = settings.REQUESTS_SSL_VERIFICATION
API_HOWTOS = API_URL + '/howtos/v1/howtos/'
API_HOWTO_GUIDE = API_URL + '/howtos/v1/guides/howto/{}/public/'
API_STEP_GUIDE = API_URL + '/howtos/v1/guides/howto/{}/{}/{}/'

#todo: remove duplicate function
def get_tree_as_nested_list(substeps):
    temp = []
    
    if not substeps:
        return ''
    
    for substep in substeps:
        temp.append(substep['title'])
        substeps = get_tree_as_nested_list(substep['substeps'])
        if substeps:
            temp.append(substeps)

    return temp


def home(request):
    return render(request, './home.html')

def viewer(request):
    r = requests.get(API_HOWTOS, verify = RSV)
    howtos = r.json()
    
    return render(request, './viewer.html', {'howtos' : howtos})

def view_howto(request, uri_id):
    r = requests.get(API_HOWTO_GUIDE.format(uri_id), verify = RSV)
    howto = r.json()

    return render(request, './view_howto.html', {'howto' : howto})

def view_step(request, howto_uri_id, step_uri_id, ref_id):
    r = requests.get(API_STEP_GUIDE.format(howto_uri_id, step_uri_id, ref_id), verify = RSV)

    if r.status_code == 200:
        step = r.json()
        return render(request, './view_step.html', {'howto_uri_id': howto_uri_id, 'step' : step})
    else:
        return HttpResponseRedirect(reverse('view-howto', args=[howto_uri_id]))