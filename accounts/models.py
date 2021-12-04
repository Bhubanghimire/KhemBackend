from __future__ import unicode_literals
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.transaction import atomic
from common.models import ConfigChoice
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        try:
            with atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except Exception as e:
            raise e

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=40, unique=True)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    profile = models.ImageField(upload_to='media/user/profile/')
    address = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    user_type = models.ForeignKey(ConfigChoice, on_delete=models.CASCADE, null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "User"

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

    def __str__(self):
        return self.name


User = get_user_model()


class OTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=255)

    def __str__(self):
        return str(self.email)

    class Meta:
        verbose_name_plural = "OTP"


class PasswordReset(models.Model):
    token = models.IntegerField()
    generated_date = models.DateTimeField(auto_now=True)
    email = models.EmailField()
