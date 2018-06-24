from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile('^[_a-z0-9-]+(.[_a-z0-9-]+)@[a-z0-9-]+(.[a-z0-9-]+)(.[a-z]{2,4})$')

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if not postData['first_name'].isalpha():
            errors['first_name'] = 'First name contains non-alpha characters.'
        if len(postData['first_name']) < 3:
            errors['first_name'] = 'First name should be at least 3 characters.'
        if len(postData['first_name']) > 255:
            errors['first_name'] = 'First name should be less than 255 characters.'
        if len(postData['username']) < 3:
            errors['username'] = 'User name should be at least 3 characters.'
        if len(postData['username']) > 255:
            errors['username'] = 'User name should be less than 255 characters.'
        # if not re.match(EMAIL_REGEX, postData['email']):
        #     errors['email'] = 'Email is not valid.'
        if not postData['hireddate']:
            errors['hireddate']= 'Please enter a hire date.'
        if len(postData['password']) < 8:
            errors['password'] = 'Password should be at least 8 characters.'
        if postData['password'] != postData['confirm_password']:
            errors['password'] = 'Passwords do not match.'
        if User.objects.filter(username = postData['username']):
            errors['username'] = 'User Name already exists.' 
        return errors

class ItemManager(models.Manager):
    def itemValidator(self,postData):
        errors = {}
        if len(postData['item_name']) > 20:
            errors['item_name'] = 'Item name should be at least 4, but less than 20 characters long.'
        if len(postData['item_name']) < 4:
            errors['item_name'] = 'Item name should be at least 4, but less than 20 characters long.'
        if Item.objects.filter(name = postData['item_name']):
            errors['item_name'] = 'Item already exists.'
        return errors


class User(models.Model): #has to be capitals
    first_name = models.CharField(max_length=255)
    username = models.TextField(max_length=255)
    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now = True)
    password = models.CharField(max_length=255)
    hireDate = models.CharField(max_length=255)

    objects = UserManager()

    def __repr__(self):
        return "<User object: {} | {}>".format(self.first_name,self.username)

class Item(models.Model): #has to be capitals
    name = models.TextField(max_length=1000)
    created_by = models.ForeignKey(User, related_name = 'creates')
    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now = True) 
    liked_by = models.ManyToManyField(User, related_name="likes")

    objects = ItemManager()
    def __repr__(self):
        return "<Secret object: {} | {} | {}>".format(self.name,self.created_by,self.liked_by)
