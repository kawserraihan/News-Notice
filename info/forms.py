import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import *



class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name',]


class DayForm(forms.ModelForm):
    class Meta:
        model = Day
        fields = ['day',]

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'name', 'password1', 'password2', 'email', 'department', 'address', 'contact_number',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'name', 'email', 'department', 'address', 'contact_number',)

    password = forms.CharField(widget=forms.PasswordInput(), required=False)

    def clean_password(self):
        # Ensure that the password is hashed before saving
        return self.cleaned_data['password'] if self.cleaned_data['password'] else None

class BusScheduleForm(forms.ModelForm):
    class Meta:
        model = BusSchedule
        fields = ['time','bus_no','day','bus_type','route_type',]


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name',]



class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'description', 'image', 'tags']

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title','description', 'posted_by','tags']



        

        


        