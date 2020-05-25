"""django_PQRS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
import main.views as main_views
'''
passpatterns = [
    path('', main_views.passes, name="passes"),
    path('delete_data/', main_views.delete_data, name="delete_data"),
]'''

urlpatterns = [
    path('create_event/', main_views.create_event, name="create_event"),
    path('event/users/', main_views.event_users, name="event_users"),
    path('register/', main_views.register, name="register"),
    path('customer/', main_views.customer, name="customer"),
    path('event/', main_views.event_details, name="event"),
    path('home/', main_views.home, name="home"),
    #path('passes/', include(passpatterns)),

]
