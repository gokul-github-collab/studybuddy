from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=100, null = True)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)

    avatar = models.ImageField(blank=True, null=True, default='profile.jpg')

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    # pass    
class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name
    

class Room(models.Model):
    name =  models.CharField(max_length=100)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    description=  models.TextField(blank=True, null=True)
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']
        
    def __str__(self) -> str:
        return self.description[:50]
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField(blank = True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:

        ordering = ['-updated', '-created']

    def __str__(self) -> str:
        return self.body[:20] 
    