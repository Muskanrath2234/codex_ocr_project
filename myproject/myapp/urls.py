from django.urls import path
from .views import *
urlpatterns = [
  path('home/', home, name="home"),
  path('Profile_edit/',Profile_edit,name="Profile_edit"),
  path('register/',register_user,name="register"),
  path('', login_user, name="login"),
  path('logout/',logout_user,name="logout"),

  path('upload_aadhar/',upload_aadhar,name='upload_aadhar'),
  path('result/', result, name='result'),

  path('upload_pan_card', upload_pan_card, name='upload_pan_card'),
  path('su/', success_page, name='success_page'),

  path('profile/', profile_view, name='profile_view'),
  path('contact/', contact, name='contact'),



]