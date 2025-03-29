from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

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

    ISINCode = models.CharField(max_length=12, unique=True, verbose_name="ISIN Code")
    company_name = models.CharField(max_length=255, verbose_name="Company Name")
    trading_symbol = models.CharField(max_length=20, unique=True, db_index=True, verbose_name="Trading Symbol")
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES, default='Banking', verbose_name="Industry")
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True, verbose_name="Company Logo")

    class Meta:
        verbose_name = "Listed Company"
        verbose_name_plural = "Listed Companies"

    def __str__(self):
        return f"{self.company_name} ({self.trading_symbol})"


class ListedCompanyBond(models.Model):
    token_name = models.CharField(max_length=255, unique=True, verbose_name="Token Name")
    token_symbol = models.CharField(max_length=10, unique=True, verbose_name="Token Symbol")
    initial_supply = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Initial Supply")
    treasure_account = models.CharField(max_length=255, verbose_name="Treasury Account")
    max_supply = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name="Max Supply")
    issue_date = models.DateField(verbose_name="Issue Date")
    maturity_date = models.DateField(verbose_name="Maturity Date")
    coupon = models.DecimalField(
        max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="Coupon Rate (%)"
    )
    coupon_frequency = models.CharField(
        max_length=50,
        choices=[('Annual', 'Annual'), ('Semi-Annual', 'Semi-Annual'), ('Quarterly', 'Quarterly'), ('Monthly', 'Monthly')],
        verbose_name="Coupon Frequency"
    )
    ISINCode = models.ForeignKey(ListedCompany, on_delete=models.CASCADE, related_name="bonds", to_field='ISINCode', verbose_name="ISIN Code")
    bond_purpose = models.TextField(verbose_name="Bond Purpose")
    outstanding_amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Outstanding Amount")

    class Meta:
        verbose_name = "Listed Company Bond"
        verbose_name_plural = "Listed Company Bonds"

    def clean(self):
        """Ensure outstanding amount does not exceed max supply."""
        if self.max_supply and self.outstanding_amount > self.max_supply:
            raise ValueError("Outstanding amount cannot exceed max supply.")

    def __str__(self):
        return f"{self.token_name} ({self.token_symbol}) - {self.ISINCode.company_name}"


class Investor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="User")
    investor_wallet = models.CharField(max_length=255, unique=True, verbose_name="Investor Wallet Address")
    investor_name = models.CharField(max_length=255, verbose_name="Investor Name")
    id_passport = models.CharField(max_length=50, unique=True, verbose_name="ID/Passport Number")
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="Registration Date")

    class Meta:
        verbose_name = "Investor"
        verbose_name_plural = "Investors"

    def __str__(self):
        return f"{self.investor_name} ({self.user.username})"


class InvestorBondBid(models.Model):
    BID_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected')
    ]

    bid_id = models.AutoField(primary_key=True, verbose_name="Bid ID")
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE, related_name="bids", verbose_name="Investor")
    token = models.ForeignKey(ListedCompanyBond, on_delete=models.CASCADE, related_name="bids", verbose_name="Token")
    bid_amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Bid Amount")
    bid_status = models.CharField(max_length=20, choices=BID_STATUS_CHOICES, default='Pending', verbose_name="Bid Status")

    class Meta:
        verbose_name = "Investor Bond Bid"
        verbose_name_plural = "Investor Bond Bids"

    def __str__(self):
        return f"Bid {self.bid_id} - {self.investor.user.username} for {self.token.token_name}"
