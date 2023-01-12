from rest_framework import serializers
from .models import Campaign,Customer,Investment
from djoser.serializers import UserCreateSerializer


class CustomUserCreateSerializer(UserCreateSerializer):  
    class Meta(UserCreateSerializer.Meta):
        fields = '__all__'
        fields = ['id','first_name','last_name','username','email','password']
    


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = '__all__'