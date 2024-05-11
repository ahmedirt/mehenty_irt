<<<<<<< HEAD
from django.db import models
from django.contrib.auth.models import AbstractUser
||||||| 6bbbf8e
from django.db import models
=======
# from django.db import models
# from django.contrib.auth.models import AbstractUser
>>>>>>> irt23243

<<<<<<< HEAD
# Create your models here.


class User(AbstractUser):
    is_admin= models.BooleanField('Is admin', default=False)
    is_client = models.BooleanField('Is client', default=False)
    is_technicien = models.BooleanField('Is technicien', default=False)
||||||| 6bbbf8e
# Create your models here.
=======
# # Create your models here.


# class User(AbstractUser):
#     is_admin= models.BooleanField('Is admin', default=False)
#     is_client = models.BooleanField('Is client', default=False)
#     is_technicien = models.BooleanField('Is technicien', default=False)
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_admin = models.BooleanField('Is admin', default=False)
    is_client = models.BooleanField('Is client', default=False)
    is_technicien = models.BooleanField('Is technicien', default=False)
    phone_number = models.CharField('Phone Number', max_length=15, blank=True, null=True)
    address = models.TextField('Address', blank=True, null=True)

class Service(models.Model):
    name = models.CharField('Service Name', max_length=100)
    description = models.TextField('Description', blank=True, null=True)
    # Add more fields as needed for services

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    status = models.CharField('Status', max_length=20, default='Pending')
    # Add more fields as needed for requests
>>>>>>> irt23243
