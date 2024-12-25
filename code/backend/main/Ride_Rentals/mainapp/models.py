from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.template.defaultfilters import slugify  # Import slugify function

# Create your models here.

class Car_info(models.Model):

    img = models.ImageField(upload_to="car_pics")
    name = models.CharField(max_length=50)
    year = models.IntegerField(default=2024) 
    capacity = models.IntegerField(null=False)
    mileage = models.FloatField(null=False) 
    engine = models.CharField(max_length=20)
    gear = models.CharField(max_length=20)
    available = models.BooleanField(default=True)
    price = models.FloatField(default=0.0)

    # Add a unique slug field
    slug = models.SlugField(max_length=100, unique=True, blank=True)  # Adjust length as needed

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Generate slug from name
        super(Car_info, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Booking(models.Model):
    cus_name = models.CharField(max_length=50)
    cus_ph = models.CharField(max_length=12)
    cus_email = models.CharField(max_length=30)

    # Foreign key relationship with Car_info
    name = models.ForeignKey(Car_info, on_delete=models.CASCADE)

    pickup_date = models.DateField()
    return_date = models.DateField()
    booked_on = models.DateField(auto_now=True)
    notes = models.TextField()

@receiver(post_delete, sender=Car_info)
def delete_event_image(sender, instance, **kwargs):
    if instance.img:
        instance.img.delete(save=False)