from django.forms import ModelForm
from .models import User, Room, Message
from django.contrib.auth.forms import UserCreationForm


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar' ,'name', 'username' ,'email', 'bio']


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['topic', 'name', 'description']