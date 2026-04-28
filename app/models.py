from django.db import models
import os
# Create your models here.
class UserModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=100)
    contact = models.IntegerField()
    address = models.CharField(max_length=100)
    profile = models.FileField(upload_to=os.path.join('static', 'usersprofiles'))
    status = models.CharField(max_length=100,default='pending',null=True)
    

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "UserModel"


class UploadFileModel(models.Model):
    file = models.FileField(upload_to=os.path.join('static', 'Files'),null=True)
    uploaderemail = models.EmailField()
    file_name = models.CharField(max_length=255)  # Store the original file name
    encrypted_data = models.BinaryField()  # Store the encrypted file content
    keyword = models.CharField(max_length=255)  # Store the encrypted keyword
    privatekey = models.BinaryField()  # Store optional attributes (for ABE)
    Publickey = models.BinaryField()
    status = models.CharField(max_length=255,default='Encrypted',null=True)
    

    def __str__(self):
        return self.file_name
    
    class Meta:
        db_table = "UploadFileModel"


class RequestFileModel(models.Model):
    file = models.FileField(upload_to=os.path.join('static', 'DecrptedFiles'))
    uploaderemail = models.EmailField()
    email = models.EmailField()
    file_name = models.CharField(max_length=255)  # Store the original file name
    encrypted_data = models.BinaryField()  # Store the encrypted file content
    keyword = models.CharField(max_length=255)  # Store the encrypted keyword
    privatekey = models.BinaryField()  # Store optional attributes (for ABE)
    Publickey = models.BinaryField()
    status = models.CharField(max_length=255,default='pending')
    key=models.CharField(max_length=255) 
    

    def __str__(self):
        return self.file_name
    
    class Meta:
        db_table = "RequestFileModel"