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

admin.site.register(ListedCompany)
admin.site.register(ListedCompanyBond)
admin.site.register(Investor, InvestorAdmin)
admin.site.register(InvestorBondBid)
