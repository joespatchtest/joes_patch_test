from django.contrib import admin

from delivery_slots.models import Slot


class SlotAdmin(admin.ModelAdmin):
    readonly_fields = ('date', 'time_of_day', )


admin.site.register(Slot, SlotAdmin)
