from django.contrib import admin
from ration.models import Inventory

# Register your models here.
@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ( 'packet_type', 'packet_content', 'calories','expiry_date','water_quantity_litres')

