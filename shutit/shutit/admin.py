from django.contrib import admin

from .models import Passenger, Queue

class PassengerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Passenger, PassengerAdmin)

class QueueAdmin(admin.ModelAdmin):
    pass

admin.site.register(Queue, QueueAdmin)