from django import forms
from .models import Inventory

class InventoryCreateForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields =('packet_type','packet_content','calories','expiry_date','water_quantity_litres')