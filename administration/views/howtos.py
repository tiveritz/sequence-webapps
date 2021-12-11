from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.conf import settings
import requests
import json

from ..forms import EditHowTo, CreateHowTo
from ..functions.apptime import convert_datetime_api_to_app
from ..functions.tree import render_tree


API_URL = settings.API_URL
RSV = settings.REQUESTS_SSL_VERIFICATION
API_HOWTOS =          API_URL + '/howtos/v1/howtos/'
API_HOWTO =           API_URL + '/howtos/v1/howtos/{}/'
API_HOWTO_STEPS =     API_URL + '/howtos/v1/howtos/{}/steps/'
API_HOWTOS_LINKABLE = API_URL + '/howtos/v1/howtos/{}/linkable/'
API_HOWTOS_PUBLISH =  API_URL + '/howtos/v1/howtos/{}/publish/'

def howtos(request):
    current_page = 1
    if request.GET.get('page'):
        current_page = int(request.GET.get('page'))
    r = requests.get(API_HOWTOS, verify=RSV, params={'page': current_page})
    howtos = r.json()
    pages = int(howtos['count'])
    
    previous, next = 'null', 'null'
    
    if current_page != 1:
        previous = int(current_page) - 1

    if current_page < howtos['pages']:
        next = int(current_page) + 1
    
    paginator = {
        'count': howtos['count'],
        'pages': range(1, howtos['pages']+1),
        'current': current_page,
        'previous': previous,
        'next': next
    }

    for howto in howtos['results']:
        howto['created'] = convert_datetime_api_to_app(howto['created'])
        howto['updated'] = convert_datetime_api_to_app(howto['updated'])

    return render(request, 'pages/howtos.html', {
        'menu' : 'howtos',
        'paginator': paginator,
        'howtos' : howtos['results']
        })

def howtos_edit(request, id):
    if request.method == 'POST':
        form = EditHowTo(request.POST)
        if form.is_valid():
            howto_title = form.cleaned_data['howto_title']
            url = API_HOWTO.format(id)
            requests.patch(url, json = {'title': howto_title}, verify=RSV)

        return HttpResponseRedirect(reverse('howtos-edit', args=[id]))
        
    r = requests.get(API_HOWTO.format(id), verify=RSV)
    howto = r.json()
    form = EditHowTo(initial={'howto_title': howto['title']})

    if howto['is_published']:
        howto['publish_date'] = convert_datetime_api_to_app(howto['publish_date'])

    for step in howto['steps']:
        rendered = []
        rendered += (render_tree(step, parent=True))
        step['rendered_tree'] = ''.join(rendered)

    
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
            r = requests.post(API_HOWTOS, json = {'title': howto_title}, verify=RSV)
            id = r.json()['uri_id']

            return HttpResponseRedirect(reverse('howtos-edit', args=[id]))
    
    form = CreateHowTo()

    return render(request, 'pages/howtos_create.html', {'form': form})

def howtos_delete(request, id):
    r = requests.get(API_HOWTO.format(id), verify=RSV)
    id = r.json()['uri_id']
    title = r.json()['title']
    
    return render(request, 'pages/howtos_delete.html',
        {'uri_id' : id,
         'title': title,
         })

def howtos_delete_confirm(request, id):
    url = API_HOWTO.format(id)
    requests.delete(url, verify=RSV)

    return HttpResponseRedirect(reverse('howtos'))

def howtos_delete_step(request, id, step_id):
    url = API_HOWTO_STEPS.format(id)
    payload = {
        'method' : 'delete',
        'uri_id': step_id
    }
    r = requests.patch(url, json = payload, verify=RSV)

    return HttpResponseRedirect(reverse('howtos-edit', args=[id]))

def howtos_add_steps(request, id):
    r = requests.get(API_HOWTOS_LINKABLE.format(id), verify=RSV)
    steps = r.json()

    return render(request, 'pages/howtos_add_steps.html', {
        'uri_id' : id,
        'menu' : 'steps',
        'steps' : steps
        })

def howtos_add_steps_confirm(request, id, step_id):
    url = API_HOWTO_STEPS.format(id)
    r = requests.post(url, json = {'uri_id': step_id}, verify=RSV)

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
    r = requests.patch(url, json = payload, verify=RSV)
    
    if r.status_code == 200:
        return JsonResponse({'message' : 'Saving order successful'})
    return r.status_code

def howtos_publish(request, id):
    spaces = json.loads(request.body)
    url = API_HOWTOS_PUBLISH.format(id)
    r = requests.post(url, json=spaces, verify=RSV)
    data = r.json()

    data['publish_date'] = convert_datetime_api_to_app(data['publish_date'])

    if r.status_code == 200:
        return JsonResponse(
            {'is_published' : data['is_published'],
             'publish_date': data['publish_date'],
            })
    return r.status_code