from django import forms
from .models import Customer,Campaign, Investment

class SignupForm(forms.Form):

    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError(
                "The passwords you entered do not match. Please try again."
            )




class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        # fields = '__all__'
        fields = ['phone','card_number','image']

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['title','details','image','required_fund']

class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ['investment_value']



