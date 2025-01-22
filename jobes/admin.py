# Register your models here.
from django.contrib import admin
from .models import Job
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required

admin.site.register(Job)

# Admin-only View for Managing Jobs
@staff_member_required
def add_job(request):
    if request.method == 'POST':
        pass
    return render(request, 'add_job.html')  
