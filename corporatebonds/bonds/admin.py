from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from .models import ListedCompany, ListedCompanyBond, Investor, InvestorBondBid

class InvestorForm(forms.ModelForm):
    class Meta:
        model = Investor
        fields = '__all__'  # Keep all fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['investor_wallet'].widget = forms.HiddenInput()  # Hide the original field

class InvestorAdmin(admin.ModelAdmin):
    form = InvestorForm  # Use the custom form
    list_display = ('investor_name', 'investor_wallet', 'id_passport', 'registration_date')
    readonly_fields = ('wallet_with_button',)

    def wallet_with_button(self, obj):
        """
        Custom field that includes a text box and a button to generate a Hedera Wallet Address.
        """
        wallet_value = obj.investor_wallet if obj.investor_wallet else ""  # Keep existing value
        return mark_safe(f"""
            <input type="text" id="wallet_address" name="investor_wallet" value="{wallet_value}" class="vTextField" readonly>
            <button type="button" class="button" onclick="generateHederaWallet()">Generate Wallet</button>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/web3/4.0.3/web3.min.js"></script>
            <script>
                async function generateHederaWallet() {{
                    try {{
                        const response = await fetch("https://testnet.mirrornode.hedera.com/api/v1/accounts", {{
                            method: "POST",
                            headers: {{ "Content-Type": "application/json" }},
                            body: JSON.stringify({{ "key": {{ "key": "ed25519" }} }})
                        }});
                        const data = await response.json();
                        document.getElementById("wallet_address").value = data.account || "Error generating wallet";
                    }} catch (error) {{
                        console.error("Wallet Generation Error:", error);
                        alert("Error generating wallet. Please try again.");
                    }}
                }}
            </script>
        """)

    wallet_with_button.short_description = "Investor Wallet Address"

    def save_model(self, request, obj, form, change):
        """
        Ensure the generated wallet address is saved when the form is submitted.
        """
        obj.investor_wallet = request.POST.get('investor_wallet', obj.investor_wallet)
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
