from django.db import models

# Create your models here.
class Inventory(models.Model):
    PACKET_CHOICES = (
        ("FOOD", "food"),
        ("WATER", "water"),
    )
    packet_type = models.CharField(choices=PACKET_CHOICES, default=PACKET_CHOICES[0][0], max_length=10 ,blank=True,null=True)
    packet_content = models.CharField(max_length=100,blank=True,null=True)
    calories = models.IntegerField(blank=True,null=True)
    expiry_date = models.DateField(blank=True,null=True)
    water_quantity_litres = models.PositiveIntegerField(blank=True,null=True)














