from django.http.response import JsonResponse
from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
import requests
import json

from ..functions.apptime import convert_datetime_api_to_app
from ..functions.tree import render_tree, get_substep_tree_as_nested_list, get_decision_tree_as_nested_list
from ..forms import EditStep, CreateStep


API_URL = settings.API_URL
RSV = settings.REQUESTS_SSL_VERIFICATION
API_STEPS =  API_URL + '/howtos/v1/steps/'
API_STEP = API_URL + '/howtos/v1/steps/{}/'
API_SUPER_STEPS =  API_URL + '/howtos/v1/steps/{}/steps/'
API_DECISION_STEPS =  API_URL + '/howtos/v1/steps/{}/decisions/'
API_MODULES = API_URL + '/howtos/v1/steps/{}/modules/'
API_DECISIONS = API_URL + '/howtos/v1/steps/{}/decisions/'
API_STEPS_LINKABLE = API_URL + '/howtos/v1/steps/{}/linkable/'
API_DECISIONS_LINKABLE = API_URL + '/howtos/v1/steps/{}/linkable-decisions/'
API_MODULES_LINKABLE = API_URL + '/howtos/v1/steps/{}/linkablemodules/'
API_IMAGES_LINKABLE = API_URL + '/howtos/v1/steps/{}/linkableimages/'

def steps(request):
    current_page = 1
    if request.GET.get('page'):
        current_page = int(request.GET.get('page'))
    r = requests.get(API_STEPS, verify=RSV, params={'page': current_page})
    steps = r.json()
    
    previous, next = 'null', 'null'
    
    if current_page != 1:
        previous = int(current_page) - 1

    if current_page < steps['pages']:
        next = int(current_page) + 1
    
    paginator = {
        'count': steps['count'],
        'pages': range(1, steps['pages']+1),
        'current': current_page,
        'previous': previous,
        'next': next
    }

    steps = r.json()

    for step in steps['results']:
        step['created'] = convert_datetime_api_to_app(step['created'])
        step['updated'] = convert_datetime_api_to_app(step['updated'])

    return render(request, 'pages/steps.html', {
        'menu' : 'steps',
        'paginator': paginator,
        'steps' : steps['results']
        })

def supersteps(request):
    r = requests.get(API_STEPS, verify = RSV)
    steps = r.json()

    for step in steps['results']:
        step['created'] = convert_datetime_api_to_app(step['created'])
        step['updated'] = convert_datetime_api_to_app(step['updated'])

    return render(request, 'pages/supersteps.html', {
        'menu' : 'supersteps',
        'steps' : steps['results']
        })

def substeps(request):
    r = requests.get(API_STEPS, verify = RSV)
    steps = r.json()

    for step in steps['results']:
        step['created'] = convert_datetime_api_to_app(step['created'])
        step['updated'] = convert_datetime_api_to_app(step['updated'])

    return render(request, 'pages/substeps.html', {
        'menu' : 'substeps',
        'steps' : steps['results']
        })


def steps_edit(request, id):
    if request.method == 'POST':
        form = EditStep(request.POST)
        if form.is_valid():
            step_title = form.cleaned_data['step_title']
            url = API_STEP.format(id)
            requests.patch(url, json = {'title': step_title}, verify = RSV)

        return HttpResponseRedirect(reverse('steps-edit', args=[id]))

    r = requests.get(API_STEP.format(id), verify = RSV)
    step = r.json()
    form = EditStep(initial={'step_title': step['title']})
  
    for substeps in step['substeps']:
        rendered = []
        rendered += (render_tree(substeps, parent=True))
        substeps['rendered_tree'] = ''.join(rendered)
        
    for decisionsteps in step['decisionsteps']:
        rendered = []
        rendered += (render_tree(decisionsteps, parent=True))
        decisionsteps['rendered_tree'] = ''.join(rendered)  
  
    for substep in step['substeps']:
        substep['decisionsteps'] = get_decision_tree_as_nested_list(substep['decisionsteps'])
        substep['substeps'] = get_substep_tree_as_nested_list(substep['substeps'])
    for decisionstep in step['decisionsteps']:
        decisionstep['decisionsteps'] = get_decision_tree_as_nested_list(decisionstep['decisionsteps'])
        decisionstep['substeps'] = get_substep_tree_as_nested_list(decisionstep['substeps'])

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
            id = r.json()['uri_id']

            return HttpResponseRedirect(reverse('steps-edit', args=[id]))
    
    form = CreateStep()

    return render(request, 'pages/steps_create.html', {'form': form})

def steps_delete(request, id):
    r = requests.get(API_STEP.format(id), verify = RSV)
    id = r.json()['uri_id']
    title = r.json()['title']
    
    return render(request, 'pages/steps_delete.html',
        {'uri_id' : id,
         'title': title,
         })

def steps_delete_confirm(request, id):
    url = API_STEP.format(id)
    requests.delete(url, verify = RSV)

    return HttpResponseRedirect(reverse('steps'))

def supersteps_delete(request, id):
    r = requests.get(API_STEP.format(id), verify = RSV)
    id = r.json()['uri_id']
    title = r.json()['title']
    
    return render(request, 'pages/supersteps_delete.html',
        {'uri_id' : id,
         'title': title,
         })

def supersteps_delete_confirm(request, id):
    url = API_STEP.format(id)
    requests.delete(url, verify = RSV)

    return HttpResponseRedirect(reverse('supersteps'))

def substeps_delete(request, id):
    r = requests.get(API_STEP.format(id), verify = RSV)
    id = r.json()['uri_id']
    title = r.json()['title']
    
    return render(request, 'pages/steps_delete.html',
        {'uri_id' : id,
         'title': title,
         })

def substeps_delete_confirm(request, id):
    url = API_STEP.format(id)
    requests.delete(url, verify = RSV)

    return HttpResponseRedirect(reverse('substeps'))

def steps_delete_step(request, id, step_id):
    url = API_SUPER_STEPS.format(id)
    payload = {
        'method' : 'delete',
        'uri_id': step_id
    }
    r = requests.patch(url, json = payload, verify = RSV)

    return HttpResponseRedirect(reverse('steps-edit', args=[id]))

def steps_delete_decision(request, id, step_id):
    url = API_DECISION_STEPS.format(id)
    payload = {
        'method' : 'delete',
        'uri_id': step_id
    }
    r = requests.patch(url, json = payload, verify = RSV)

    return HttpResponseRedirect(reverse('steps-edit', args=[id]))

def steps_add_steps(request, id):
    r = requests.get(API_STEPS_LINKABLE.format(id), verify = RSV)
    steps = r.json()

    for step in steps:
        step['substeps'] = render_tree(step['substeps'])

    return render(request, 'pages/steps_add_steps.html', {
        'uri_id' : id,
        'menu' : 'steps',
        'steps' : steps
        })

def steps_add_steps_confirm(request, id, step_id):
    url = API_SUPER_STEPS.format(id)
    r = requests.post(url, json = {'uri_id': step_id}, verify = RSV)

    return HttpResponseRedirect(reverse(steps_add_steps, args=[id]))

def steps_add_decisions(request, id):
    r = requests.get(API_DECISIONS_LINKABLE.format(id), verify = RSV)
    steps = r.json()

    for step in steps:
        step['substeps'] = render_tree(step['substeps'])

    return render(request, 'pages/steps_add_decisions.html', {
        'uri_id' : id,
        'menu' : 'steps',
        'steps' : steps
        })

def steps_add_decisions_confirm(request, id, step_id):
    url = API_DECISION_STEPS.format(id)
    r = requests.post(url, json = {'uri_id': step_id}, verify = RSV)

    return HttpResponseRedirect(reverse(steps_add_decisions, args=[id]))

def steps_delete_module(request, id, explanation_id):
    url = API_MODULES.format(id)
    payload = {
        'method' : 'delete',
        'uri_id': explanation_id
    }
    r = requests.patch(url, json = payload, verify = RSV)

    return HttpResponseRedirect(reverse('steps-edit', args=[id]))

def steps_add_textmodule(request, id):
    r = requests.get(API_MODULES_LINKABLE.format(id), verify = RSV)
    texts = r.json()
    texts = [text for text in texts if text['type'] == 'text']

    return render(request, 'pages/steps_add_textmodule.html', {
        'uri_id' : id,
        'menu' : 'steps',
        'texts' : texts
        })

def steps_add_textmodule_confirm(request, id, explanation_id):
    url = API_MODULES.format(id)
    payload = {
        'type': 'explanation',
        'uri_id': explanation_id,
        }
    r = requests.post(url, json = payload, verify = RSV)

    return HttpResponseRedirect(reverse(steps_add_textmodule, args=[id]))

def steps_add_codemodule(request, id):
    r = requests.get(API_MODULES_LINKABLE.format(id), verify = RSV)
    codes = r.json()
    codes = [code for code in codes if code['type'] == 'code']

    return render(request, 'pages/steps_add_codemodule.html', {
        'uri_id' : id,
        'menu' : 'steps',
        'codes' : codes,
        })

def steps_add_codemodule_confirm(request, id, code_id):
    url = API_MODULES.format(id)
    payload = {
        'type': 'explanation',
        'uri_id': code_id,
        }
    r = requests.post(url, json = payload, verify = RSV)

    return HttpResponseRedirect(reverse(steps_add_codemodule, args=[id]))

def steps_add_image(request, id):
    r = requests.get(API_IMAGES_LINKABLE.format(id), verify = RSV)
    images = r.json()

    return render(request, 'pages/steps_add_image.html', {
        'uri_id' : id,
        'menu' : 'steps',
        'images' : images,
        })

def steps_add_image_confirm(request, id, image_id):
    url = API_MODULES.format(id)
    payload = {
        'type': 'image',
        'uri_id': image_id,
        }
    r = requests.post(url, json = payload, verify = RSV)

    return HttpResponseRedirect(reverse(steps_add_image, args=[id]))

# AJAX
def save_step_order(request, id):
    r_body = json.loads(request.body)
    old_index = r_body['old_index']
    new_index = r_body['new_index']

    url = API_SUPER_STEPS.format(id)
    payload = {
        'method' : 'order',
        'old_index': old_index,
        'new_index' : new_index
        }
    r = requests.patch(url, json = payload,
        verify = RSV)

    if r.status_code == 200:
        return JsonResponse({'message' : 'Saving order successful'})
    return r.status_code

def save_explanation_order(request, id):
    r_body = json.loads(request.body)
    old_index = r_body['old_index']
    new_index = r_body['new_index']

    url = API_MODULES.format(id)
    payload = {
        'method' : 'order',
        'old_index': old_index,
        'new_index' : new_index
        }
    r = requests.patch(url, json = payload,
        verify = RSV)

    if r.status_code == 200:
        return JsonResponse({'message' : 'Saving order successful'})
    return r.status_code


def save_decision_order(request, id):
    r_body = json.loads(request.body)
    old_index = r_body['old_index']
    new_index = r_body['new_index']

    url = API_DECISIONS.format(id)
    payload = {
        'method' : 'order',
        'old_index': old_index,
        'new_index' : new_index
        }
    r = requests.patch(url, json = payload,
        verify = RSV)

    if r.status_code == 200:
        return JsonResponse({'message' : 'Saving order successful'})
    return r.status_code