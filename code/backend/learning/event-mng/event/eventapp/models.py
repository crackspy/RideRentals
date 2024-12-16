from django.db import models

# Create your models here.

class Event(models.Model):
    img = models.ImageField(upload_to="pic")
    name = models.CharField(max_length=50)
    dec = models.CharField(max_length=50)

class Booking(models.Model):
    cus_name = models.CharField(max_length=50)
    cus_ph = models.CharField(max_length=12)
    # pull data from table using foreign key
    name = models.ForeignKey(Event, on_delete=models.CASCADE)
    # if any event deleted then deleted foreign key data will be deleted
    # booking_date =
    # booked_on = 