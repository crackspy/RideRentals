# Built by crackspy

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import uuid
import os


# Profile details
def profile_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"  # Random string filename
    return os.path.join('images/profile_pics/', filename)

# Function to validate file size
def validate_file_size(value):
    limit = 5 * 1024 * 1024  # 5MB limit
    if value.size > limit:
        raise ValidationError("File size must be less than 5MB.")

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to=profile_image_path,
        blank=True,
        null=True,
        default='images/profile_pics/default.png',
        validators=[validate_file_size]
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def save(self, *args, **kwargs):
        try:
            old_profile = Profile.objects.get(pk=self.pk)
            if old_profile.profile_picture and old_profile.profile_picture.url != '/media/images/profile_pics/default.png':
                if old_profile.profile_picture != self.profile_picture:
                    if os.path.isfile(old_profile.profile_picture.path):
                        os.remove(old_profile.profile_picture.path)
        except Profile.DoesNotExist:
            pass  # New profile, no old image to delete

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Delete profile image when profile is deleted."""
        if self.profile_picture and self.profile_picture.url != '/media/images/profile_pics/default.png':
            if os.path.isfile(self.profile_picture.path):
                os.remove(self.profile_picture.path)
        super().delete(*args, **kwargs)

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

    class Payment_method(models.TextChoices):
        UPI = 'UPI'
        CARD = 'Card'
        CashOnDelivery = 'Cash on Delivery'

    class Payment_Status(models.TextChoices):
        PAID = 'Paid'
        PENDING = 'Pending'

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.BOOKED,  # Default value is 'Booked'
    )

    payment_method = models.CharField(
        max_length=50,
        choices=Payment_method.choices,
        default=Payment_method.CashOnDelivery, # Default value is 'COD'
    )

    payment_status = models.CharField(
        max_length=10,
        choices=Payment_Status.choices,
        default=Payment_Status.PENDING,  # Default value is 'Pending'
    )


    pickup_date = models.DateField()
    return_date = models.DateField()
    booked_on = models.DateField(auto_now=True)
    rent = models.DecimalField(max_digits=10, decimal_places=2) # Car price
    total_rent = models.DecimalField(max_digits=10, decimal_places=2) # Computed total rent

    def save(self, *args, **kwargs):
        # Update car availability when status is set to 'completed'
        if self.status == Booking.Status.COMPLETED:
            self.car.available = True 
            self.car.save()
        
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


# receivers

# delete old car image 
@receiver(post_delete, sender=Car_info)
def delete_event_image(sender, instance, **kwargs):
    if instance.img and os.path.isfile(instance.img.path):
        instance.img.delete(save=False)

# create profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# save profile
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()