from django.db import models
import re
# Create your models here.

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z._-]+\.[a-zA-Z]+$')
        if len(postData["first_name"]) == 0:
            errors["first_name"] = "First Name Required"
        if len(postData["last_name"]) == 0:
            errors["last_name"] = "Last Name Required"
        if not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Invalid Email"
        if len(postData["password"]) < 8:
            errors["password"] = "Password must be at least 8 characters"
        if postData["password"] != postData["confirm"]:
            errors["confirm"] = "Passwords doesn't match!"
        return errors
    
    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData["login_email"]):
            errors["login"] = "Invalid Email/Password"
        if len(postData["login_password"]) < 8:
            errors["login"] = "Invalid Email/Password"
        return errors

    def edit_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z._-]+\.[a-zA-Z]+$')
        if len(postData["edit_first_name"]) == 0:
            errors["edit_first_name"] = "First Name Required"
        if len(postData["edit_last_name"]) == 0:
            errors["edit_last_name"] = "Last Name Required"
        if not EMAIL_REGEX.match(postData["edit_email"]):
            errors["edit_email"] = "Invalid Email"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

    def __repr__(self):
        return f"Name: {self.first_name} {self.last_name}, Email: {self.email}"

class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        errors = {}
        if len(postData["author"]) == 0:
            errors["author"] = "Author Required"
        if len(postData["quote"]) == 0:
            errors["quote"] = "Quote Required"
        return errors

class Quote(models.Model):
    author = models.CharField(max_length = 255)
    quote = models.TextField()
    user = models.ForeignKey(User, related_name = "quotes", on_delete = models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name = "likes")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = QuoteManager()