"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from .views import *

urlpatterns = [
        # path('AdminViews/', AdminViews.as_view()),
    # path('AdminViews/<int:pk>/', AdminViews.as_view()),
    path('staff/', StaffViews.as_view(), name='staff'),
    path('staff/<int:pk>/', StaffViews.as_view()),

    path('clients/', ClientView.as_view()),
    path('clients/<int:pk>/', ClientView.as_view()),
    path('client-login/', ClientAPIView.as_view(), name='client-login'),
    path('staff-login/', StaffLoginAPIView.as_view(), name='staff-login'),
    # path('AdminRegister/', AdminRegister.as_view()),
    path('AdminLogin/', AdminLogin.as_view()),
    path('Admin/<int:pk>/', AdminLogin.as_view()),
    path('tasks/', TaskAPIView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskAPIView.as_view(), name='task-detail-update-delete'),
    path('income-tax/', IncomeTaxAPIView.as_view(), name='income-tax-list-create'),
    path('income-tax/<int:pk>/', IncomeTaxAPIView.as_view(), name='income-tax-detail'),
    path('gst/', GstAPIView.as_view(), name='gst-list-create'),
    path('gst/<int:pk>/', GstAPIView.as_view(), name='gst-detail'),
    path('kyc/', KycAPIView.as_view(), name='kyc-list'),
    path('kyc/<int:pk>/', KycAPIView.as_view(), name='kyc-detail'),
    path('kyc/<int:pk>/partners/<int:index>/', UpdatePartnerAPIView.as_view(), name='update-partner'),
    path('tds/', TdsAPIView.as_view(), name='tds-list-create'),       # GET all / POST new
    path('tds/<int:pk>/', TdsAPIView.as_view(), name='tds-detail'),
    path('otherdocs/', OtherDocAPIView.as_view(), name='otherdocs-list-create'),
    path('otherdocs/<int:pk>/', OtherDocAPIView.as_view(), name='otherdocs-detail'),
    ]