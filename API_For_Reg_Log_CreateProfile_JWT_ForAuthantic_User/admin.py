from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = ['user','role','date_of_birth','tag_line','profile_pic']


admin.site.register(Blog)
