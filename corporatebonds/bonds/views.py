from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import InvestorLoginForm, InvestorBondBidForm
from .models import ListedCompanyBond, InvestorBondBid, Investor



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

