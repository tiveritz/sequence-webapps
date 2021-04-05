from django import forms


class EditHowTo(forms.Form):
    howto_title = forms.CharField(
        initial='',
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'class': "input-text"}))