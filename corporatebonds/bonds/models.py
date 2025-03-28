from django.db import models
from django.contrib.auth.models import User

class ListedCompany(models.Model):
    INDUSTRY_CHOICES = [
        ('Agriculture', 'Agriculture'),
        ('Automobiles & Accessories', 'Automobiles & Accessories'),
        ('Banking', 'Banking'),
        ('Commercial & Services', 'Commercial & Services'),
        ('Construction & Allied', 'Construction & Allied'),
        ('Energy & Petroleum', 'Energy & Petroleum'),
        ('Insurance', 'Insurance'),
        ('Investment', 'Investment'),
        ('Investment Services', 'Investment Services'),
        ('Manufacturing & Allied', 'Manufacturing & Allied'),
        ('Telecommunication & Technology', 'Telecommunication & Technology'),
        ('Real Estate Investment Trust', 'Real Estate Investment Trust'),
        ('Exchange Traded Fund', 'Exchange Traded Fund'),
    ]

    ISINCode = models.CharField(max_length=20, unique=True)
    company_name = models.CharField(max_length=255)
    trading_symbol = models.CharField(max_length=20, unique=True)
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES, default='Banking')
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)  # Upload to 'media/company_logos/'

    def __str__(self):
        return f"{self.company_name} ({self.trading_symbol})"


class ListedCompanyBond(models.Model):
    token_name = models.CharField(max_length=255, unique=True)
    token_symbol = models.CharField(max_length=10, unique=True)
    initial_supply = models.DecimalField(max_digits=20, decimal_places=2)
    treasure_account = models.CharField(max_length=255)
    max_supply = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    issue_date = models.DateField()
    maturity_date = models.DateField()
    coupon = models.DecimalField(max_digits=5, decimal_places=2)
    coupon_frequency = models.CharField(
        max_length=50,
        choices=[('Annual', 'Annual'), ('Semi-Annual', 'Semi-Annual'), ('Quarterly', 'Quarterly'), ('Monthly', 'Monthly')]
    )
    ISINCode = models.ForeignKey(ListedCompany, on_delete=models.CASCADE, to_field='ISINCode')
    bond_purpose = models.TextField()
    outstanding_amount = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"{self.token_name} ({self.token_symbol})"


class Investor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Links to Django's User model
    investor_wallet = models.CharField(max_length=255, unique=True)
    investor_name = models.CharField(max_length=255)
    id_passport = models.CharField(max_length=50, unique=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.investor_name} ({self.user.username})"


class InvestorBondBid(models.Model):
    BID_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected')
    ]

    bid_id = models.AutoField(primary_key=True)
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    token = models.ForeignKey(ListedCompanyBond, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=20, decimal_places=2)
    bid_status = models.CharField(max_length=20, choices=BID_STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Bid {self.bid_id} - {self.investor.user.username} for {self.token.token_name}"
