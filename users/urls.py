from django.urls import path
from . import views


urlpatterns = [
    path('',views.userLogin,name='userLogin'),
    path('signup/',views.userSignup,name='userSignup'),
    path('home/',views.userHome,name='userHome'),
    path('logout/',views.userLogout,name='userLogout'),
    
]
