from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.text import slugify
from django.contrib.auth.models import User  # Import User model
import os

# User profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='media/images/profile_pics/', 
        blank=True, 
        null=True, 
        default='media/images/profile_pics/default.png'
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    # You can access email, first_name, last_name, and username via `profile.user.email`, `profile.user.first_name`, etc.

    def __str__(self):
        return self.user.username


# Car details
class Car_info(models.Model):
    def image_upload_path(instance, filename):
        ext = os.path.splitext(filename)[-1]  # Get the file extension
        new_filename = f"{instance.slug}{ext}"  # Format filename using slug
        return os.path.join("images/car_pics", new_filename)  # Store in media/images/car_pics/
    
    img = models.ImageField(upload_to=image_upload_path)  # Upload path updated
    name = models.CharField(max_length=50)
    year = models.IntegerField(default=2024)
    capacity = models.IntegerField(null=False)
    mileage = models.FloatField(null=False)

    class Engine(models.TextChoices):
        Hybrid = 'Hybrid'
        Petrol = 'Petrol'
        Diesel = 'Diesel'

    class Transmission(models.TextChoices):
        Manual = 'Manual'
        Automatic = 'Automatic'

    engine = models.CharField(
        max_length=10,
        choices=Engine.choices,
        default=Engine.Petrol,
    )

    transmission = models.CharField(
        max_length=15,
        choices=Transmission.choices,
        default=Transmission.Manual,
    )

    available = models.BooleanField(default=True)
    rent = models.FloatField(default=0.0)
    slug = models.SlugField(max_length=100, unique=True, blank=True)  # Unique slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Car_info, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


#  Booking details
class Booking(models.Model):
    cus_name = models.CharField(max_length=50)
    cus_ph = models.CharField(max_length=15)
    cus_email = models.EmailField(max_length=254)

    # ForeignKey to Car_info
    car = models.ForeignKey('Car_info', on_delete=models.CASCADE)

    # ForeignKey to User (Customer)
    cus_username = models.ForeignKey(User, on_delete=models.CASCADE)

    class Status(models.TextChoices):
        BOOKED = 'Booked'
        RENTED = 'Rented'
        COMPLETED = 'Completed'

    class Payment_Status(models.TextChoices):
        PAID = 'Paid'
        PENDING = 'Pending'

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.BOOKED,  # Default value is 'Booked'
    )

    pickup_date = models.DateField()
    return_date = models.DateField()
    booked_on = models.DateField(auto_now=True)
    rent = models.DecimalField(max_digits=10, decimal_places=2) # Car price
    total_rent = models.DecimalField(max_digits=10, decimal_places=2) # Computed total rent
    payment_status = models.CharField(
        max_length=10,
        choices=Payment_Status.choices,
        default=Payment_Status.PENDING,  # Default value is 'Pending'
    )

    def save(self, *args, **kwargs):
        # Update car availability when status is set to 'completed'
        if self.status == Booking.Status.COMPLETED:
            self.car.available = True  # Set car as available
            self.car.save()  # Save the car object to reflect the change
        
        super(Booking, self).save(*args, **kwargs)  # Call the original save method

    def __str__(self):
        return f"Booking by {self.cus_name} for {self.car.name}"

# Wishlists
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to User
    car = models.ForeignKey(Car_info, on_delete=models.CASCADE)  # ForeignKey to Car_info
    added_on = models.DateTimeField(auto_now_add=True)  # Timestamp when added to wishlist

    class Meta:
        unique_together = ('user', 'car')  # Ensures a user cannot add the same car twice

    def __str__(self):
        return f"{self.user.username} - {self.car.name}" 


@receiver(post_delete, sender=Car_info)
def delete_event_image(sender, instance, **kwargs):
    if instance.img and os.path.isfile(instance.img.path):
        instance.img.delete(save=False)


