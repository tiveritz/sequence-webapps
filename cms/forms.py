from django import forms


class EditSequence(forms.Form):
    sequence_title = forms.CharField(
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

class CreateSequence(forms.Form):
    sequence_title = forms.CharField(
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

class CreateCode(forms.Form):
    title = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'class': "input-text", 'autofocus' : "autofocus"}))

class EditExplanation(forms.Form):
    title = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'class': "input-text", 'autofocus' : "autofocus"}))
    content = forms.CharField(
        label='',
        max_length=2048,
        widget=forms.Textarea(attrs={'class': "input-explanation-text", 'autofocus' : "autofocus"}))

class EditCode(forms.Form):
    title = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'class': "input-text", 'autofocus' : "autofocus"}))
    content = forms.CharField(
        label='',
        max_length=2048,
        widget=forms.Textarea(attrs={'class': "input-explanation-text", 'autofocus' : "autofocus"}))

class UploadImage(forms.Form):
    image = forms.ImageField()