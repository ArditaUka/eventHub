from __future__ import unicode_literals
from django.db import models
import re
from datetime import datetime

# Create your models here.

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validator(self, postData):
        errors={}
        if len(postData["first_name"])<2:
            errors["first_name"] = "First name must be at least 2 characters long"
        if len(postData["last_name"])<2:
            errors["last_name"] = "Last name must be at least 2 characters long"
        if len(postData["email"])<1:
            errors["email"] = "Email cannot be blank"
        if not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Email is not valid"
        result = User.objects.filter(email=postData['email'])
        if len(result)>0:
            errors['email'] = "Email address is already registered"
        
        if len(postData["password"])<8:
            errors["password"] = "Password must be at least 8 characters long."
        elif postData["password"] != postData["confirm_password"]:
            errors["password"] = "Passwords do not match"
        return errors        

class EventManager(models.Manager):
    def validator(self, postData):
        errors={}
        if len(postData["name"])<3:
            errors["name"] = "Name must be at least 3 characters long"
        if len(postData["location"])<3:
            errors["location"] = "Location must be at least 3 characters long"
        if len(postData["tickets"])<1:
            errors["tickets"] = "You must provide a number of tickets"
        if len(postData["price"])<1:
            errors["price"] = "You must provide a price per ticket"
        if len(postData["about"])<5:
            errors["price"] = "Description must be at least 3 characters long"
        if postData['start_date'] == "":
            errors["start_date"] = "Start Date must be filled in."
        else:
            converted_start_date = datetime.strptime(postData['start_date'], '%Y-%m-%d')
            if converted_start_date < datetime.now():
                errors['start_date'] = "Invalid Date (must be a future date)"
        return errors



class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Event(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    category = models.CharField(max_length=100)
    tickets = models.IntegerField()
    price = models.IntegerField()
    about = models.TextField()
    users = models.ManyToManyField(User, related_name="events")
    creator = models.ForeignKey(User,related_name="created_events", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = EventManager()


class Cart(models.Model):
    event = models.ForeignKey(Event, related_name="cart", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
# class Category(models.Model):
#     name = models.CharField(max_length=255, null=True)
#     events = models.ForeignKey(Event, related_name="categories", on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add = True)
#     updated_at = models.DateTimeField(auto_now = True)