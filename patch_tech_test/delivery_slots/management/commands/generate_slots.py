import datetime

from django.core.management.base import BaseCommand

from delivery_slots.models import Slot


class Command(BaseCommand):
    help = 'Creates delivery slots for the next four weeks'

    def add_arguments(self, parser):
        parser.add_argument('--num-days', nargs='?', type=int, default=28)
        parser.add_argument('--slot-capacity', nargs='?', type=int, default=4)
        parser.add_argument('--wednesdays-unavailable', nargs='?', type=bool, const=True, default=False)

    def handle(self, *args, **options):
        num_days = options['num_days']
        slot_capacity = options['slot_capacity']
        wednesdays_unavailable = options['wednesdays_unavailable']
        self.stdout.write(
            self.style.NOTICE(
                f"Creating delivery slots with a capacity of {slot_capacity} "
                f"for the next {num_days} days"
            )
        )
        start_date = datetime.date.today()
        # Pick an arbitrary Friday in the recent-ish past:
        first_ever_friday = datetime.date(2020, 1, 3)

        for day in range(0, num_days):
            date = start_date + datetime.timedelta(days=day)
            days_since_first_ever_friday = (date - first_ever_friday).days
            for tod, _ in Slot.TIME_OF_DAY_CHOICES:
                # Make unavailable if the "wednesdays-unavailable" switch is
                # provided by the user and date is a wednesday,
                # OR
                # if it's a morning slot falling on every other Friday
                unavailable = (
                    (wednesdays_unavailable and date.isoweekday() == 3) or
                    (tod == 'AM' and not (days_since_first_ever_friday % 14))
                )
                defaults={
                    'capacity': slot_capacity,
                    'unavailable': unavailable,
                }
                Slot.objects.get_or_create(
                    date=date,
                    time_of_day=tod,
                    defaults=defaults,
                )
        self.stdout.write(
            self.style.SUCCESS(
                f"Created delivery slots up until {date}"
            )
        )
