from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from .forms import InvestorLoginForm, InvestorBondBidForm
from .models import ListedCompanyBond, InvestorBondBid, Investor
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess
from .forms import InvestorForm, ListedCompanyBondForm

def is_investor_admin(user):
    return user.is_authenticated and user.groups.filter(name='investor-admin').exists()

@login_required
@user_passes_test(is_investor_admin)
def home(request):
    return render(request, 'home.html')

@login_required
# @user_passes_test(is_investor_admin)
def update_investor(request, investor_id):
    investor = get_object_or_404(Investor, id=investor_id)
    if request.method == "POST":
        form = InvestorForm(request.POST, instance=investor)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = InvestorForm(instance=investor)
    return render(request, 'update_investor.html', {'form': form})

@login_required
# @user_passes_test(is_investor_admin)
def update_bond(request, bond_id):
    bond = get_object_or_404(ListedCompanyBond, id=bond_id)
    if request.method == "POST":
        form = ListedCompanyBondForm(request.POST, instance=bond)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ListedCompanyBondForm(instance=bond)
    return render(request, 'update_bond.html', {'form': form})


def homepage(request):
    return render(request, 'homepage.html')

def investor_login(request):
    if request.method == "POST":
        form = InvestorLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('client_bid_page')  # Redirect after login
    else:
        form = InvestorLoginForm()
    return render(request, "investor_login.html", {"form": form})

@login_required
def view_bonds(request):
    bonds = ListedCompanyBond.objects.all()
    return render(request, "client_bid_page.html", {"bonds": bonds})

@login_required
def client_bid_page(request):
    # Fetch available bonds
    bonds = ListedCompanyBond.objects.all()
    
    # Fetch bids for the logged-in investor
    investor_bids = InvestorBondBid.objects.filter(investor=request.user.investor)

    if request.method == 'POST':
        form = InvestorBondBidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.investor = request.user.investor  # Assign logged-in investor
            bid.save()
            return redirect('client_bid_page')  # Refresh page after submission
    else:
        form = InvestorBondBidForm()

    return render(request, 'client_bid_page.html', {'form': form, 'investor_bids': investor_bids, 'bonds': bonds})

