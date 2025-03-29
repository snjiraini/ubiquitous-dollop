from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import InvestorBondBid

class InvestorLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class InvestorBondBidForm(forms.ModelForm):
    class Meta:
        model = InvestorBondBid
        fields = ['token', 'bid_amount']
        widgets = {
            'bid_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter bid amount'}),
            'token': forms.Select(attrs={'class': 'form-control'}),
        }