from django.db import models

# Create your models here.
class Account(models.Model):
    Id = models.IntegerField(default=1)
    Name = models.CharField(max_length=255, null="true")
    Email = models.CharField(max_length=255, null="true")
    Department = models.CharField(max_length=255, null="true")
    Verified = models.BooleanField(default=False)

class Teacher(models.Model):
    Name = models.CharField(max_length=255, null="true")
    Email = models.CharField(max_length=255, null="true")
    Department = models.CharField(max_length=255, null="true")
    Designation = models.CharField(max_length=255, null="true")
    Verified = models.BooleanField(default=False)