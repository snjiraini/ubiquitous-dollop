from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import InvestorLoginForm, BidForm
from .models import ListedCompanyBond, InvestorBondBid, Investor

def homepage(request):
    return render(request, 'homepage.html')

def investor_login(request):
    if request.method == "POST":
        form = InvestorLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('view_bonds')  # Redirect after login
    else:
        form = InvestorLoginForm()
    return render(request, "investor_login.html", {"form": form})

def view_bonds(request):
    bonds = ListedCompanyBond.objects.all()
    return render(request, "view_bonds.html", {"bonds": bonds})

@login_required
def place_bid(request, bond_id):
    bond = get_object_or_404(ListedCompanyBond, id=bond_id)
    investor = get_object_or_404(Investor, user=request.user)

    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            InvestorBondBid.objects.create(
                investor=investor,
                token=bond,
                bid_amount=form.cleaned_data["bid_amount"],
                bid_status="Pending"
            )
            return redirect("view_bonds")
    else:
        form = BidForm()

    return render(request, "place_bid.html", {"form": form, "bond": bond})