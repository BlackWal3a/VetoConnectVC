from django.db import models
from django.contrib.auth.models import User 


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    surname = models.CharField(max_length=50, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    nom_clinique = models.CharField(max_length=50, blank=True, null=True)
    num_ordre = models.IntegerField(blank=True, null=True)
    specialty = models.CharField(max_length=50, blank=True, null=True)
    animall_examined = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    units = models.CharField(max_length=50, blank=True, null=True)
    dark_mode = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class AnimalForm(models.Model):
    id = models.AutoField(primary_key=True)  # Add an auto-incrementing primary key ID field
    form_picture = models.ImageField(upload_to='animal_pictures/', blank=True, null=True)
    client_name = models.CharField(max_length=100, null=True)
    email = models.EmailField()  # Add an email field
    clinic = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(auto_now_add=True)  # Automatically set the date and time when the form is submitted
    animal_name = models.CharField(max_length=100)
    animal_type = models.CharField(max_length=100)
    problem = models.CharField(max_length=1000)
    probleme = models.CharField(max_length=1000)
    description = models.TextField()
    # New fields for storing images
    picture1 = models.ImageField(upload_to='animal_pictures/', blank=True, null=True)
    picture2 = models.ImageField(upload_to='animal_pictures/', blank=True, null=True)
    picture3 = models.ImageField(upload_to='animal_pictures/', blank=True, null=True)
    status = models.CharField(max_length=100, default='En attente')  # Allow null values #1st needed for checks
    status_feedback = models.CharField(max_length=100, default='No')  # Allow null values   #2nd needed for checks
    stars = models.IntegerField(blank=True, null=True)
    feedback_text = models.TextField(blank=True, null=True)  # Add a response field    
    response = models.TextField(blank=True, null=True)  # Add a response field
    viewed = models.CharField(max_length=100, default='No')

    def __str__(self):
        return self.animal_name

from django.db import models

class Blacklist(models.Model):
    email = models.EmailField(unique=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Help(models.Model):
    nom = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField()
    response = models.TextField(blank=True, null=True)  # Add a response field

    def __str__(self):
        return self.email