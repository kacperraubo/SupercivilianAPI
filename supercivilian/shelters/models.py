from django.db import models


class Shelter(models.Model):
    id = models.BigIntegerField(primary_key=True)
    capacity = models.IntegerField()
    occupancy = models.IntegerField()

    def __str__(self):
        return (
            f"Shelter {self.id} ({self.capacity - self.occupancy}/{self.capacity} free)"
        )
