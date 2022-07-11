from django.http.response import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
import requests
import json

from cms.base.utils import apply_positions
from cms.forms import EditStep, CreateStep
from cms.serializers import StepsSerializer, StepSerializer


API_URL = settings.API_URL
RSV = settings.REQUESTS_SSL_VERIFICATION
API_STEPS = API_URL + '/sequence/steps/'
API_STEP = API_URL + '/sequence/steps/{}/'
API_LINKED_STEPS_ORDER = API_URL + '/sequence/steps/{}/steps/order/'
API_LINKED_STEPS_DELETE = API_URL + '/sequence/steps/{}/steps/delete/'
API_STEP_LINKABLE = API_URL + '/sequence/steps/{}/linkable/'
API_STEP_LINK = API_URL + '/sequence/steps/{}/steps/link/'


def steps(request):
    if request.method == 'POST':
        form = CreateStep(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            r = requests.post(API_STEPS, json={'title': title}, verify=RSV)
            data = r.json()

            kwargs = {'uuid': data['uuid']}
            return HttpResponseRedirect(reverse('step', kwargs=kwargs))

    page = int(request.GET.get('page', 1))
    ordering = request.GET.get('ordering', '')

    params = {'page': page, 'ordering': ordering}
    r = requests.get(API_STEPS, verify=RSV, params=params)
    data = r.json()

    serializer = StepsSerializer(data)
    context = serializer.data

    context['site'] = 'steps'
    context['ordering'] = ordering

    form = CreateStep()
    context['form'] = form

    template_name = 'pages/steps.html'
    return render(request, template_name, context)


def step(request, uuid):
    if request.method == 'POST':
        form = EditStep(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            url = API_STEP.format(uuid)
            requests.patch(url, json={'title': title}, verify=RSV)

        return HttpResponseRedirect(reverse('step', args=[uuid]))

    r = requests.get(API_STEP.format(uuid), verify=RSV)
    data = r.json()

    serializer = StepSerializer(data)
    context = serializer.data

    apply_positions(context)

    form = EditStep(initial={'title': context['title']})
    context['form'] = form

    page = int(request.GET.get('page', 1))
    context['page'] = page

    ordering = request.GET.get('ordering', '')
    context['ordering'] = ordering

    template_name = 'pages/step.html'
    return render(request, template_name, context=context)


def step_delete(request, uuid):
    requests.delete(API_STEP.format(uuid), verify=RSV)
    return HttpResponseRedirect(reverse('steps'))


def delete_linked(request, uuid, sub):
    url = API_LINKED_STEPS_DELETE.format(uuid)
    payload = {'sub': str(sub)}
    r = requests.delete(url, json=payload, verify=RSV)

    return HttpResponseRedirect(reverse('step', args=[uuid]))


# AJAX
def linked_step_order(request, uuid):
    r_body = json.loads(request.body)
    from_index = r_body['from_index']
    to_index = r_body['to_index']

    url = API_LINKED_STEPS_ORDER.format(uuid)
    payload = {
        'from_index': from_index,
        'to_index': to_index
    }
    r = requests.post(url, json=payload, verify=RSV)

    if r.status_code == 200:
        return JsonResponse({'message': 'Saving order successful'})
    return r.status_code


def steps_filter(request):
    page = int(request.GET.get('page', 1))
    ordering = request.GET.get('ordering', '')

    params = {'page': page, 'ordering': ordering}
    r = requests.get(API_STEPS, verify=RSV, params=params)
    data = r.json()

    serializer = StepsSerializer(data)
    context = serializer.data

    context['site'] = 'steps'
    context['ordering'] = ordering

    form = CreateStep()
    context['form'] = form

    template_name = 'modules/step_list.html'

    html = render_to_string(template_name, context)
    return HttpResponse(html)


def step_linkable_filter(request, uuid):
    page = int(request.GET.get('page', 1))
    ordering = request.GET.get('ordering', '')

    params = {'page': page, 'ordering': ordering}
    r = requests.get(API_STEP_LINKABLE.format(uuid), verify=RSV, params=params)
    data = r.json()

    serializer = StepsSerializer(data)
    context = serializer.data

    context['page'] = page
    context['ordering'] = ordering
    context['type'] = 'linkable'

    template_name = 'modules/step_list.html'

    html = render_to_string(template_name, context)
    return HttpResponse(html)


def link_step(request, uuid):
    r_body = json.loads(request.body)
    sub = r_body['sub']

    url = API_STEP_LINK.format(uuid)
    payload = {'sub': sub}
    r = requests.post(url, json=payload, verify=RSV)

    if r.status_code == 201:
        return JsonResponse({'message': 'Linking step successful'})
    return r.status_code
