from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, RestaurantProfile, TableBooking, MenuItem

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(RestaurantProfile)
admin.site.register(MenuItem)
admin.site.register(TableBooking)
