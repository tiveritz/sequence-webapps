from django.shortcuts import render
from django.http import HttpResponse


def test(request):
    return HttpResponse("Hello World")

def dashboard(request):
	return render(request, 'pages/dashboard.html')
