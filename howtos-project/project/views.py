from django.shortcuts import render
from django.conf import settings
import requests
import json


API_URL = settings.API_URL
RSV = settings.REQUESTS_SSL_VERIFICATION
API_HOWTOS =          API_URL + '/howtos/v1/howtos/'
API_HOWTO =           API_URL + '/howtos/v1/howtos/{}/'

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

def render_howto(request, uri_id):
    r = requests.get(API_HOWTO.format(uri_id), verify = RSV)
    howto = r.json()
    
    for step in howto['steps']:
        step['substeps'] = get_tree_as_nested_list(step['substeps'])

    return render(request, './render_howto.html', {'howto' : howto})