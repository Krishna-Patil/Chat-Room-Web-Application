from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class RoomCreateForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class RoomUpdateForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'topic', 'discription']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_pic', 'name', 'username', 'email', 'bio']
