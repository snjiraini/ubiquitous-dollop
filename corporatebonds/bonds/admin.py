from django.utils.html import format_html
from django.contrib import admin
from django.contrib.auth.models import User
from .models import ListedCompany, ListedCompanyBond, Investor, InvestorBondBid

class InvestorAdmin(admin.ModelAdmin):
    list_display = ('investor_name', 'investor_wallet', 'id_passport', 'user')

    def save_model(self, request, obj, form, change):
        if not obj.user:
            username = obj.investor_wallet  # Using wallet as username
            user = User.objects.create_user(username=username, password="defaultpassword")  # Change password logic later
            obj.user = user
        super().save_model(request, obj, form, change)

class ListedCompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'trading_symbol', 'industry', 'logo_preview')
    list_filter = ('industry',)
    search_fields = ('company_name', 'trading_symbol')

    def logo_preview(self, obj):
        if obj.company_logo:
            return format_html('<img src="{}" style="width:50px;height:50px;border-radius:5px;">', obj.company_logo.url)
        return "No Logo"

    logo_preview.short_description = 'Company Logo'

admin.site.register(ListedCompany, ListedCompanyAdmin)
admin.site.register(ListedCompanyBond)
admin.site.register(Investor, InvestorAdmin)
admin.site.register(InvestorBondBid)
