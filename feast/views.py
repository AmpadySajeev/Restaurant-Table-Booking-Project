from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import login,logout,authenticate  
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import TableBooking, RestaurantProfile, MenuItem, CustomUser
from .forms import UserSignupForm, RestaurantSignupForm, MenuItemForm, TableBookingForm, RestaurantProfileForm


# Create your views here.

def mainpage(request):
    restaurants = RestaurantProfile.objects.all()
    return render(request, 'main.html',{'restaurants' : restaurants})

def restaurant_page(request, slug):
    restaurant = get_object_or_404(RestaurantProfile, slug = slug)
    menu_items = MenuItem.objects.filter(restaurant = restaurant)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(loginpage)
        form = TableBookingForm(request.POST, restaurant = restaurant)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.restaurant = restaurant
            booking.status = 'pending'
            booking.save()
            return redirect(booking_pending)
    else:
        form = TableBookingForm(restaurant = restaurant)
    return render(request, 'restaurantPage.html', {'restaurant' : restaurant, 'menu_items' : menu_items, 'form' : form})

def all_menu(request, slug):
    restaurant = get_object_or_404(RestaurantProfile, slug = slug)
    menu_details = MenuItem.objects.filter(restaurant = restaurant)
    return render(request, 'all_menu.html',{'menu_details' : menu_details})

@login_required
def booking_pending(request):
    latest_booking = TableBooking.objects.filter(user = request.user).latest('id')
    return render(request, 'booking_pending.html', {'booking' : latest_booking})

def loginpage(request):
    
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username = username, password = password)
    
    if user:
        login(request, user)
        # print(f"user authenticated: {user.username}, role : {user.role}, slug : {user.restaurantprofile.slug}")

        if user.role == 'restaurant':
            return redirect(restaurant_dashboard, slug = user.restaurantprofile.slug)
        elif user.role == 'admin':
            return redirect(goToAdmin)
        else:
            
            return redirect(mainpage)
    return render(request, 'login.html')

def logoutpage(request):
    logout(request)
    return redirect(loginpage)

def user_signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(mainpage)
    else:
        form = UserSignupForm()
    return render(request, 'signup.html', {'form' : form, 'role' : 'User'})

def restaurant_signup(request):
    if request.method == 'POST':
        form = RestaurantSignupForm(request.POST)
        if form.is_valid():
            restaurant_user = form.save()
            login(request, restaurant_user)
            return redirect(restaurant_dashboard, slug = restaurant_user.restaurantprofile.slug)
    else:
        form = RestaurantSignupForm()
    return render(request, 'signup.html', {'form' : form, 'role' : 'Restaurant'})

@login_required
def restaurant_dashboard(request, slug):
    restaurant = get_object_or_404(RestaurantProfile, slug = slug)
    if request.user != restaurant.user:
        return redirect(mainpage)
    menu_items = MenuItem.objects.filter(restaurant = restaurant)
    bookings = TableBooking.objects.filter(restaurant = restaurant, status = 'pending')
    all_bookings = TableBooking.objects.filter(restaurant = restaurant)
    return render(request, 'restaurant_dashboard.html', {'restaurant' :  restaurant, 'menu_items' : menu_items, 'bookings' : bookings, 'all_bookings' : all_bookings})

@login_required
def accept_booking(request, booking_id):
    booking = get_object_or_404(TableBooking, id = booking_id)
    booking.status = 'accepted'
    booking.save()
    request.session['booking_message'] = f'Your last booking request at {booking.restaurant.restaurant_name} was accepted.'
    return redirect(restaurant_dashboard, slug = booking.restaurant.slug)

@login_required
def reject_booking(request, booking_id):
    booking = get_object_or_404(TableBooking, id = booking_id)
    booking.status = 'rejected'
    booking.save()
    request.session['booking_message'] = f'Your last booking request at {booking.restaurant.restaurant_name} was rejected.'
    return redirect(restaurant_dashboard, slug = booking.restaurant.slug)

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(TableBooking, id = booking_id, user = request.user)
    booking.status = 'cancelled'
    booking.save()
    request.session['booking_message'] = f"Your last booking request at {booking.restaurant.restaurant_name} has been successfully cancelled."
    return redirect(userProfile, user_id = request.user.id)

# @login_required
# def menu_list(request):
#     restaurant = RestaurantProfile.objects.get(user = request.user)
#     menu_items = MenuItem.objects.filter(restaurant = restaurant)
#     return render(request, 'menu_list.html', {'menu_items' : menu_items})

@login_required
def add_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save(commit=False)
            restaurant_profile = RestaurantProfile.objects.get(user = request.user)
            menu_item.restaurant = restaurant_profile
            menu_item.save()
            return redirect(restaurant_dashboard, slug = restaurant_profile.slug)
    else:
        form = MenuItemForm()
    return render(request, 'add_menu_item.html',{'form' : form})

@login_required
def edit_menu_item(request, item_id):
    menu_item = get_object_or_404(MenuItem, id = item_id, restaurant__user = request.user)
    if request.method == 'POST':
        form = MenuItemForm(request.POST,request.FILES, instance=menu_item)
        if form.is_valid():
            menu_item = form.save(commit=False)
            restaurant_profile = RestaurantProfile.objects.get(user = request.user)
            menu_item.restaurant = restaurant_profile
            menu_item.save()
            return redirect(restaurant_dashboard, slug = restaurant_profile.slug)
    else:
        form = MenuItemForm(instance=menu_item)
    return render(request, 'edit_menu_item.html',{'form' : form} )

@login_required
def delete_menu_item(request, item_id):
    menu_item = get_object_or_404(MenuItem, id = item_id, restaurant__user = request.user)
    restaurant_profile = RestaurantProfile.objects.get(user = request.user)
    menu_item.delete()
    return redirect(restaurant_dashboard, slug = restaurant_profile.slug)

 

@login_required
def goToAdmin(request):
    restaurants = RestaurantProfile.objects.all()
    all_users = CustomUser.objects.filter(role = 'user')
    return render(request, 'admin_dashboard.html',{'restaurants' : restaurants, 'all_users' : all_users} )

def goToStaff(request):
    return render(request, 'staff_dashboard.html')

def staffProfile(request):
    return render(request, 'staff-profile.html')

def userDetails(request):
    return render(request, 'user-details.html')

@login_required
def userProfile(request, user_id):
    user_details = CustomUser.objects.get(id = user_id)
    booking_details = TableBooking.objects.filter(user = user_details)
    booking_message = request.session.pop('booking_message', None)
    return render(request, 'user-profile.html', {'user_details' : user_details, 'booking_details' : booking_details, 'booking_message' : booking_message})

@login_required
def userProfileAdmin(request, user_id):
    user_details = CustomUser.objects.get(id = user_id)
    booking_details = TableBooking.objects.filter(user = user_details)
    return render(request, 'user_profile_admin.html', {'user_details' : user_details, 'booking_details' : booking_details})

# admin dashboard list powers
@login_required
def user_edit_admin(request, user_id):
    user_edit_details = CustomUser.objects.get(id = user_id)
    if request.method == 'POST':
        form = UserSignupForm(request.POST, instance = user_edit_details)
        if form.is_valid():
            form.save()
            return redirect(goToAdmin)
    else:
        form = UserSignupForm(instance = user_edit_details)
    return render(request, 'user-edit-admin.html', {'form' : form})

@login_required
def user_delete_admin(request, user_id):
    user_delete_details = get_object_or_404(CustomUser, id = user_id)
    user_delete_details.delete()
    return redirect(goToAdmin)

@login_required
def rest_profile_admin(request, slug):
    rest_details = RestaurantProfile.objects.get(slug = slug)
    menu_items = MenuItem.objects.filter(restaurant = rest_details)
    all_bookings = TableBooking.objects.filter(restaurant = rest_details)
    return render(request, 'rest-profile-admin.html',{'rest_details' : rest_details, 'menu_items' : menu_items, 'all_bookings' : all_bookings})

@login_required
def rest_edit_admin(request, slug):
    rest_details = get_object_or_404(RestaurantProfile, slug=slug)
    
    if request.method == 'POST':
        form = RestaurantProfileForm(request.POST, instance=rest_details)
        if form.is_valid():
            form.save()
            return redirect(goToAdmin)
    else:
        form = RestaurantProfileForm(instance=rest_details)
        
        
    return render(request, 'rest-edit-admin.html', {'form' : form, 'rest_details' : rest_details})

@login_required
def rest_delete_admin(request, slug):
    rest_details = RestaurantProfile.objects.get(slug = slug)
    rest_details.delete()
    return redirect(goToAdmin)


