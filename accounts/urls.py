from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

from .views import logout_view


app_name='accounts'

urlpatterns = [
    path('signup/',views.signup,name='signup'), 
    path('profile/',views.profile,name='profile'), 
    path('profile/edit',views.profile_edit,name='profile_edit'),
    path('logout/', logout_view, name='logout'),



    
]