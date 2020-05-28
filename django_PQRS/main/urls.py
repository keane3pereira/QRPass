from django.urls import path, include
from django.contrib import admin
import main.views as main_views


urlpatterns = [
    path('create_event/', main_views.create_event, name="create_event"),
    path('event/users/', main_views.event_users, name="event_users"),
    path('event/delete_data/', main_views.delete_data, name="delete_data"),
    path('event/undo_register/', main_views.undo_register, name="undo_register"),
    path('register/', main_views.register, name="register"),
    path('customer/', main_views.customer, name="customer"),
    path('event/', main_views.event_details, name="event"),
    path('home/', main_views.home, name="home"),
]
