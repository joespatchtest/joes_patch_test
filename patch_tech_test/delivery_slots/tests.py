import datetime
import factory
import lxml
import lxml.html
import pytest

from django.urls import reverse

from delivery_slots.models import Slot


class SlotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'delivery_slots.Slot'


@pytest.fixture
def ten_days_of_slots():
    today = datetime.date.today()
    slots = []
    for d in range(10):
        date = today + datetime.timedelta(days=d)
        for tod, _ in Slot.TIME_OF_DAY_CHOICES:
            slots.append(
                SlotFactory(
                    date=date,
                    time_of_day=tod,
                    capacity=3,
                    unavailable=False,
                )
            )
    return slots


@pytest.mark.django_db
def test_homepage(client, ten_days_of_slots):
    r = client.get(reverse('home'))
    tree = lxml.html.fromstring(r.content)
    # Check we see thirty slots:
    slot_tds = tree.xpath("//td[contains(@class, 'slot')]")
    assert len(slot_tds) == 30


@pytest.mark.django_db
def test_schedule(client, ten_days_of_slots):
    slot = ten_days_of_slots[0]
    assert slot.capacity == 3
    r = client.get(
        reverse(
            'schedule_delivery',
            args=(slot.pk,)
        )
    )
    assert r.status_code == 302
    assert r['Location'] == reverse('home')
    slot.refresh_from_db()
    assert slot.capacity == 2
