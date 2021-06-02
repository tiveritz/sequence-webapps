from django.http.response import JsonResponse
from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
import requests
import json

from ..forms import EditStep, CreateStep


API_URL = settings.API_URL
RSV = settings.REQUESTS_SSL_VERIFICATION
API_STEPS =           API_URL + '/hwts/v1/steps'
API_STEP =            API_URL + '/hwts/v1/steps/{}'
API_SUPER_STEPS =     API_URL + '/hwts/v1/steps/{}/steps'
API_STEPS_LINKABLE =  API_URL + '/hwts/v1/steps/{}/linkable'

def steps(request):
    from ..functions.apptime import convert_datetime_api_to_app
    r = requests.get(API_STEPS, verify = RSV)
    steps = r.json()

    for step in steps:
        step['created'] = convert_datetime_api_to_app(step['created'])
        step['updated'] = convert_datetime_api_to_app(step['updated'])

    return render(request, 'pages/steps.html', {
        'menu' : 'steps',
        'steps' : steps
        })

def supersteps(request):
    r = requests.get(API_STEPS, verify = RSV)
    steps = r.json()

    for step in steps:
        from ..functions.apptime import convert_datetime_api_to_app
        step['created'] = convert_datetime_api_to_app(step['created'])
        step['updated'] = convert_datetime_api_to_app(step['updated'])

    return render(request, 'pages/supersteps.html', {
        'menu' : 'steps',
        'steps' : steps
        })

def substeps(request):
    from ..functions.apptime import convert_datetime_api_to_app
    r = requests.get(API_STEPS, verify = RSV)
    steps = r.json()

    for step in steps:
        step['created'] = convert_datetime_api_to_app(step['created'])
        step['updated'] = convert_datetime_api_to_app(step['updated'])

    return render(request, 'pages/substeps.html', {
        'menu' : 'steps',
        'steps' : steps
        })


def steps_edit(request, id):
    if request.method == 'POST':
        form = EditStep(request.POST)
        if form.is_valid():
            step_title = form.cleaned_data['step_title']
            url = API_STEP.format(id)
            requests.patch(url, json = {'title': step_title}, verify = RSV)

        return HttpResponseRedirect(reverse('steps_edit', args=[id]))
    
    from ..functions.tree import get_tree_as_nested_list

    r = requests.get(API_STEP.format(id), verify = RSV)
    step = r.json()
    form = EditStep(initial={'step_title': step['title']})
    
    for substep in step['steps']:
        substep['substeps'] = get_tree_as_nested_list(substep['substeps'])

    return render(request, 'pages/steps_edit.html', {
        'menu' : 'steps',
        'step' : step,
        'form' : form
        })

def steps_create(request):
    if request.method == 'POST':
        form = CreateStep(request.POST)
        if form.is_valid():
            step_title = form.cleaned_data['step_title']
            r = requests.post(API_STEPS, json = {'title': step_title}, verify = RSV)
            id = r.json()['id']

            return HttpResponseRedirect(reverse('steps_edit', args=[id]))
    
    form = CreateStep()

    return render(request, 'pages/steps_create.html', {'form': form})

def steps_delete(request, id):
    r = requests.get(API_STEP.format(id), verify = RSV)
    id = r.json()['id']
    title = r.json()['title']
    
    return render(request, 'pages/steps_delete.html',
        {'id' : id,
         'title': title,
         })

def steps_delete_confirm(request, id):
    url = API_STEP.format(id)
    requests.delete(url, verify = RSV)
    print(id)

    return HttpResponseRedirect(reverse('steps'))

def supersteps_delete(request, id):
    r = requests.get(API_STEP.format(id), verify = RSV)
    id = r.json()['id']
    title = r.json()['title']
    
    return render(request, 'pages/supersteps_delete.html',
        {'id' : id,
         'title': title,
         })

def supersteps_delete_confirm(request, id):
    url = API_STEP.format(id)
    requests.delete(url, verify = RSV)

    return HttpResponseRedirect(reverse('supersteps'))

def substeps_delete(request, id):
    r = requests.get(API_STEP.format(id), verify = RSV)
    id = r.json()['id']
    title = r.json()['title']
    
    return render(request, 'pages/steps_delete.html',
        {'id' : id,
         'title': title,
         })

def substeps_delete_confirm(request, id):
    url = API_STEP.format(id)
    requests.delete(url, verify = RSV)

    return HttpResponseRedirect(reverse('substeps'))

def steps_delete_step(request, id, step_id):
    url = API_SUPER_STEPS.format(id)
    r = requests.delete(url, json = {'id': step_id}, verify = RSV)

    return HttpResponseRedirect(reverse('steps_edit', args=[id]))

def steps_add_steps(request, id):
    from ..functions.apptime import convert_datetime_api_to_app
    r = requests.get(API_STEPS_LINKABLE.format(id), verify = RSV)
    steps = r.json()

    for step in steps:
        step['created'] = convert_datetime_api_to_app(step['created'])
        step['updated'] = convert_datetime_api_to_app(step['updated'])

    return render(request, 'pages/steps_add_steps.html', {
        'id' : id,
        'menu' : 'steps',
        'steps' : steps
        })

def steps_add_steps_confirm(request, id, step_id):
    url = API_SUPER_STEPS.format(id)
    r = requests.post(url, json = {'id': step_id}, verify = RSV)

    return HttpResponseRedirect(reverse(steps_add_steps, args=[id]))


def save_step_order(request, id):
    r_body = json.loads(request.body)
    old_index = r_body['old_index']
    new_index = r_body['new_index']

    url = API_SUPER_STEPS.format(id)
    r = requests.patch(url, json = {
        'oldIndex': old_index,
        'newIndex' : new_index},
        verify = RSV)

    if r.status_code == 200:
        return JsonResponse({'message' : 'Saving order successful'})
    return r.status_code
