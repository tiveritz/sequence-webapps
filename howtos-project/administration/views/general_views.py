from django.shortcuts import redirect, render, reverse
from django.conf import settings
import requests


API_URL = settings.API_URL
RSV = settings.REQUESTS_SSL_VERIFICATION
API_STATISTICS = API_URL + '/howtos/v1/statistics/'

def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))
    return redirect('login/')

def logout(request):
    return redirect('logout/')

def dashboard(request):
    r = requests.get(API_STATISTICS, verify = RSV)
    print(r)
    statistics = r.json()

    return render(request, 'pages/dashboard.html', {
        'menu' : 'dashboard',
        'statistics' : statistics
        })

def information(request):
    return render(request, 'pages/information.html', {'menu' : 'information'})
