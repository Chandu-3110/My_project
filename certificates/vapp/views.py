from django.shortcuts import render

def home(request):
    return render(request, 'home.html')


from django.shortcuts import render, HttpResponse
from .models import User

def register(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']

        User.objects.create(
            name=name,
            email=email,
            password=password,
            role=role
        )
        return HttpResponse("Registered Successfully")

    return render(request, 'register.html')




def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.filter(email=email, password=password).first()

        if user:
            if user.role == 'student':
                return render(request, 'student/dashboard.html')
            elif user.role == 'college':
                return render(request, 'college/dashboard.html')
            elif user.role == 'company':
                return render(request, 'company/dashboard.html')
        else:
            return HttpResponse("Invalid Login")

    return render(request, 'login.html')