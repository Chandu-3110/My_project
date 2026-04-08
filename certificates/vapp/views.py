
import hashlib
from django.shortcuts import render, redirect
from .models import User, Certificate


# 🔐 HASH FUNCTION
def generate_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()


# 🏠 HOME
def home(request):
    return render(request, 'home.html')


# 📝 REGISTER
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

        return render(request, 'message.html', {
            'message': '✅ Registered Successfully',
            'back_url': '/login/'
        })

    return render(request, 'register.html')


# 🔑 LOGIN
def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.filter(email=email, password=password).first()

        if user:
            # ✅ STORE SESSION
            request.session['user_id'] = user.id
            request.session['role'] = user.role

            # ✅ REDIRECT BASED ON ROLE
            if user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'college':
                return redirect('college_dashboard')
            elif user.role == 'company':
                return redirect('company_dashboard')

        else:
            return render(request, 'message.html', {
                'message': '❌ Invalid Login',
                'back_url': '/login/'
            })

    return render(request, 'login.html')


# 🚪 LOGOUT
def logout_view(request):
    request.session.flush()
    return redirect('home')


# 🎓 STUDENT DASHBOARD
def student_dashboard(request):
    if request.session.get('role') != 'student':
        return redirect('login')

    user_id = request.session.get('user_id')

    # ✅ Get logged-in student
    student = User.objects.get(id=user_id)

    # ✅ Fetch certificates of that student
    certificates = Certificate.objects.filter(student=student)

    return render(request, 'student/dashboard.html', {
        'certificates': certificates
    })


# 🏫 COLLEGE DASHBOARD
def college_dashboard(request):
    if request.session.get('role') != 'college':
        return redirect('login')
    return render(request, 'college/dashboard.html')


# 🏢 COMPANY DASHBOARD
def company_dashboard(request):
    if request.session.get('role') != 'company':
        return redirect('login')
    return render(request, 'company/dashboard.html')


# 📄 ADD CERTIFICATE
def add_certificate(request):
    if request.session.get('role') != 'college':
        return redirect('login')

    if request.method == "POST":
        name = request.POST['name']
        course = request.POST['course']
        grade = request.POST['grade']
        issued_by = request.POST['issued_by']

        student = User.objects.filter(name=name, role='student').first()

        if not student:
            return render(request, 'message.html', {
                'message': '❌ Student not found',
                'back_url': '/add_certificate/'
            })

        data = student.name + course + grade + issued_by
        cert_hash = generate_hash(data)

        Certificate.objects.create(
            student=student,
            course=course,
            grade=grade,
            issued_by=issued_by,
            certificate_hash=cert_hash
        )

        return render(request, 'message.html', {
            'message': '✅ Certificate Added Successfully',
            'back_url': '/add_certificate/'
        })

    return render(request, 'college/add_certificate.html')


# 🔍 VERIFY CERTIFICATE
def verify_certificate(request):
    if request.session.get('role') != 'company':
        return redirect('login')

    if request.method == "POST":
        name = request.POST['name']
        course = request.POST['course']
        grade = request.POST['grade']
        issued_by = request.POST['issued_by']

        data = name + course + grade + issued_by
        new_hash = generate_hash(data)

        cert = Certificate.objects.filter(
            certificate_hash=new_hash
        ).first()

        if cert:
            return render(request, 'message.html', {
                'message': '✅ Certificate is VALID',
                'back_url': '/verify/'
            })
        else:
            return render(request, 'message.html', {
                'message': '❌ Certificate is FAKE',
                'back_url': '/verify/'
            })

    return render(request, 'company/verify.html')
