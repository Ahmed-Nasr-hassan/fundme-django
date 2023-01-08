from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

import requests
from django.conf import settings
from rest_framework import viewsets
from .forms import SignupForm, LoginForm
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Campaign, Customer, Investment
from .serializers import CampaignSerializer, CustomerSerializer, InvestmentSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Make a request to the /auth/users/ endpoint to create a new user
            response = requests.post(settings.BASE_URL + '/auth/users/', json={'email': email,'username': username, 'password': password})
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
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(settings.BASE_URL + 'core/customer')
            else:
                return render(request, 'core/login.html', {'form': form, 'error': 'Invalid username or password'})
        else:
            return render(request, 'core/login.html', {'form': form, 'error': 'Invalid form'})
    else:
        form = LoginForm()
        return render(request, 'core/login.html', {'form': form})



# def login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']

#             # Make a request to the /auth/jwt/create endpoint to get the JWT
#             response = requests.post(settings.BASE_URL +'/auth/jwt/create', json={'username': username, 'password': password})
#             print(response)
#             if response.status_code == 200:
#                 # Extract the JWT from the response
#                 jwt = response.json()
#                 refresh_token = jwt['refresh']
#                 access_token = jwt['access']
#                 # Store the JWT in the user's session or a cookie
#                 request.session['refresh_token'] = refresh_token
#                 request.session['access_token'] = access_token
#                 request.session['Authorization'] = f' Bearer {access_token}'
#                 request.META['Authorization'] = f' Bearer {access_token}'
#                 headers = {
#                     "Authorization": f" Bearer {access_token}"
#                 }

#                 print(access_token)                
#                 # print(response.cookies.get('access_token'))
#                 # Redirect the user to the desired page
#                 response = redirect(settings.BASE_URL + 'core/customer',headers=headers)
#                 response.set_cookie('Authorization', f'Bearer {access_token}')
#                 response.set_cookie('refresh_token', refresh_token)
#                 response.set_cookie('access_token', access_token)
#                 return response
#                 # return redirect('core/home.html')
#             else:
#                 # Handle unsuccessful request (e.g., invalid credentials)
#                 pass
#     else:
#         form = LoginForm()

#     return render(request, 'core/login.html', {'form': form})

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # authentication_class = (JWTAuthentication,)
    permission_classes = [IsAuthenticated]

class InvestmentViewSet(viewsets.ModelViewSet):
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer
    permission_classes = [IsAuthenticated] 
    # authentication_class = (JWTAuthentication,)

class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated] 
    # authentication_class = (JWTAuthentication,)

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