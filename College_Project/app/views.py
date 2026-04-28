from django.shortcuts import render, redirect
from . models import *
from django.contrib import messages
import pickle
from phe import paillier
import numpy as np
# Create your views here.import random
from django.db.models import Q
from django.http import FileResponse
from django.core.mail import send_mail
import random
import secrets
from .models import RequestFileModel


def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        dob = request.POST['dob']
        gender = request.POST['gender']
        contact = request.POST['contact']
        address = request.POST['address']
        profile = request.FILES['profile']
        
        if UserModel.objects.filter(email=email).exists():
            messages.success(request, 'Email already existed')
            return redirect('register')
        else:
            UserModel.objects.create(name=name, email=email, password=password, dob=dob, gender=
                                      gender, contact=contact, address=address, profile=profile).save()
            messages.success(request, 'Registration Successfull')
            return redirect('register')
    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if UserModel.objects.filter(email=email, password=password).exists():
            request.session['email']=email
            request.session['login']='user'
            return redirect('home')
        else:
            messages.success(request, 'Invalid Email or Password')
            return redirect('login')
    return render(request, 'login.html')


def home(request):
    login = request.session['login']
    return render(request, 'home.html',{'login':login})

def logout(request):
    del request.session['email']
    del request.session['login']
    return redirect('index')



def create_paillier_keys():
    # Generate Paillier public and private keys
    public_key, private_key = paillier.generate_paillier_keypair()
    return public_key, private_key

def encrypt_file(input_file_path, output_file_path, public_key):
    # Read file data
    with open(input_file_path, 'r') as file:
        file_data = file.read()
    
    # Convert text data to list of integers (ASCII values)
    data = [ord(char) for char in file_data]
    
    # Encrypt each integer
    encrypted_data = [public_key.encrypt(x) for x in data]
    
    # Serialize encrypted data
    with open(output_file_path, 'wb') as file:
        for enc in encrypted_data:
            # Convert ciphertext to bytes
            ciphertext = enc.ciphertext()
            ciphertext_bytes = ciphertext.to_bytes((ciphertext.bit_length() + 7) // 8, byteorder='big')
            # Write length followed by actual encrypted bytes
            file.write(len(ciphertext_bytes).to_bytes(2, byteorder='big'))
            file.write(ciphertext_bytes)

def decrypt_file(input_file_path, output_file_path, private_key, public_key):
    # Read encrypted file data
    with open(input_file_path, 'rb') as file:
        encrypted_data = file.read()
    
    # Deserialize encrypted data
    decrypted_data = []
    i = 0
    while i < len(encrypted_data):
        # Read length of ciphertext
        length = int.from_bytes(encrypted_data[i:i+2], byteorder='big')
        i += 2
        # Read ciphertext bytes
        ciphertext_bytes = encrypted_data[i:i+length]
        i += length
        # Convert bytes to ciphertext
        ciphertext = int.from_bytes(ciphertext_bytes, byteorder='big')
        enc_number = paillier.EncryptedNumber(public_key, ciphertext)
        decrypted_value = private_key.decrypt(enc_number)
        decrypted_data.append(decrypted_value)
    
    # Convert integers back to text
    decrypted_text = ''.join(chr(int(d)) for d in decrypted_data)
    
    # Write decrypted text to file
    with open(output_file_path, 'w') as file:
        file.write(decrypted_text)

# Example usage



def uploadfile(request):
    email = request.session['email']
    login = request.session['login']
    if request.method == 'POST':
        file = request.FILES.get('file')
        keyword = request.POST.get('Keyword')
        filename=file.name
        public_key, private_key = create_paillier_keys()
        temp_file_path = os.path.join('static', 'Files', filename)
            
            # Save the uploaded file temporarily
        with open(temp_file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Encrypt the file
        encrypt_file(temp_file_path, temp_file_path, public_key)
        # x.delete()

        
        # Read the encrypted file data
        with open(temp_file_path, 'rb') as f:
            file_data = f.read()
        
        private_key_serialized = pickle.dumps(private_key)
        public_key_serialized = pickle.dumps(public_key)
            
            # Save details to the model
        UploadFileModel.objects.create(
            uploaderemail=email,
            file=temp_file_path,  # Store just the filename or path depending on your model setup
            keyword=keyword,
            file_name=filename,
            privatekey=private_key_serialized,
            Publickey=public_key_serialized,
            encrypted_data=file_data
        ).save()
        messages.success(request, 'File Uploaded Successfully!')
        return redirect('uploadfile')
            

        # decrypt_file('encrypted_example.bin', 'decrypted_example.txt', private_key, public_key)
    return render(request, 'uploadfile.html',{'login':login})

def viewfiles(request):
    # RequestFileModel.objects.all().delete()
    login =request.session['login']
    email =request.session['email']
    files = UploadFileModel.objects.all()
    return render(request, 'viewfiles.html',{'data':files,'login':login,'email':email})


def datastatus(request):
    login =request.session['login']
    email =request.session['email']
    files = UploadFileModel.objects.filter(uploaderemail=email)
    return render(request, 'datastatus.html',{'data':files,'login':login})


def requestfiles(request, id):
    login =request.session['login']
    email =request.session['email']
    req = UploadFileModel.objects.get(id=id)
    RequestFileModel.objects.create(
        uploaderemail=req.uploaderemail,
            file=req.file,  
            keyword=req.keyword,
            file_name=req.file_name,
            privatekey=req.privatekey,
            Publickey=req.Publickey,
            encrypted_data=req.encrypted_data,
            email=email
    ).save()
    messages.success(request, 'File Requested Successfully!')
    return redirect('viewfiles')

def filerequests(request):
    login =request.session['login']
    email =request.session['email']
    files = RequestFileModel.objects.filter(uploaderemail=email,status='pending')
    return render(request, 'filerequests.html',{'data':files,'login':login})

def acceptrequest(request, id):
    login =request.session['login']
    email =request.session['email']
    req = RequestFileModel.objects.get(id=id)
    file = req.file.path
    private_key =pickle.loads(req.privatekey)
    public_key = pickle.loads(req.Publickey)
    temp_file_path = os.path.join('static', 'DecrptedFiles', req.file_name)
    decrypt_file(file, temp_file_path, private_key, public_key)
    req.status='Decrypted'
    req.file=temp_file_path
    req.save()
    messages.success(request, 'File Accepted and Decrypted Successfully!')
    req.save()
    return redirect('filerequests')


def adminlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if email == 'admin@gmail.com' and password == 'admin':
            request.session['login'] = 'admin'
            request.session['email'] = email
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials!')
            return redirect('adminlogin')
    return render(request, 'adminlogin.html')


def viewallfiles(request):
    login =request.session['login']
    files = UploadFileModel.objects.all()
    return render(request, 'viewallfiles.html',{'data':files,'login':login})


def viewrequests(request):
    login =request.session['login']
    files = RequestFileModel.objects.filter(status='Decrypted',key='')
    return render(request, 'viewrequests.html',{'data':files,'login':login})

def generatekey(request,id):
    key = random.randint(100000,999999)
    req = RequestFileModel.objects.get(id=id)
    # print(req.key)
    req.key=key
    req.save()
    email_subject = 'Key Details'
    email_message = f'Hello {req.email},\n\nWelcome To Our Website!\n\nHere are your Key details:\nEmail: {req.email}\nKey: {req.key}\n\nPlease keep this information safe.\n\nBest regards,\nYour Website Team'
    send_mail(email_subject, email_message, 'hietechsolutions@gmail.com', [req.email])
   
    messages.success(request, 'Key Generated Successfully!')
    return redirect('viewrequests')

def filetransactions(request):
    login =request.session['login']
    data = RequestFileModel.objects.filter(~Q(key=''),status='Decrypted')
    return render(request, 'filetransactions.html',{'data':data,'login':login})

def viewresponses(request):
    login =request.session['login']
    email =request.session['email']
    data = RequestFileModel.objects.filter(~Q(key=''),status='Decrypted',email=email)
    return render(request, 'viewresponses.html',{'data':data,'login':login})

import secrets
from django.http import HttpResponse

def downloadfile(request, id):
    key = secrets.token_hex(4)

    print("Generated Key:", key)   # shows in VS Code terminal

    return HttpResponse(f"File downloaded. Key: {key}")


def downloadfile(request, id):
    login = request.session.get('login')
    email = request.session.get('email')

    context = RequestFileModel.objects.get(id=id)

    # STEP 1: Generate key when page is opened (GET request)
    if request.method == 'GET':
        key = secrets.token_hex(4)  # 8-character key like 7b392b7c

        print("Generated Key:", key)  # shows in VS Code terminal

        # store key in session so we can verify later
        request.session['download_key'] = key

        return render(request, 'download.html', {
            'login': login,
            'email': email,
            'id': id
        })

    # STEP 2: when user submits key (POST request)
    if request.method == 'POST':
        entered_key = request.POST['Key']
        stored_key = request.session.get('download_key')

        if entered_key == stored_key:
            file_path = context.file.path
            file_name = context.file_name.split('/')[-1]

            response = FileResponse(
                open(file_path, 'rb'),
                as_attachment=True,
                filename=file_name
            )
            return response
        else:
            messages.error(request, 'You entered correct key')
            return redirect('downloadfile', id)
