from django.contrib import admin
from .models import User, Certificate

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'role')

admin.site.register(User, UserAdmin)
admin.site.register(Certificate)