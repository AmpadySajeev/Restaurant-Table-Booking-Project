from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser, RestaurantProfile, MenuItem, TableBooking

class UserSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = None  

class RestaurantSignupForm(UserCreationForm):
    restaurant_name = forms.CharField(max_length=100)
    location = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.TextInput)
    opening_time = forms.TimeField(widget=forms.TimeInput(attrs={'type':'time'}))
    closing_time = forms.TimeField(widget=forms.TimeInput(attrs={'type':'time'}))
    number_of_tables = forms.IntegerField(widget=forms.NumberInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = None

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'restaurant'
        if commit:
            user.save()
            # create RestaurantProfile linked to this user
            restaurant_profile = RestaurantProfile.objects.create(
                user = user,
                restaurant_name = self.cleaned_data.get('restaurant_name'),
                location = self.cleaned_data.get('location'),
                description = self.cleaned_data.get('description'),
                opening_time = self.cleaned_data.get('opening_time'),
                closing_time = self.cleaned_data.get('closing_time'),
                number_of_tables = self.cleaned_data.get('number_of_tables')
            )
            restaurant_profile.save()
        return user
    
class RestaurantProfileForm(forms.ModelForm):
    class Meta:
        model = RestaurantProfile
        fields = ['restaurant_name', 'location', 'description', 'opening_time', 'closing_time', 'number_of_tables']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['opening_time'].widget = forms.TimeInput(attrs={'type': 'time'})
        self.fields['closing_time'].widget = forms.TimeInput(attrs={'type': 'time'})



class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'menu_image' , 'price', 'available']
        widgets = {
            'description' : forms.Textarea(attrs={'class' : 'form-control'}),
            'name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'price' : forms.TextInput(attrs={'class' : 'form-control'}),
        }

class TableBookingForm(forms.ModelForm):
    class Meta:
        model = TableBooking
        fields = ['date', 'time', 'number_of_people','table_number']
        widgets = {
            'date' : forms.DateInput(attrs={'type' : 'date','class' : 'form-control', 'placeholder' : 'Select your date'}),
            'time' : forms.TimeInput(attrs={'type': "time",'class' : 'form-control', 'placeholder' : 'Select your time'}),
            'number_of_people' : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter number of people'}),
            'table_number' : forms.Select(attrs={'class' : 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        restaurant = kwargs.pop('restaurant', None)
        super(TableBookingForm, self).__init__(*args, **kwargs)
        if restaurant:
            print(f"Restaurant : {restaurant.restaurant_name}")
            date = self.data.get('date') or self.initial.get('date')
            if date:
                
                available_tables = [
                    (i,i) for i in range(1, restaurant.number_of_tables + 1)
                    if not restaurant.bookings.filter(date = date, table_number = i).exists()
                ]
                print(f"Available tables : {available_tables}")
                self.fields['table_number'] = forms.ChoiceField(choices=available_tables)
