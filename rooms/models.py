from django.db import models

# Create your models here.
class rooms(models.Model):
    name = models.CharField(max_length=20)
    floor_number = models.IntegerField(default=1)
    room_number = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name} at {self.floor_number} on {self.room_number}"