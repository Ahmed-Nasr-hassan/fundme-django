from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

import requests
from django.conf import settings
from rest_framework import viewsets
from .forms import SignupForm, LoginForm, ProfileForm, InvestmentForm, CampaignForm
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Campaign, Customer, Investment
from .serializers import CampaignSerializer, CustomerSerializer, InvestmentSerializer

current_user = None
def logout_view(request):
    logout(request)
    return redirect(settings.BASE_URL + 'login')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Make a request to the /auth/users/ endpoint to create a new user
            response = requests.post(settings.BASE_URL + '/auth/users/', json={'first_name': first_name,\
                                                                                'last_name': last_name,\
                                                                                'email': email,\
                                                                                'username': username,\
                                                                                'password': password})
            if response.status_code == 201:
                # Redirect the user to the login page
                return redirect('/login')
            else:
                # Handle unsuccessful request (e.g., email already in use)
                pass
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        user = request.user
        global current_user
        current_user = request.user
        print(current_user)
        login(request, user)
        return redirect(settings.BASE_URL + 'create-profile')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(settings.BASE_URL + 'create-profile')
            else:
                # Return an 'invalid login' error message.
                return render(request, 'core/login.html', {'form': form, 'error': 'Invalid login'})
        else:
            # Return a 'form is invalid' error message.
            return render(request, 'core/login.html', {'form': form, 'error': 'Form is invalid'})
    else:
        form = LoginForm()
        return render(request, 'core/login.html', {'form': form})



class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    # use request.user.is_authinticated 

   
 
    

class InvestmentViewSet(viewsets.ModelViewSet):
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)


class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)


    # def list(self, request):
    #         # ...
    #         return render(request, 'core/list.html')

    # def list(self, request):
    #     queryset = User.objects.all()
    #     serializer = UserSerializer(queryset, many=True)
    #     return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     queryset = User.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)

    # def create(self, request):
    #     pass

    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass

def createCustomer(request) :
    customer = ProfileForm(request.POST,request.FILES)
    customerData = customer
    if customer.is_valid():
        profile_data = customer.cleaned_data
        profile_data['user'] = request.user
        profile_obj, created = Customer.objects.update_or_create(user=request.user, defaults=profile_data)
        # return render(request,'core/profile.html',{"profile_obj":profile_obj})
        return redirect('/profile')

    return render(request,'core/create-profile.html',{"form":customer})

def showCustomer(request):
    if Customer.objects.filter(user=request.user).exists():
        customer = Customer.objects.get(user=request.user)
        return render(request, 'core/profile.html', {"customer": customer})
    else:
        return redirect('/create-profile')

def updateCustomer(request):
    if current_user is None:
        return redirect('/login')

    customer = Customer.objects.get(pk=request.user.id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            customer_dict={'customers': Customer.objects.all()}
            return render(request,'core/profile.html',customer_dict)
    else:
        form = ProfileForm(instance=customer)
    return render(request, 'core/update_profile.html', {'form': form})


def create_campaign(request):
    if current_user is None:
        return redirect('/login')
    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.customer = Customer.objects.get(pk=request.user.id)
            campaign.save()
            return redirect('campaign_detail', campaign.id)
    else:
        form = CampaignForm()
    return render(request, 'campaigns/create_campaign.html', {'form': form})

def campaign_detail(request, campaign_id):
    if current_user is None:
        return redirect('/login')
    campaign = Campaign.objects.get(id=campaign_id)
    return render(request, 'campaigns/campaign_detail.html', {'campaign': campaign})

def campaign_list(request):
    if current_user is None:
        return redirect('/login')
    campaigns = Campaign.objects.filter(customer=Customer.objects.get(pk=request.user.id))
    return render(request, 'campaigns/campaign_list.html', {'campaigns': campaigns})

def update_campaign(request, campaign_id):
    if current_user is None:
        return redirect('/login')
    campaign = Campaign.objects.get(id=campaign_id)
    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES, instance=campaign)
        if form.is_valid():
            form.save()
            return redirect('campaign_detail', campaign.id)
    else:
        form = CampaignForm(instance=campaign)
    return render(request, 'campaigns/update_campaign.html', {'form': form})

def delete_campaign(request, campaign_id):
    if current_user is None:
        return redirect('/login')
    campaign = Campaign.objects.get(id=campaign_id)
    campaign.delete()
    return redirect('campaign_list')

def home(request):
    campaigns = Campaign.objects.all()
    campaign_count = campaigns.count()
    total_fund = sum(campaign.required_fund for campaign in campaigns)
    context = {
        'campaigns': campaigns,
        'campaign_count': campaign_count,
        'total_fund': total_fund,
    }
    return render(request, 'core/home.html', context)