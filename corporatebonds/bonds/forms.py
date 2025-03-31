from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import InvestorBondBid, Investor,ListedCompanyBond

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

class InvestorForm(forms.ModelForm):
    class Meta:
        model = Investor
        fields = ["user", "investor_name", "id_passport", "investor_wallet", "public_key", "private_key"]


class ListedCompanyBondForm(forms.ModelForm):
    class Meta:
        model = ListedCompanyBond
        fields = [
            'token_name', 'token_symbol', 'initial_supply', 'treasury_account',
            'max_supply', 'issue_date', 'maturity_date', 'coupon', 'coupon_frequency',
            'ISINCode', 'bond_purpose', 'outstanding_amount'
        ]
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'maturity_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'coupon': forms.NumberInput(attrs={'class': 'form-control'}),
            'initial_supply': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_supply': forms.NumberInput(attrs={'class': 'form-control'}),
            'outstanding_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'bond_purpose': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
