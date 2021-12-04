from django.contrib import admin
from .models import User, OTP


# Register your models here.
@admin.register(User)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ["id", 'name','email', 'phone',"address"]


@admin.register(OTP)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ["id", 'email','otp']