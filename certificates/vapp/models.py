from django.db import models

class User(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('college', 'College'),
        ('company', 'Company'),
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.name
    
    
    
    
    from django.db import models
from django.conf import settings

class Certificate(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.CharField(max_length=100)
    grade = models.CharField(max_length=10)
    issued_by = models.CharField(max_length=100)
    certificate_hash = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.course} - {self.student}"