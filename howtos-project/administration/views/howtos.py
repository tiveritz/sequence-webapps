from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
import requests
import json

from ..forms import EditHowTo, CreateHowTo
from ..functions.apptime import convert_datetime_api_to_app
from ..functions.tree import get_tree_as_nested_list


API_URL = settings.API_URL
RSV = settings.REQUESTS_SSL_VERIFICATION
API_HOWTOS =          API_URL + '/howtos/v1/howtos/'
API_HOWTO =           API_URL + '/howtos/v1/howtos/{}/'
API_HOWTO_STEPS =     API_URL + '/howtos/v1/howtos/{}/steps/'
API_HOWTOS_LINKABLE = API_URL + '/howtos/v1/howtos/{}/linkable/'

def howtos(request):
    r = requests.get(API_HOWTOS, verify = RSV)
    howtos = r.json()

    for howto in howtos:
        howto['created'] = convert_datetime_api_to_app(howto['created'])
        howto['updated'] = convert_datetime_api_to_app(howto['updated'])

    return render(request, 'pages/howtos.html', {
        'menu' : 'howtos',
        'howtos' : howtos
        })


def howtos_edit(request, id):
    if request.method == 'POST':
        form = EditHowTo(request.POST)
        if form.is_valid():
            howto_title = form.cleaned_data['howto_title']
            url = API_HOWTO.format(id)
            requests.patch(url, json = {'title': howto_title}, verify = RSV)

        return HttpResponseRedirect(reverse('howtos-edit', args=[id]))
        
    r = requests.get(API_HOWTO.format(id), verify = RSV)
    howto = r.json()
    form = EditHowTo(initial={'howto_title': howto['title']})
    
    for step in howto['steps']:
        step['substeps'] = get_tree_as_nested_list(step['substeps'])

    return render(request, 'pages/howtos_edit.html', {
        'menu' : 'howtos',
        'howto' : howto,
        'form' : form
        })

def howtos_create(request):
    if request.method == 'POST':
        form = CreateHowTo(request.POST)
        if form.is_valid():
            howto_title = form.cleaned_data['howto_title']
            r = requests.post(API_HOWTOS, json = {'title': howto_title}, verify = RSV)
            id = r.json()['uri_id']

            return HttpResponseRedirect(reverse('howtos-edit', args=[id]))
    
    form = CreateHowTo()

    return render(request, 'pages/howtos_create.html', {'form': form})

def howtos_delete(request, id):
    r = requests.get(API_HOWTO.format(id), verify = RSV)
    id = r.json()['uri_id']
    title = r.json()['title']
    
    return render(request, 'pages/howtos_delete.html',
        {'uri_id' : id,
         'title': title,
         })

def howtos_delete_confirm(request, id):
    url = API_HOWTO.format(id)
    requests.delete(url, verify = RSV)

    return HttpResponseRedirect(reverse('howtos'))

def howtos_delete_step(request, id, step_id):
    url = API_HOWTO_STEPS.format(id)
    payload = {
        'method' : 'delete',
        'uri_id': step_id
    }
    r = requests.patch(url, json = payload, verify = RSV)

    return HttpResponseRedirect(reverse('howtos-edit', args=[id]))

def howtos_add_steps(request, id):
    r = requests.get(API_HOWTOS_LINKABLE.format(id), verify = RSV)
    steps = r.json()

    return render(request, 'pages/howtos_add_steps.html', {
        'uri_id' : id,
        'menu' : 'steps',
        'steps' : steps
        })

def howtos_add_steps_confirm(request, id, step_id):
    url = API_HOWTO_STEPS.format(id)
    r = requests.post(url, json = {'uri_id': step_id}, verify = RSV)

    return HttpResponseRedirect(reverse(howtos_add_steps, args=[id]))

# AJAX
def save_howto_order(request, id):
    r_body = json.loads(request.body)
    old_index = r_body['old_index']
    new_index = r_body['new_index']

    url = API_HOWTO_STEPS.format(id)
    payload = {
        'method' : 'order',
        'old_index': old_index,
        'new_index' : new_index
        }
    r = requests.patch(url, json = payload, verify = RSV)
    
    if r.status_code == 200:
        return JsonResponse({'message' : 'Saving order successful'})
    return r.status_code
