from django.http.response import JsonResponse
from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
import requests
import json

from .forms import EditHowTo, CreateHowTo, EditStep, CreateStep


# API URLs
API_STATISTICS = 'https://api.tiveritz.at/hwts/v1/statistics'
API_HOWTOS = 'https://api.tiveritz.at/hwts/v1/howtos'
API_HOWTO = 'https://api.tiveritz.at/hwts/v1/howtos/{}'
API_HOWTO_STEPS = 'https://api.tiveritz.at/hwts/v1/howtos/{}/steps'
API_HOWTOS_LINKABLE = 'https://api.tiveritz.at/hwts/v1/howtos/{}/linkable'

API_STEPS = 'https://api.tiveritz.at/hwts/v1/steps'
API_STEP = 'https://api.tiveritz.at/hwts/v1/steps/{}'
API_SUPER_STEPS = 'https://api.tiveritz.at/hwts/v1/steps/{}/steps'
API_STEPS_LINKABLE = 'https://api.tiveritz.at/hwts/v1/steps/{}/linkable'


def dashboard(request):
    api_response = requests.get(API_STATISTICS)
    statistics = api_response.json()

    return render(request, 'pages/dashboard.html', {
        'menu' : 'dashboard',
        'statistics' : statistics
        })


def howtos(request):
    r = requests.get(API_HOWTOS)
    howtos = r.json()

    for howto in howtos:
        howto['created'] = convert_api_time(howto['created'])
        howto['updated'] = convert_api_time(howto['updated'])

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
            requests.patch(url, json = {'title': howto_title})

        return HttpResponseRedirect(reverse('howtos_edit', args=[id]))
        
    r = requests.get(API_HOWTO.format(id))
    howto = r.json()
    form = EditHowTo(initial={'howto_title': howto['title']})
    
    for step in howto['steps']:
        step['substeps'] = get_simple_nested_list(step['substeps'])

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
            r = requests.post(API_HOWTOS, json = {'title': howto_title})
            id = r.json()['id']

            return HttpResponseRedirect(reverse('howtos_edit', args=[id]))
    
    form = CreateHowTo()

    return render(request, 'pages/howtos_create.html', {'form': form})

def howtos_delete(request, id):
    r = requests.get(API_HOWTO.format(id))
    id = r.json()['id']
    title = r.json()['title']
    
    return render(request, 'pages/howtos_delete.html',
        {'id' : id,
         'title': title,
         })

def howtos_delete_confirm(request, id):
    url = API_HOWTO.format(id)
    requests.delete(url)

    return HttpResponseRedirect(reverse('howtos'))

def howtos_delete_step(request, id, step_id):
    url = API_HOWTO_STEPS.format(id)
    r = requests.delete(url, json = {'id': step_id})

    return HttpResponseRedirect(reverse('howtos_edit', args=[id]))

def howtos_add_steps(request, id):
    r = requests.get(API_HOWTOS_LINKABLE.format(id))
    steps = r.json()

    for step in steps:
        step['created'] = convert_api_time(step['created'])
        step['updated'] = convert_api_time(step['updated'])

    return render(request, 'pages/howtos_add_steps.html', {
        'id' : id,
        'menu' : 'steps',
        'steps' : steps
        })

def howtos_add_steps_confirm(request, id, step_id):
    url = API_HOWTO_STEPS.format(id)
    r = requests.post(url, json = {'id': step_id})

    return HttpResponseRedirect(reverse(howtos_add_steps, args=[id]))


def steps(request):
    r = requests.get(API_STEPS)
    steps = r.json()

    for step in steps:
        step['created'] = convert_api_time(step['created'])
        step['updated'] = convert_api_time(step['updated'])

    return render(request, 'pages/steps.html', {
        'menu' : 'steps',
        'steps' : steps
        })

def supersteps(request):
    r = requests.get(API_STEPS)
    steps = r.json()

    for step in steps:
        step['created'] = convert_api_time(step['created'])
        step['updated'] = convert_api_time(step['updated'])

    return render(request, 'pages/supersteps.html', {
        'menu' : 'steps',
        'steps' : steps
        })

def substeps(request):
    r = requests.get(API_STEPS)
    steps = r.json()

    for step in steps:
        step['created'] = convert_api_time(step['created'])
        step['updated'] = convert_api_time(step['updated'])

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
            requests.patch(url, json = {'title': step_title})

        return HttpResponseRedirect(reverse('steps_edit', args=[id]))

    r = requests.get(API_STEP.format(id))
    step = r.json()
    form = EditStep(initial={'step_title': step['title']})
    
    for substep in step['steps']:
        substep['substeps'] = get_simple_nested_list(substep['substeps'])

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
            r = requests.post(API_STEPS, json = {'title': step_title})
            id = r.json()['id']

            return HttpResponseRedirect(reverse('steps_edit', args=[id]))
    
    form = CreateStep()

    return render(request, 'pages/steps_create.html', {'form': form})

def steps_delete(request, id):
    r = requests.get(API_STEP.format(id))
    id = r.json()['id']
    title = r.json()['title']
    
    return render(request, 'pages/steps_delete.html',
        {'id' : id,
         'title': title,
         })

def steps_delete_confirm(request, id):
    url = API_STEP.format(id)
    requests.delete(url)
    print(id)

    return HttpResponseRedirect(reverse('steps'))

def supersteps_delete(request, id):
    r = requests.get(API_STEP.format(id))
    id = r.json()['id']
    title = r.json()['title']
    
    return render(request, 'pages/supersteps_delete.html',
        {'id' : id,
         'title': title,
         })

def supersteps_delete_confirm(request, id):
    url = API_STEP.format(id)
    requests.delete(url)

    return HttpResponseRedirect(reverse('supersteps'))

def substeps_delete(request, id):
    r = requests.get(API_STEP.format(id))
    id = r.json()['id']
    title = r.json()['title']
    
    return render(request, 'pages/steps_delete.html',
        {'id' : id,
         'title': title,
         })

def substeps_delete_confirm(request, id):
    url = API_STEP.format(id)
    requests.delete(url)

    return HttpResponseRedirect(reverse('substeps'))

def steps_delete_step(request, id, step_id):
    url = API_SUPER_STEPS.format(id)
    r = requests.delete(url, json = {'id': step_id})

    return HttpResponseRedirect(reverse('steps_edit', args=[id]))

def information(request):
    return render(request, 'pages/information.html', {'menu' : 'information'})

def steps_add_steps(request, id):
    r = requests.get(API_STEPS_LINKABLE.format(id))
    steps = r.json()

    for step in steps:
        step['created'] = convert_api_time(step['created'])
        step['updated'] = convert_api_time(step['updated'])

    return render(request, 'pages/steps_add_steps.html', {
        'id' : id,
        'menu' : 'steps',
        'steps' : steps
        })

def steps_add_steps_confirm(request, id, step_id):
    url = API_SUPER_STEPS.format(id)
    r = requests.post(url, json = {'id': step_id})

    return HttpResponseRedirect(reverse(steps_add_steps, args=[id]))

# AJAX
def save_howto_order(request, id):
    r_body = json.loads(request.body)
    old_index = r_body['old_index']
    new_index = r_body['new_index']

    url = API_HOWTO_STEPS.format(id)
    r = requests.patch(url, json = {
        'oldIndex': old_index,
        'newIndex' : new_index})

    return JsonResponse({'message' : 'Saving order successful'})

def save_step_order(request, id):
    r_body = json.loads(request.body)
    old_index = r_body['old_index']
    new_index = r_body['new_index']

    url = API_SUPER_STEPS.format(id)
    r = requests.patch(url, json = {
        'oldIndex': old_index,
        'newIndex' : new_index})

    return JsonResponse({'message' : 'Saving order successful'})

# Helper functions
def convert_api_time(api_time):
    api_time_format = '%Y-%m-%dT%H:%M:%S+00:00'
    app_time_format = '%d.%m.%Y %H:%M'
    time = datetime.strptime(api_time, api_time_format)
    return time.strftime(app_time_format)

def get_simple_nested_list(substeps):
    temp = []
    
    if not substeps:
        return ''
    
    for substep in substeps:
        temp.append(substep['title'])
        substeps = get_simple_nested_list(substep['substeps'])
        if substeps:
            temp.append(substeps)

    return temp
