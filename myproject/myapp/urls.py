from django.urls import path
from .views import *
urlpatterns = [
  path('home/', home, name="home"),
  path('Profile_edit/',Profile_edit,name="Profile_edit"),
  path('register/',register_user,name="register"),
  path('', login_user, name="login"),
  path('logout/',logout_user,name="logout"),

  path('upload_document/',upload_document,name='upload_document'),
  path('result/', result, name='result'),

]