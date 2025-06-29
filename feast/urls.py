from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path('main', mainpage, name='mainpage'),
    path('login', loginpage, name='login'),
    path('logout', logoutpage, name='logout'),
    # path('signup', signup_page, name='signup'),

    path('signup/user', user_signup, name = 'user_signup'),
    path('signup/restaurant', restaurant_signup, name='restaurant_signup'),

    path('restaurant-dashboard/<slug:slug>', restaurant_dashboard, name='restaurant_dashboard'),
    path('add_menu_item', add_menu_item, name='add_menu_item'),
    path('edit_menu_item/<int:item_id>', edit_menu_item, name='edit_menu_item'),
    path('delete_menu_item/<int:item_id>', delete_menu_item, name='delete_menu_item'),

    path('restaurant/<slug:slug>', restaurant_page, name='rest-page'),
    path('all_menu/<slug:slug>', all_menu, name='all_menu'),
    path('booking-pending', booking_pending, name='booking_pending'),
    path('accept-booking/<int:booking_id>', accept_booking, name='accept_booking'),
    path('reject-booking/<int:booking_id>', reject_booking, name='reject_booking'),
    path('cancel_booking/<int:booking_id>', cancel_booking, name='cancel_booking'),

    path('admin-dashboard' , goToAdmin, name = 'admindb'),
    path('staff-dashboard' , goToStaff, name = 'staffdb'),
    path('staff-profile' , staffProfile, name = 'staff-profile'),
    path('user-details', userDetails, name='user-details'),

    path('user-profile/<int:user_id>', userProfile, name='user-profile'),
    path('user-profile-admin/<int:user_id>', userProfileAdmin, name='user-profile-admin'),

    # admin power
    path('user-edit-admin/<int:user_id>', user_edit_admin, name='user_edit_admin'),
    path('user-delete-admin/<int:user_id>', user_delete_admin, name='user_delete_admin'),

    path('rest-profile-admin/<slug:slug>', rest_profile_admin, name='rest_profile_admin'),
    path('rest-edit-admin/<slug:slug>', rest_edit_admin, name='rest_edit_admin'),
    path('rest_delete_admin/<slug:slug>', rest_delete_admin, name='rest_delete_admin'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)