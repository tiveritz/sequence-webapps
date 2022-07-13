from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import requests


API_URL = settings.API_URL
RSV = settings.REQUESTS_SSL_VERIFICATION
API_STEP_GUIDE = API_URL + '/sequence/guides/sequence/{}/'
API_SEQUENCE_GUIDE = API_URL + '/sequence/guides/sequence/{}/preview/'

def view_step_preview(request, step_api_id):
    r = requests.get(API_STEP_GUIDE.format(step_api_id), verify = RSV)

    if r.status_code == 200:
        step = r.json()
        if step['decision_steps']:
            step['decision_steps'] = step['decision_steps'].split(',')
        html = render_to_string('./modules/render_step.html', {'sequence_api_id': id, 'step' : step})
        return HttpResponse(html)
    else:
        return HttpResponse(status=r.status_code)
    
def view_step_pre(request):
    pass  # Only used for url tag in templates

def view_sequence_data(request, id):
    r = requests.get(API_SEQUENCE_GUIDE.format(id), verify = RSV)
    sequence = r.json()

    return JsonResponse ({"sequence": sequence}, status = 200)
