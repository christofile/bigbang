from django.db import models

# Create your models here.
class User(models.Model):
    email = models.CharField(max_length=128)
    password = models.CharField(max_length=32)
    status = models.CharField(max_length=32)
    create_time = models.DateTimeField()
    group = models.CharField(max_length=32)
    account = models.IntegerField()

class order(models.Model):
    user_id = models.IntegerField()
    account_id = models.IntegerField()  
    lab_id = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=32)
    mail_to_user = models.TextField()

class lab(models.Model):
    name = models.CharField(max_length=256)
    type = models.CharField(max_length=64)
    hypervisor_ip = models.IPAddressField()
    status = models.CharField(max_length=32)
    create_time = models.DateTimeField()
    


