from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('uploadfile/', views.uploadfile, name='uploadfile'),
    path('viewfiles/', views.viewfiles, name='viewfiles'),
    path('datastatus/', views.datastatus, name='datastatus'),
    path('requestfiles/<int:id>/', views.requestfiles, name='requestfiles'),
    path('filerequests/', views.filerequests, name='filerequests'),
    path('acceptrequest/<int:id>/', views.acceptrequest, name='acceptrequest'),
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('viewallfiles/', views.viewallfiles, name='viewallfiles'),
    path('viewrequests/', views.viewrequests, name='viewrequests'),
    path('generatekey/<int:id>/', views.generatekey, name='generatekey'),
    path('filetransactions/', views.filetransactions, name='filetransactions'),
    path('viewresponses/', views.viewresponses, name='viewresponses'),
    path('downloadfile/<int:id>/', views.downloadfile, name='downloadfile'),

    
]
