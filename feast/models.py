from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.contrib.auth import get_user_model

# Create your models here.

class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('restaurant', 'Restaurant'),
        ('user', 'User'),
    )

    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='user')

class RestaurantProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='restaurantprofile')
    restaurant_name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    description = models.TextField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    slug = models.SlugField(unique=True, blank=True)
    number_of_tables = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.restaurant_name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.restaurant_name)
        super().save(*args, **kwargs)
    
class MenuItem(models.Model):
    restaurant = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=50)
    menu_image = models.ImageField(upload_to='menu', blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} at {self.restaurant.restaurant_name}"
    
class TableBooking(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    time = models.TimeField()
    number_of_people = models.PositiveIntegerField()
    table_number = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Booking by {self.user.username} at {self.restaurant.restaurant_name} on {self.date} at {self.time}" 

