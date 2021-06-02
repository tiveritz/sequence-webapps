from django.shortcuts import render
from django.conf import settings
import requests


API_URL = settings.API_URL
RSV = settings.REQUESTS_SSL_VERIFICATION
API_STATISTICS =      API_URL + '/hwts/v1/Statistics'


def dashboard(request):
    api_response = requests.get(API_STATISTICS, verify = RSV)
    statistics = api_response.json()

    return render(request, 'pages/dashboard.html', {
        'menu' : 'dashboard',
        'statistics' : statistics
        })

def information(request):
    return render(request, 'pages/information.html', {'menu' : 'information'})
