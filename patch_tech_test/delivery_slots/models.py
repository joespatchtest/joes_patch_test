from django.db import models


class Slot(models.Model):
    TIME_OF_DAY_CHOICES = [
            ("AM", "AM"),
            ("PM", "PM"),
            ("EVE", "EVE"),
    ]
    date = models.DateField()
    time_of_day = models.CharField(
        max_length=3,
        choices=TIME_OF_DAY_CHOICES,
    )
    capacity = models.PositiveIntegerField()
    unavailable = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('date', 'time_of_day'),
                name="unique_slot",
            )
        ]
        ordering = ('date', 'time_of_day', )

    def __str__(self):
        return f"{self.date}, {self.time_of_day}"

    def is_full(self):
        return self.capacity <= 0
