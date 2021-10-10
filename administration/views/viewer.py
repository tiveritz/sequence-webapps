from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import requests


API_URL = settings.API_URL
RSV = settings.REQUESTS_SSL_VERIFICATION
API_STEP_GUIDE = API_URL + '/howtos/v1/guides/howto/{}/{}/{}/'
API_HOWTO_GUIDE = API_URL + '/howtos/v1/guides/howto/{}/preview/'

def view_step_preview(request, id, step_uri_id, ref_id):
    r = requests.get(API_STEP_GUIDE.format(id, step_uri_id, ref_id), verify = RSV)

    if r.status_code == 200:
        step = r.json()
        html = render_to_string('./modules/render_step.html', {'howto_uri_id': id, 'step' : step})
        return HttpResponse(html)
    else:
        return HttpResponse(status=r.status_code)
    
def view_step_pre(request):
    pass  # Only used for url tag in templates

def view_howto_data(request, id):
    r = requests.get(API_HOWTO_GUIDE.format(id), verify = RSV)
    howto = r.json()

    return JsonResponse ({"howto": howto}, status = 200)
