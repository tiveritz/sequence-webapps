import json

import requests

from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.views.generic import CreateView, ListView

from cms.forms import CreateStep
from cms.serializers import StepsSerializer


RSV = settings.REQUESTS_SSL_VERIFICATION


class StepLinkedOrderView(CreateView):
    API_LINKED_STEPS_ORDER = settings.API_URL \
        + '/sequence/steps/{}/steps/order/'

    def post(self, request, uuid):
        r_body = json.loads(request.body)
        from_index = r_body['from_index']
        to_index = r_body['to_index']

        url = self.API_LINKED_STEPS_ORDER.format(uuid)
        payload = {
            'from_index': from_index,
            'to_index': to_index
        }
        r = requests.post(url, json=payload, verify=RSV)

        if r.status_code == 200:
            return JsonResponse({'message': 'Saving order successful'})
        return r.status_code


class LinkStepView(CreateView):
    API_STEP_LINK = settings.API_URL + '/sequence/steps/{}/steps/link/'

    def post(self, request, uuid):
        r_body = json.loads(request.body)
        sub = r_body['sub']

        url = self.API_STEP_LINK.format(uuid)
        payload = {'sub': sub}
        r = requests.post(url, json=payload, verify=RSV)

        if r.status_code == 201:
            return JsonResponse({'message': 'Linking step successful'})
        return r.status_code


class StepListFilterView(ListView):
    API_STEPS = settings.API_URL + '/sequence/steps/'

    def get(self, request):
        page = int(request.GET.get('page', 1))
        ordering = request.GET.get('ordering', '')

        params = {'page': page, 'ordering': ordering}
        r = requests.get(self.API_STEPS, verify=RSV, params=params)
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


class StepLinkableListFilterView(ListView):
    API_STEP_LINKABLE = settings.API_URL + '/sequence/steps/{}/linkable/'

    def get(self, request, uuid):
        page = int(request.GET.get('page', 1))
        ordering = request.GET.get('ordering', '')

        params = {'page': page, 'ordering': ordering}
        r = requests.get(self.API_STEP_LINKABLE.format(
            uuid), verify=RSV, params=params)
        data = r.json()

        serializer = StepsSerializer(data)
        context = serializer.data

        context['page'] = page
        context['ordering'] = ordering
        context['type'] = 'linkable'

        template_name = 'modules/step_list.html'

        html = render_to_string(template_name, context)
        return HttpResponse(html)
