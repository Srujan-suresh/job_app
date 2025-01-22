# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    required_skills = models.TextField()
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=50) 
    salary_range = models.CharField(max_length=50, blank=True)
   
    def __str__(self):
        return self.title

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, null=True, blank=True)