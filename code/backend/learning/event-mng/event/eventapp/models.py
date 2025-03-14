from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
# Create your models here.

class Event(models.Model):
    img = models.ImageField(upload_to="pic")
    name = models.CharField(max_length=50)
    dec = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Booking(models.Model):
    cus_name = models.CharField(max_length=50)
    cus_ph = models.CharField(max_length=12)

    # pull data from table using foreign key
    name = models.ForeignKey(Event, on_delete=models.CASCADE)
    # if any event deleted then delete record data realted to foreign key
    booking_date = models.DateField()
    booked_on = models.DateField(auto_now=True)

@receiver(post_delete, sender=Event)
def delete_event_image(sender, instance, **kwargs):
    if instance.img:
        instance.img.delete(save=False)
