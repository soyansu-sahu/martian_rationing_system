from datetime import date
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from .models import Inventory
from ration.forms import InventoryCreateForm
from django.views.generic import DeleteView,CreateView
from django.forms.models import model_to_dict
from ration.common_utils.util import ScheduleInventory
from django.db.models import Q


# Create your views here.
class InventoryList(View):
    def get(self,request):
        inventory = Inventory.objects.filter(Q(expiry_date__gte=date.today()) | Q(expiry_date__isnull=True)).all()
        input_inventory = []
        for inv in inventory:
            _inv = model_to_dict(inv)
            if _inv['expiry_date']:
                _inv['expiry_days'] = (_inv['expiry_date'] - date.today()).days
            else:
                _inv['expiry_days'] = None
            input_inventory.append(_inv)
        resp = ScheduleInventory(input_inventory)
       
        schedule_inventory = resp.getSchedule()
        return render(request,'ration/final_inventory.html', {'inventory':schedule_inventory})


class InventoryItemCreateView(CreateView):
    model  = Inventory
    template_name ='ration/ration_create_form.html'
    form_class  = InventoryCreateForm
    success_url = '/create/'        

    def get_context_data(self, **kwargs):
            ctx = super(InventoryItemCreateView, self).get_context_data(**kwargs)
            inventory = Inventory.objects.filter(Q(expiry_date__gte=date.today()) | Q(expiry_date__isnull=True)).all()
            ctx['inventory'] = [ model_to_dict(inv) for inv in inventory]
            return ctx


class InventoryDeleteView(DeleteView):
    success_url = "/create/"
    template_name = "ration/delete.html"
    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Inventory, id=id_)


