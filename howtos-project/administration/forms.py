from django import forms


class EditHowTo(forms.Form):
    howto_title = forms.CharField(
        initial='',
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'class': "input-text"}))

class EditStep(forms.Form):
    step_title = forms.CharField(
        initial='',
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'class': "input-text"}))

class CreateHowTo(forms.Form):
    howto_title = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'class': "input-text", 'autofocus' : "autofocus"}))
    
class CreateStep(forms.Form):
    step_title = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'class': "input-text", 'autofocus' : "autofocus"}))

class CreateText(forms.Form):
    title = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'class': "input-text", 'autofocus' : "autofocus"}))

class EditText(forms.Form):
    title = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'class': "input-text", 'autofocus' : "autofocus"}))
    content = forms.CharField(
        label='',
        max_length=2048,
        widget=forms.TextInput(attrs={'class': "input-text", 'autofocus' : "autofocus"}))