from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Profile(models.Model):
    role = models.CharField(max_length=100)
    date_of_birth = models.DateField(max_length=20)
    tag_line = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='images')
    user = models.OneToOneField(User, on_delete= models.CASCADE)


    def __str__(self):
        return self.user.username

# class User(models.Model):
#     username = models.CharField(max_length=100)
#     password = models.CharField(max_length=50)


    

class Blog(models.Model):
    title = models.CharField(max_length=100)
    Meta_descreption = models.CharField(max_length=500)
    tag = models.CharField(max_length=100)
    content = models.CharField(max_length=700,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    create_date = models.DateField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    

    def __str__(self):
        return self.title


