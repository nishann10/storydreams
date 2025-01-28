from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    phone_number=models.IntegerField(null=True,blank=True)
    def __str__(self):
        return self.username
class category(models.Model):
    category_name=models.CharField(max_length=100)
    def __str__(self):
        return self.category_name

class book(models.Model):
    name=models.CharField(max_length=100)
    quantity=models.IntegerField()
    category=models.ForeignKey(category,on_delete=models.CASCADE)
    publisher=models.CharField(max_length=100)
    published_date=models.DateField()
    price=models.IntegerField(null=True)
    auther=models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.name
class booking(models.Model):
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    book_id=models.ForeignKey(book,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    status=models.CharField(max_length=100)
    payment=models.CharField(max_length=100)
    total_amount=models.IntegerField()

    
