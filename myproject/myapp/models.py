from django.db import models
from django.contrib.auth.models import User


class PANCard(models.Model):
    image = models.ImageField(upload_to='static/images')

    def __str__(self):
        return f"PAN Card {self.id}"

class UploadFiles(models.Model):
    file = models.FileField()

    def __str__(self):
        return f"aadhar card {self.id}"





class Profile(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(null=True,max_length=200,blank=True)
    DOB = models.DateField(null=True,max_length=10,blank=True)
    Pan = models.CharField(null=True,max_length=10,blank=True)
    Fathers_Name  = models.CharField(null=True,max_length=200,blank=True)

    aadhar_gender = models.CharField(null=True, blank=True, max_length=10)
    aadhar_number = models.IntegerField(null=True, blank=True,max_length=12)
    aadhar_Phone= models.PositiveIntegerField(null=True, blank=True,max_length=10)
    aadhar_address = models.TextField(null=True, blank=True)
    pin= models.PositiveIntegerField(null=True, blank=True,max_length=6)

    def __str__(self):
        return self.user.username + "'s Profile"



