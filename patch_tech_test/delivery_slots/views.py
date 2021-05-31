import datetime

from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Slot


def home(request):
    """Show a user a list of available (and unavailable) delivery slots"""
    first_day = datetime.date.today()
    if not Slot.objects.filter(
        date=first_day,
        capacity__gt=0,
    ).exists():
        # No available slots on first day, so start on next day as per spec
        first_day += datetime.timedelta(days=1)

    # Get the next four weeks of slots:
    slots = Slot.objects.filter(
        date__gte=first_day,
        date__lte=first_day + datetime.timedelta(days=27)
    )

    return render(
        request,
        template_name='delivery_slots.html',
        context={
            'slots': slots,
        }
    )


def schedule_delivery(request, slot__pk):
    """Schedule a delivery in the specified time slot"""
    redirect = HttpResponseRedirect(reverse('home'))
    with transaction.atomic():
        slot = Slot.objects.select_for_update().get(pk=slot__pk)
        if slot.is_full():
            messages.add_message(
                request, messages.ERROR,
                "Sorry, we were not able to schedule a delivery in that slot. Please try again."
            )
            return redirect
        slot.capacity -= 1
        slot.save()
    messages.add_message(
        request, messages.INFO,
        f"Thank you for scheduling a delivery on {slot}. If you wish you can schedule another below."
    )
    return redirect
