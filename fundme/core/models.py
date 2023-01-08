from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    # phone = PhoneNumberField(unique = True, null = False, blank = False)
    phone = models.CharField(max_length=20)
    card_number=models.CharField(max_length=20)
    image=models.ImageField(upload_to='photo/%y/%m/%d',null=True)


class Campaign(models.Model):
    title=models.CharField(max_length=50)
    details=models.TextField(max_length=255)
    image=models.ImageField(upload_to='photo/%y/%m/%d',null=True)
    required_fund=models.PositiveIntegerField()
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name="campaigns")


class Investment(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.PROTECT,related_name="investments")
    campaign=models.ForeignKey(Campaign,on_delete=models.CASCADE,related_name="investments")
    investment_value=models.PositiveIntegerField()
    date_of_investment=models.DateField(auto_now_add=True)