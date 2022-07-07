from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
import requests
import json

from cms.forms import EditSequence, CreateSequence

from cms.serializers import SequenceSerializer, SequencesSerializer


API_URL = settings.API_URL
RSV = settings.REQUESTS_SSL_VERIFICATION
API_SEQUENCES = API_URL + '/sequence/sequences/'
API_SEQUENCE = API_URL + '/sequence/sequences/{}/'

def sequences(request):
    page = int(request.GET.get('page', 1))
    ordering = request.GET.get('ordering')
    
    params = {'page': page, 'ordering': ordering}
    r = requests.get(API_SEQUENCES, verify=RSV, params=params)
    data = r.json()
    
    serializer = SequencesSerializer(data)
    context = serializer.data
    
    context['site'] = 'sequences'
    context['ordering'] = ordering

    template_name = 'pages/sequences.html'
    return render(request, template_name, context)


def sequence(request, uuid):
    if request.method == 'POST':
        form = EditSequence(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            url = API_SEQUENCE.format(uuid)
            requests.patch(url, json = {'title': title}, verify=RSV)

        return HttpResponseRedirect(reverse('sequence', args=[uuid]))
        
    r = requests.get(API_SEQUENCE.format(uuid), verify=RSV)
    data = r.json()
    
    serializer = SequenceSerializer(data)
    context = serializer.data

    form = EditSequence(initial={'title': context['title']})
    context['form'] = form
    
    template_name = 'pages/sequence.html'
    return render(request, template_name, context=context)


'''
API_SEQUENCE =           API_URL + '/sequence/sequences/{}/'
API_SEQUENCE_STEPS =     API_URL + '/sequence/sequences/{}/steps/'
API_SEQUENCE_LINKABLE =  API_URL + '/sequence/sequences/{}/linkable/'
API_SEQUENCE_PUBLISH =   API_URL + '/sequence/sequences/{}/publish/'

def sequences_edit(request, id):
    if request.method == 'POST':
        form = EditSequence(request.POST)
        if form.is_valid():
            sequence_title = form.cleaned_data['sequence_title']
            url = API_SEQUENCE.format(id)
            requests.patch(url, json = {'title': sequence_title}, verify=RSV)

        return HttpResponseRedirect(reverse('sequences-edit', args=[id]))
        
    r = requests.get(API_SEQUENCE.format(id), verify=RSV)
    sequence = r.json()
    form = EditSequence(initial={'sequence_title': sequence['title']})

    if sequence['is_published']:
        sequence['publish_date'] = convert_datetime_api_to_app(sequence['publish_date'])

    for step in sequence['steps']:
        rendered = []
        rendered += (render_tree(step, parent=True))
        step['rendered_tree'] = ''.join(rendered)

    
    return render(request, 'pages/sequences_edit.html', {
        'menu' : 'sequences',
        'sequence' : sequence,
        'form' : form
        })

def sequences_create(request):
    if request.method == 'POST':
        form = CreateSequence(request.POST)
        if form.is_valid():
            sequence_title = form.cleaned_data['sequence_title']
            r = requests.post(API_SEQUENCES, json = {'title': sequence_title}, verify=RSV)
            id = r.json()['api_id']

            return HttpResponseRedirect(reverse('sequences-edit', args=[id]))
    
    form = CreateSequence()

    return render(request, 'pages/sequences_create.html', {'form': form})

def sequence_delete(request, id):
    r = requests.get(API_SEQUENCE.format(id), verify=RSV)
    id = r.json()['api_id']
    title = r.json()['title']
    
    return render(request, 'pages/sequences_delete.html',
        {'api_id' : id,
         'title': title,
         })

def sequence_delete_confirm(request, id):
    url = API_SEQUENCE.format(id)
    requests.delete(url, verify=RSV)

    return HttpResponseRedirect(reverse('sequences'))

def sequence_delete_step(request, id, step_id):
    url = API_SEQUENCE_STEPS.format(id)
    payload = {
        'method' : 'delete',
        'api_id': step_id
    }
    r = requests.patch(url, json = payload, verify=RSV)

    return HttpResponseRedirect(reverse('sequences-edit', args=[id]))

def sequence_add_steps(request, id):
    r = requests.get(API_SEQUENCE_LINKABLE.format(id), verify=RSV)
    steps = r.json()

    return render(request, 'pages/sequences_add_steps.html', {
        'api_id' : id,
        'menu' : 'steps',
        'steps' : steps
        })

def sequence_add_steps_confirm(request, id, step_id):
    url = API_SEQUENCE_STEPS.format(id)
    r = requests.post(url, json = {'api_id': step_id}, verify=RSV)

    return HttpResponseRedirect(reverse(sequence_add_steps, args=[id]))

# AJAX
def save_sequence_order(request, id):
    r_body = json.loads(request.body)
    old_index = r_body['old_index']
    new_index = r_body['new_index']

    url = API_SEQUENCE_STEPS.format(id)
    payload = {
        'method' : 'order',
        'old_index': old_index,
        'new_index' : new_index
        }
    r = requests.patch(url, json = payload, verify=RSV)
    
    if r.status_code == 200:
        return JsonResponse({'message' : 'Saving order successful'})
    return r.status_code

def sequence_publish(request, id):
    spaces = json.loads(request.body)
    url = API_SEQUENCE_PUBLISH.format(id)
    r = requests.post(url, json=spaces, verify=RSV)
    data = r.json()

    data['publish_date'] = convert_datetime_api_to_app(data['publish_date'])

    if r.status_code == 200:
        return JsonResponse(
            {'is_published' : data['is_published'],
             'publish_date': data['publish_date'],
            })
    return r.status_code
'''
