from django import forms
from base.models import CurrentCase, UserInventory


class CurrentCaseForm(forms.Form):
    name = forms.CharField(max_length=255)
    hash_search = forms.CharField(max_length=255)



class UserInventoryForm(forms.ModelForm):
    buy_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control form-control-lg'}),
        required=True,
        label="Buy Date"
    )

    class Meta:
        model = UserInventory
        fields = ['case_bought', 'ammount', 'buy_price', 'buy_date']
        widgets = {
            'case_bought': forms.Select(attrs={'class': 'form-control form-control-lg'}),
            'ammount': forms.NumberInput(attrs={'class': 'form-control form-control-lg'}),
            'buy_price': forms.NumberInput(attrs={'class': 'form-control form-control-lg'}),
        }