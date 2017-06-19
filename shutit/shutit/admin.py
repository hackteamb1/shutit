from django.contrib import admin

from .models import _Passenger as Passenger
from .models import _Queue as Queue

class PassengerAdmin(admin.ModelAdmin):
    pass

class QueueAdmin(admin.ModelAdmin):
    pass


admin.site.register(Passenger, PassengerAdmin)
admin.site.register(Queue, QueueAdmin)