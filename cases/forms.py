from django import forms

class CurrentCaseForm(forms.Form):
    name = forms.CharField(max_length=255)
    hash_search = forms.CharField(max_length=255)