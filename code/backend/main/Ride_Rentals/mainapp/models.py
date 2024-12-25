from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
# Create your models here.

class Car_info(models.Model):
    img = models.ImageField(upload_to="car_pics")
    name = models.CharField(max_length=50)
    capacity = models.IntegerField(null=False)
    mileage = models.IntegerField(null=False)
    engine = models.CharField(max_length=20)
    gear = models.CharField(max_length=20)
    available = models.BooleanField(default=True) 

    def __str__(self):
        return self.name

class Booking(models.Model):
    cus_name = models.CharField(max_length=50)
    cus_ph = models.CharField(max_length=12)
    cus_email = models.CharField(max_length=30)

    # pull data from table using foreign key
    name = models.ForeignKey(Car_info, on_delete=models.CASCADE)
    # if any event deleted then delete record data realted to foreign key
    pickup_date = models.DateField()
    return_date = models.DateField()
    booked_on = models.DateField(auto_now=True)
    notes = models.TextField()

@receiver(post_delete, sender=Car_info)
def delete_event_image(sender, instance, **kwargs):
    if instance.img:
        instance.img.delete(save=False)