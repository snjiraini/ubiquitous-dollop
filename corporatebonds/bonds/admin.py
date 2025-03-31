from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.utils.safestring import mark_safe
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib import messages
from .models import ListedCompany, ListedCompanyBond, Investor, InvestorBondBid
from .forms import InvestorForm
from . import create_account
from . import create_token
import time  # Import time module for sleep
import traceback  # ✅ Import for detailed error logging

class InvestorAdmin(admin.ModelAdmin):
    form = InvestorForm
    list_display = ("investor_name", "user", "investor_wallet", "registration_date")
    search_fields = ("investor_name", "user__username", "id_passport", "investor_wallet")
    list_filter = ("registration_date",)
    readonly_fields = ("registration_date", "public_key", "private_key")

    def save_model(self, request, obj, form, change):
        new_account = False  # Flag to check if a new account was generated
        
        # Check if investor_wallet is empty or has 10 or fewer characters
        if not obj.investor_wallet or len(obj.investor_wallet) <= 10:
            try:
                account_data = create_account.generateHederaAccount()  # Generate Hedera account
                # time.sleep(10)  # ⏸ Pause for 10 seconds
                obj.investor_wallet = account_data.get("accountid")
                obj.public_key = account_data.get("publickey")
                obj.private_key = account_data.get("privatekey")
                new_account = True  # Set flag if a new account was generated

                if not obj.investor_wallet or not obj.public_key or not obj.private_key:
                    self.message_user(request, "Failed to generate Hedera account. Please try again.", level="error")
                    return  # Stop saving if keys are missing

            except Exception as e:
                print("❌ Error generating Hedera account:", str(e))  # ✅ Print error
                traceback.print_exc()  # ✅ Show full error traceback
                self.message_user(request, f"Error generating account: {str(e)}", level="error")
                return  # Stop save on error
        
        super().save_model(request, obj, form, change)  # ✅ Save only if generation is successful
        
        # ✅ Add the success message with the generated details
        if new_account:
            self.message_user(
                request,
                f"✅ Hedera Account Generated Successfully!\n"
                f"🔹 Account ID: {obj.investor_wallet}\n"
                f"🔹 Public Key: {obj.public_key}\n"
                f"🔹 Private Key: {obj.private_key}",
                level="success"
            )
        else:
            self.message_user(request, "Investor details updated successfully.", level="info")
    
    def response_change(self, request, obj):
        """
        Override the default success message when saving changes in Django Admin.
        """
        # No need to set the success message in session. It's handled directly in save_model.
        return super().response_change(request, obj)
    
class ListedCompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'trading_symbol', 'industry', 'logo_preview')
    list_filter = ('industry',)
    search_fields = ('company_name', 'trading_symbol')

    def logo_preview(self, obj):
        if obj.company_logo:
            return format_html('<img src="{}" style="width:50px;height:50px;border-radius:5px;">', obj.company_logo.url)
        return "No Logo"

    logo_preview.short_description = 'Company Logo'

class ListedCompanyBondAdmin(admin.ModelAdmin):
    list_display = ("token_name", "token_symbol", "initial_supply", "token_id")
    search_fields = ("token_name", "token_symbol")
    

    def save_model(self, request, obj, form, change):
        # Check if token_id is empty or has 10 or fewer characters
        if not obj.token_id or len(obj.token_id) <= 10:
            try:
                # Extract values from the form fields
                token_id = obj.token_id
                token_name = obj.token_name
                token_symbol = obj.token_symbol
                initial_supply = obj.initial_supply

                # Generate bond token on Hedera
                token_data = create_token.generateBondToken(token_name, token_symbol, initial_supply)
                # time.sleep(10)  # ⏸ Pause to ensure token creation completion

                # Assign values to the model
                obj.token_id = token_data.get("Tokenid")

                if not obj.token_id:
                    messages.error(request, "Failed to generate bond token. Please try again.")
                    return  # Stop saving if token creation failed

            except Exception as e:
                messages.error(request, f"Error generating bond token: {str(e)}")
                return  # Stop save on error

        super().save_model(request, obj, form, change)  # ✅ Save only if successful
        
        # ✅ Add a success message with the generated Token ID
        messages.success(
            request,
            f"✅ Bond Token Created Successfully!\n"
            f"🔹 Token Name: {obj.token_name}\n"
            f"🔹 Symbol: {obj.token_symbol}\n"
            f"🔹 Initial Supply: {obj.initial_supply}\n"
            f"🔹 Token ID: {obj.token_id}"
        )

admin.site.register(ListedCompany, ListedCompanyAdmin)
admin.site.register(ListedCompanyBond,ListedCompanyBondAdmin)
admin.site.register(Investor, InvestorAdmin)
admin.site.register(InvestorBondBid)
