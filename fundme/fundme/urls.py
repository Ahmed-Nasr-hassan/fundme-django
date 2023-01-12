"""fundme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import core.views as coreViews
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', coreViews.signup, name='signup'),
    path('login/', coreViews.login_view, name='login'),
    path('logout/', coreViews.logout_view, name='logout'),
    path('profile/', coreViews.showCustomer, name='showcustomer'),
    path('update-profile/', coreViews.updateCustomer, name='updatecustomer'),
    path('create-profile',coreViews.createCustomer,name='create-customer'),
    path('core/', include('core.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('', coreViews.home, name='home'),
    path('create/', coreViews.create_campaign, name='create_campaign'),
    path('<int:campaign_id>/', coreViews.campaign_detail, name='campaign_detail'),
    path('list/', coreViews.campaign_list, name='campaign_list'),
    path('<int:campaign_id>/update/', coreViews.update_campaign, name='update_campaign'),
    path('<int:campaign_id>/delete/', coreViews.delete_campaign, name='delete_campaign'),



]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
