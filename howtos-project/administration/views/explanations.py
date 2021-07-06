from django.shortcuts import redirect, render, reverse
from django.conf import settings
import requests
from django.http import HttpResponseRedirect
from ..forms import CreateText, EditExplanation


API_URL = settings.API_URL
RSV = settings.REQUESTS_SSL_VERIFICATION
API_EXPLANATION = API_URL + '/howtos/v1/explanation/'
API_EXPLANATION_EDIT = API_URL + '/howtos/v1/explanation/{}/'


def text(request):
    r = requests.get(API_EXPLANATION, verify = RSV)
    texts = r.json()

    return render(request, 'pages/modules_text.html', {
        'menu' : 'steps',
        'texts' : texts
        })

def text_create(request):
    if request.method == 'POST':
        form = CreateText(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            payload = {
                'type' : 'text',
                'title' : title,
            }

            r = requests.post(API_EXPLANATION, json = payload, verify = RSV)
            id = r.json()['uri_id']

            return HttpResponseRedirect(reverse('text'))#, args=[id]))

    form = CreateText()

    return render(request, 'pages/text_create.html', {'form': form})

def explanation_edit(request, id):
    if request.method == 'POST':
        form = EditExplanation(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            explanation = form.cleaned_data['content']
            url = API_EXPLANATION_EDIT.format(id)

            payload = {
                'title': title,
                'content': explanation,
                }
            requests.patch(url, json = payload, verify = RSV)

        return HttpResponseRedirect(reverse('explanation-edit', args=[id]))
    
    from ..functions.tree import get_tree_as_nested_list
        
    r = requests.get(API_EXPLANATION_EDIT.format(id), verify = RSV)
    explanation = r.json()
    form = EditExplanation(initial={
        'title': explanation['title'],
        'content': explanation['content'],
        })

    return render(request, 'pages/explanation_edit.html', {
        'menu' : 'text',
        'explanation' : explanation,
        'form' : form
        })

def code(request):
    r = requests.get(API_EXPLANATION, verify = RSV)
    codes = r.json()

    return render(request, 'pages/modules_code.html', {
        'menu' : 'steps',
        'codes' : codes
        })

def explanation_delete(request, id):
    r = requests.get(API_EXPLANATION_EDIT.format(id), verify = RSV)
    id = r.json()['uri_id']
    title = r.json()['title']
    
    return render(request, 'pages/explanation_delete.html',
        {'uri_id' : id,
         'title': title,
         })

def explanation_delete_confirm(request, id):
    url = API_EXPLANATION_EDIT.format(id)
    requests.delete(url, verify = RSV)
    print(id)

    return HttpResponseRedirect(reverse('text'))