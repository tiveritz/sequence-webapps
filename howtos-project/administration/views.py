from django.shortcuts import render
from django.http import HttpResponse
import requests
from datetime import datetime


def dashboard(request):
	return render(request, 'pages/dashboard.html', {'menu' : 'dashboard'})

def howtos(request):
	response = requests.get('https://api.tiveritz.at/hwts/v1/howtos')
	howtos = response.json()

	for howto in howtos:
		howto['created'] = convert_api_time(howto['created'])
		howto['updated'] = convert_api_time(howto['updated'])

	return render(request, 'pages/howtos.html',
	{
		'menu' : 'howtos',
		'howtos' : howtos
	})

def howtos_edit(request, uri_id):
	response = requests.get('https://api.tiveritz.at/hwts/v1/howtos/' + uri_id)
	howto = response.json()

	return render(request, 'pages/howtos_edit.html', {
		'menu' : 'howtos',
		'howto' : howto
	})

def information(request):
	return render(request, 'pages/information.html', {'menu' : 'information'})


# Helper functions
def convert_api_time(api_time):
	api_time_format = '%Y-%m-%dT%H:%M:%S+00:00'
	app_time_format = '%Y.%m.%d %H:%M'
	time = datetime.strptime(api_time, api_time_format)
	return time.strftime(app_time_format)