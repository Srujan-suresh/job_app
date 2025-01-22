from django.shortcuts import render, get_object_or_404, redirect
from .models import Job, Application
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.admin.views.decorators import staff_member_required
from .forms import JobForm
from django.contrib.auth.views import LoginView

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('job_listings') 
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

def job_listings(request):
    jobs = Job.objects.all()

    location = request.GET.get('location')
    job_type = request.GET.get('job_type')
    skills = request.GET.get('skills')

    if location:
        jobs = jobs.filter(location__icontains=location)
    if job_type:
        jobs = jobs.filter(job_type__icontains=job_type)
    if skills:
        jobs = jobs.filter(description__icontains=skills)
    return render(request, 'jobes/job_listings.html', {'jobs': jobs})

@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        user = request.user
        if not Application.objects.filter(job=job, user=user).exists():
            Application.objects.create(job=job, user=user)
            messages.success(request, 'Thank you for applying! ')
        else:
            messages.warning(request, 'You have already applied for this job.')
        return redirect('home')  
    return render(request, 'jobes/job_detail.html', {'job': job})

def apply_for_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        user = request.user
        if not Application.objects.filter(job=job, user=user).exists():
            Application.objects.create(job=job, user=user, status="pending")
            messages.success(request, 'Thank you for applying!')
        else:
            messages.warning(request, 'You have already applied for this job.')
        return redirect('home') 
    return render(request, 'jobes/job_detail.html', {'job': job})

@login_required
def applied_jobs(request):
    applications = Application.objects.filter(user=request.user)
    return render(request, 'applied_jobs.html', {'applications': applications})

def home_view(request):
    return render(request, 'home.html')

# User Signup View
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# User Login View (Custom Login)
class CustomLoginView(LoginView):
    template_name = 'login.html'  
    redirect_authenticated_user = True 

# Add Job View (Staff Only)
@staff_member_required
def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_listings') 
    else:
        form = JobForm()
    return render(request, 'add_job.html', {'form': form})