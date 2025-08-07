from django.db import models
from django.db import models
from django.utils import timezone 

# Create your models here.
class Admin(models.Model):

    Email=models.EmailField(unique=True)
    Password = models.CharField(max_length=150) 

    def __str__(self):
        return self.Email
    

    
class Staff(models.Model):
    name=models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password=models.CharField(max_length=150)
    mobile_No = models.BigIntegerField()

    def __str__(self):
        return self.name
    



class Client(models.Model):
    name=models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password=models.CharField(max_length=150)
    mobile_No = models.CharField(max_length=15, null=False, default='0000000000')
    
    def __str__(self):
        return (self.name)
    


class Task(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=1)
    title = models.TextField()
    description = models.TextField()
    start_date = models.DateField(auto_now_add=True)
    end_date = models.CharField(max_length=250)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    status=models.CharField(max_length=250,default='Pending')

    def __str__(self):
        return self.title

class IncomeTax(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    # staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    year = models.IntegerField()
    document = models.FileField(upload_to='documents/', blank=True, null=True)
    def __str__(self):
        return str(self.client)  

class Gst(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    year = models.IntegerField()
    document = models.FileField(upload_to='documents/', blank=True, null=True)
    def __str__(self):
        return self.client


class Kyc(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    year = models.IntegerField()
    document = models.FileField(upload_to='documents/', blank=True, null=True)
    def __str__(self):
        return self.client
    
class Tds(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    year = models.IntegerField()
    document = models.FileField(upload_to='documents/', blank=True, null=True)
    def __str__(self):
        return self.client



class OtherDoc(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    year = models.IntegerField()
    document = models.FileField(upload_to='documents/', blank=True, null=True)
    def __str__(self):
        return self.client
    