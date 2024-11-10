from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login ,logout
from django.views.decorators.cache import cache_control,never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import AdminLogin,AddUser,UpdateUser


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminLoin(request):

    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('adminHome')

    aform=AdminLogin(request.POST or None)

    if request.method == 'POST':
        if aform.is_valid():
            username = aform.cleaned_data.get('username')
            password = aform.cleaned_data.get('password')

            user = authenticate(username = username ,password = password)

            if user is not None and user.is_superuser:
                login(request,user)
                return redirect('adminHome')
            else:
                messages.error(request,'Invalid admin username or password')
            
        
    return render(request,'admin/alogin.html',{
        'aform':aform
    })


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def adminHome(request):
    return render (request,'admin/ahome.html')


@login_required
@never_cache
def usersList(request):

    query =request.GET.get('search')
    users = User.objects.filter(is_superuser = False)
    if query:
        users = User.objects.filter(username__icontains=query)

    return render(request,'admin/userlist.html',{
        'users' : users
    })


def userUpdate(request,user_id):
    user = get_object_or_404(User,id=user_id)
    if request.method == 'POST':
        form = UpdateUser(request.POST)
        
        if form.is_valid():
            user.username  = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.save()
            messages.success(request,'User profile updated successfully.')
            return redirect('usersList')

    else:
        form = UpdateUser(initial={'username' : user.username , 'email' :user.email})


    return render(request,'admin/userupdate.html',{
        'form':form,
        'admin':user
    })


@never_cache
@login_required
def addUser(request):
    if request.method == 'POST':
        form = AddUser(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username = form.cleaned_data['username'],
                email = form.cleaned_data['email'],
                password =form.cleaned_data['password']
                )
            
            messages.success(request, 'User successfully created')
            return redirect ('usersList')
    else:
        form = AddUser()
    
    return render(request,'admin/adduser.html',{
        'form' : form
    })


def deleteUser(request,user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.delete()
        messages.success(request, f'{user.username} has been deleted successfully.')
        return redirect('usersList')
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminLogout(request):
    logout(request)
    return redirect('adminLogin')


