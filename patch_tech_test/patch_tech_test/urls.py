from django.contrib import admin
from django.urls import path

from delivery_slots.views import home, schedule_delivery


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path(
        'schedule-delivery/<int:slot__pk>/',
        schedule_delivery,
        name="schedule_delivery"
    ),
]
