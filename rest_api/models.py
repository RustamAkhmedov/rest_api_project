from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=150) 
    body = models.TextField(blank= True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now= True)
    is_published= models.BooleanField(default=True)
    category = models.ForeignKey("Category", on_delete=models.PROTECT, null= True, related_name= "posts") 
    autor = models.ForeignKey(User, verbose_name="autor", on_delete=models.CASCADE)

    def __str__(self):
        return self.title 
    

    #class Meta:
    #    ordering = ["time_update"]
        

class Category(models.Model):
    title = models.CharField(max_length=150) 

    def __str__(self):
        return self.title 



class Phone(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField(blank=True)
    model = models.ForeignKey("PhoneModel",on_delete=models.PROTECT, related_name= "phones")


class PhoneModel(models.Model):
    title = models.CharField(max_length=150) 

    def __str__(self):
        return self.title 
