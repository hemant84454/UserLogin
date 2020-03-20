from __future__ import unicode_literals
import uuid
from random import randint


from .managers import MYUserManager
from . regex import *

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as lazy
from django.contrib.auth.base_user import AbstractBaseUser,BaseUserManager


class MyUser(AbstractBaseUser, PermissionsMixin):

    firstName = models.CharField(max_length=30, blank=True, validators=[name_reg,])
    lastName = models.CharField(max_length=30, blank=True, validators=[name_reg,])
    email = models.EmailField(unique=True, validators=[email_reg,])
    otp=models.CharField(max_length=4,null=True,blank=True)
    password = models.CharField(max_length=255, validators=[password_reg, ])
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    is_otpverified = models.BooleanField(default=False)
    otp_verify= models.BooleanField(default=False)

    objects = MYUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def otp_gen(self):
        self.otp=randint(1000,9999)
        self.save()
        print(self.otp)
        return self.otp

    
