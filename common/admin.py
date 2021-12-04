from django.contrib import admin
from .models import ConfigChoice, ConfigCategory


# Register your models here.
@admin.register(ConfigCategory)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ["id","type","description"]


@admin.register(ConfigChoice)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ["id","value","description","category"]