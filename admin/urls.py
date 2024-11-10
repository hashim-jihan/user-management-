from django.urls import path
from . import views


urlpatterns = [
    path('',views.adminLoin,name='adminLogin'),
    path('admin_home/',views.adminHome,name='adminHome'),
    path('userlist/',views.usersList,name='usersList'),
    path('userupdate/<int:user_id>',views.userUpdate,name='userUpdate'),
    path('adduser/',views.addUser,name='addUser'),
    path('deleteuser/<int:user_id>/',views.deleteUser,name='deleteUser'),
    path('adminlogout/',views.adminLogout,name='adminLogout')

   
]

