import requests

from django.conf import settings
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, ListView

from cms.base.utils import apply_positions
from cms.forms import EditSequence, CreateSequence
from cms.serializers import StepSerializer, SequencesSerializer


RSV = settings.REQUESTS_SSL_VERIFICATION


class SequenceListView(CreateView):
    API_SEQUENCES = settings.API_URL + '/sequence/sequences/'

    def get(self, request):
        page = int(request.GET.get('page', 1))
        ordering = request.GET.get('ordering', '')

        params = {'page': page, 'ordering': ordering}
        r = requests.get(self.API_SEQUENCES, verify=RSV, params=params)
        data = r.json()

        serializer = SequencesSerializer(data)
        context = serializer.data

        context['site'] = 'sequences'
        context['ordering'] = ordering

        form = CreateSequence()
        context['form'] = form

        template_name = 'pages/sequences.html'
        return render(request, template_name, context)

    def post(self, request):
        form = CreateSequence(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            r = requests.post(self.API_SEQUENCES, json={
                              'title': title}, verify=RSV)
            data = r.json()

            kwargs = {'uuid': data['uuid']}
            return HttpResponseRedirect(reverse('sequence', kwargs=kwargs))


class SequenceView(CreateView):
    API_SEQUENCE = settings.API_URL + '/sequence/sequences/{}/'

    def get(self, request, uuid):
        r = requests.get(self.API_SEQUENCE.format(uuid), verify=RSV)
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

    def post(self, request, uuid):
        form = EditSequence(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            url = self.API_SEQUENCE.format(uuid)
            requests.patch(url, json={'title': title}, verify=RSV)

        return HttpResponseRedirect(reverse('sequence', args=[uuid]))


class SequenceDeleteView(ListView):
    API_SEQUENCE = settings.API_URL + '/sequence/sequences/{}/'

    def get(self, request, uuid):
        requests.delete(self.API_SEQUENCE.format(uuid), verify=RSV)
        return HttpResponseRedirect(reverse('sequences'))


class SequenceDeleteLinkedView(ListView):
    API_LINKED_STEPS_DELETE = settings.API_URL \
        + '/sequence/steps/{}/steps/delete/'

    def get(self, request, uuid, super, sub):
        # this is +- duplicate with steps -> refactor!
        url = self.API_LINKED_STEPS_DELETE.format(super)
        payload = {'sub': str(sub)}
        requests.delete(url, json=payload, verify=RSV)

        return HttpResponseRedirect(reverse('sequence', args=[uuid]))
