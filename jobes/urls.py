from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('jobs/', views.job_listings, name='job_listings'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'), 
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('applications/', views.applied_jobs, name='applied_jobs'),
    path('add_job/', views.add_job, name='add_job'),
]
