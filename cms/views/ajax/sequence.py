import requests

from django.conf import settings
from django.http.response import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import ListView

from cms.forms import CreateSequence
from cms.serializers import SequencesSerializer


RSV = settings.REQUESTS_SSL_VERIFICATION


class SequenceListFilterView(ListView):
    API_SEQUENCES = settings.API_URL + '/sequence/sequences/'

    def get(self, request):
        page = int(request.GET.get('page', 1))
        ordering = request.GET.get('ordering', '')

        params = {'page': page, 'ordering': ordering}
        r = requests.get(self.API_SEQUENCES, verify=RSV, params=params)
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
