from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
import requests

from .forms import EditHowTo, EditStep


# API URLs
API_STATISTICS = 'https://api.tiveritz.at/hwts/v1/statistics'
API_HOWTOS = 'https://api.tiveritz.at/hwts/v1/howtos'
API_HOWTOS_EDIT = 'https://api.tiveritz.at/hwts/v1/howtos/{}'
API_STEPS = 'https://api.tiveritz.at/hwts/v1/steps'
API_STEPS_EDIT = 'https://api.tiveritz.at/hwts/v1/steps/{}'


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

    return render(request, 'pages/howtos.html',
    {
        'menu' : 'howtos',
        'howtos' : howtos
    })


def howtos_edit(request, uri_id):

    if request.method == 'POST':
        form = EditHowTo(request.POST)
        if form.is_valid():
            howto_title = form.cleaned_data['howto_title']
            # Make POST request to API
        return HttpResponseRedirect(reverse('howtos_edit', args=[uri_id]))
        
    else:
        r = requests.get(API_HOWTOS_EDIT.format(uri_id))
        howto = r.json()
        form = EditHowTo(initial={'howto_title': howto["title"]})

    return render(request, 'pages/howtos_edit.html', {
        'menu' : 'howtos',
        'howto' : howto,
        'form' : form
    })


def steps(request):
    r = requests.get(API_STEPS)
    steps = r.json()

    for step in steps:
        step['created'] = convert_api_time(step['created'])
        step['updated'] = convert_api_time(step['updated'])

    return render(request, 'pages/steps.html',
    {
        'menu' : 'steps',
        'steps' : steps
    })


def steps_edit(request, uri_id):

    if request.method == 'POST':
        form = EditStep(request.POST)
        if form.is_valid():
            step_title = form.cleaned_data['step_title']
            # Make POST request to API
        return HttpResponseRedirect(reverse('steps_edit', args=[uri_id]))
        
    else:
        r = requests.get(API_STEPS_EDIT.format(uri_id))
        step = r.json()
        form = EditStep(initial={'step_title': step["title"]})

    return render(request, 'pages/steps_edit.html', {
        'menu' : 'steps',
        'step' : step,
        'form' : form
    })


def information(request):
    return render(request, 'pages/information.html', {'menu' : 'information'})


# Helper functions
def convert_api_time(api_time):
    api_time_format = '%Y-%m-%dT%H:%M:%S+00:00'
    app_time_format = '%Y.%m.%d %H:%M'
    time = datetime.strptime(api_time, api_time_format)
    return time.strftime(app_time_format)