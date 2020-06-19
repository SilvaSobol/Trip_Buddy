from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from datetime import datetime
import re


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = []

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # PASS tests whether a field matches the pattern            
            errors.append ("Invalid email address!")

        if len(postData['first_name']) < 2:
            errors.append("First name should be at least 2 characters long ")

        if len(postData['last_name']) < 2:
            errors.append("Last name should be at least 2 characters long ")

        if len(postData['email']) < 1:    #pass email cant be blank 
            errors.append("Invalid Email")
        
        if len(postData['psw']) < 8:  
           errors.append("Your password needs to be at least 8 characters long")
        
        if postData['psw'] != postData['confirm']:      #PASS if password does not match 
            errors.append("Password does not match!")

        result = User.objects.filter(email = postData['email']) #PASS if the email already exists!
        if result:
            errors.append("Email already created!")


            return errors
        
class TripManager(models.Manager):
    def basic_validator(self, postData):
        errors = []

        if len(postData['destination']) < 3:
            errors.append("A trip destination must be at least 3 characters long ")

        if postData['plan'] == "":
             errors.append("A plan must be provided!")

        else:                                                                   #PASS if younger than 13
            start_date = datetime.strptime(postData['start_date'],'%Y-%m-%d')
            end_date = datetime.strptime(postData['end_date'],'%Y-%m-%d')
            today = datetime.now()
            if (start_date.year, start_date.month, start_date.day) > (end_date.year, end_date.month, end_date.day):
                errors.append('Please input a proper return date, it can not be before your start date!')

            elif (start_date.year, start_date.month, start_date.day) < (today.year, today.month, today.day):
                errors.append("Start Date should be in future! ")


        return errors


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.EmailField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length = 255)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.TextField()
    travels_by = models.ForeignKey(User, related_name = "has_trips", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TripManager()

        


