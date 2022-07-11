from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
import requests
import json

from cms.base.utils import apply_positions
from cms.forms import EditSequence, CreateSequence
from cms.serializers import StepSerializer, SequencesSerializer


API_URL = settings.API_URL
RSV = settings.REQUESTS_SSL_VERIFICATION
API_SEQUENCES = API_URL + '/sequence/sequences/'
API_SEQUENCE = API_URL + '/sequence/sequences/{}/'
API_LINKED_STEPS_DELETE = API_URL + '/sequence/steps/{}/steps/delete/'


def sequences(request):
    if request.method == 'POST':
        form = CreateSequence(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            r = requests.post(API_SEQUENCES, json={'title': title}, verify=RSV)
            data = r.json()

            kwargs = {'uuid': data['uuid']}
            return HttpResponseRedirect(reverse('sequence', kwargs=kwargs))

    page = int(request.GET.get('page', 1))
    ordering = request.GET.get('ordering', '')

    params = {'page': page, 'ordering': ordering}
    r = requests.get(API_SEQUENCES, verify=RSV, params=params)
    data = r.json()

    serializer = SequencesSerializer(data)
    context = serializer.data

    context['site'] = 'sequences'
    context['ordering'] = ordering

    form = CreateSequence()
    context['form'] = form

    template_name = 'pages/sequences.html'
    return render(request, template_name, context)


def sequence(request, uuid):
    if request.method == 'POST':
        form = EditSequence(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            url = API_SEQUENCE.format(uuid)
            requests.patch(url, json={'title': title}, verify=RSV)

        return HttpResponseRedirect(reverse('sequence', args=[uuid]))

    r = requests.get(API_SEQUENCE.format(uuid), verify=RSV)
    data = r.json()

    serializer = StepSerializer(data)
    context = serializer.data

    apply_positions(context)

    form = EditSequence(initial={'title': context['title']})
    context['form'] = form

    page = int(request.GET.get('page', 1))
    context['page'] = page

    ordering = request.GET.get('ordering', '')
    context['ordering'] = ordering

    template_name = 'pages/sequence.html'
    return render(request, template_name, context=context)


def sequence_delete(request, uuid):
    requests.delete(API_SEQUENCE.format(uuid), verify=RSV)
    return HttpResponseRedirect(reverse('sequences'))


def delete_linked(request, uuid, super, sub):
    # this is +- duplicate with steps -> refactor!
    url = API_LINKED_STEPS_DELETE.format(super)
    payload = {
        'sub': str(sub),
    }
    r = requests.delete(url, json=payload, verify=RSV)

    return HttpResponseRedirect(reverse('sequence', args=[uuid]))


# AJAX
def sequences_filter(request):
    page = int(request.GET.get('page', 1))
    ordering = request.GET.get('ordering', '')

    params = {'page': page, 'ordering': ordering}
    r = requests.get(API_SEQUENCES, verify=RSV, params=params)
    data = r.json()

    serializer = SequencesSerializer(data)
    context = serializer.data

    context['site'] = 'steps'
    context['ordering'] = ordering

    form = CreateSequence()
    context['form'] = form

    template_name = 'modules/sequence_list.html'

    html = render_to_string(template_name, context)
    return HttpResponse(html)
