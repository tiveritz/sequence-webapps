import requests

from django.conf import settings
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, ListView

from cms.base.utils import apply_positions
from cms.forms import CreateStep, EditStep
from cms.serializers import StepSerializer, StepsSerializer


RSV = settings.REQUESTS_SSL_VERIFICATION


class StepListView(CreateView):
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

        template_name = 'pages/steps.html'
        return render(request, template_name, context)

    def post(self, request):
        form = CreateStep(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            r = requests.post(self.API_STEPS,
                              json={'title': title},
                              verify=RSV)
            data = r.json()

            kwargs = {'uuid': data['uuid']}
            return HttpResponseRedirect(reverse('step', kwargs=kwargs))


class StepView(CreateView):
    API_STEP = settings.API_URL + '/sequence/steps/{}/'

    def get(self, request, uuid):
        r = requests.get(self.API_STEP.format(uuid), verify=RSV)
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

    def post(self, request, uuid):
        form = EditStep(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            url = self.API_STEP.format(uuid)
            requests.patch(url, json={'title': title}, verify=RSV)

        return HttpResponseRedirect(reverse('step', args=[uuid]))


class StepDeleteView(ListView):
    API_STEP = settings.API_URL + '/sequence/steps/{}/'

    def get(self, request, uuid):
        requests.delete(self.API_STEP.format(uuid), verify=RSV)
        return HttpResponseRedirect(reverse('steps'))


class StepDeleteLinkedView(ListView):
    API_LINKED_STEPS_DELETE = settings.API_URL \
        + '/sequence/steps/{}/steps/delete/'

    def get(self, request, uuid, sub):
        url = self.API_LINKED_STEPS_DELETE.format(uuid)
        payload = {'sub': str(sub)}
        requests.delete(url, json=payload, verify=RSV)

        return HttpResponseRedirect(reverse('step', args=[uuid]))
