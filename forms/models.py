from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Form(models.Model):
    roll = models.IntegerField(default=1)
    regno = models.IntegerField(default=1)
    session = models.CharField(max_length=255, null="true", default='')
    name = models.CharField(max_length=255, null="true", default='')
    semester = models.CharField(max_length=255, null="true", default='')
    backlog = models.TextField(null="true", default='')
    
    courseno = models.TextField(null="true", default='')
    title = models.TextField(null="true", default='')
    credit = models.TextField(null="true", default='')
    
    totalcredit = models.FloatField(default=0)
    date = models.DateTimeField(default=timezone.now)
    
    def date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')

class Counter(models.Model):
    oneOdd = models.IntegerField(default=0)
    oneEven = models.IntegerField(default=0)
    twoOdd = models.IntegerField(default=0)
    twoEven = models.IntegerField(default=0)
    threeOdd = models.IntegerField(default=0)
    threeEven = models.IntegerField(default=0)
    fourOdd = models.IntegerField(default=0)
    fourEven = models.IntegerField(default=0)