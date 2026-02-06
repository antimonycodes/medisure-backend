from django.contrib import admin
from .models import Manufacturer, Distributor, Pharmacy, Batch, Transaction

admin.site.register(Manufacturer)
admin.site.register(Distributor)
admin.site.register(Pharmacy)
admin.site.register(Batch)
admin.site.register(Transaction)