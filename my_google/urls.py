from django.urls import path
from . import views 
from .views import extract_text,chatbot




app_name='my_google'

urlpatterns = [
    path('',views.google,name='my_google'),
    path('', views.home_view, name='home'),  # Default home page
    path('extract-text/', extract_text, name='extract_text'),
    path('extract/', views.extract_page, name='extract_page'),
    path('chatbot/', chatbot, name='chatbot'),



    path('gmail/', views.gmail_view, name='gmail'),
    path('images/', views.images_view, name='images'),
]