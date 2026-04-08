from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # dashboards
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('college/dashboard/', views.college_dashboard, name='college_dashboard'),
    path('company/dashboard/', views.company_dashboard, name='company_dashboard'),

    # features
    path('add_certificate/', views.add_certificate, name='add_certificate'),
    path('verify/', views.verify_certificate, name='verify'),
]