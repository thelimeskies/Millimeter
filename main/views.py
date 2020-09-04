from django.contrib.auth.models import Group
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from .models import MyUser
from .forms import CreateUserForm
from .decorator import unauthenticated_user, admin_only, user_only


# Create your views here.

@login_required(login_url='login')
@admin_only
def console(request):
    return render(request, 'admin/dashboard.html')

@login_required(login_url='login')
@admin_only
def billing(request):
    return render(request, 'admin/billing.html')

@login_required(login_url='login')
@admin_only
def new_meter(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('meter_id')
            messages.success(request, 'Account was created for ' + username)

            group = Group.objects.get(name='User')
            MyUser.groups.add(group)

            return redirect('login')

    context = {'form': form}
    return render(request, 'admin/new_user.html', context)

@login_required(login_url='login')
@admin_only
def view_meters(request):
    meters = MyUser.objects.all()
    return render(request, 'admin/meters.html', {'meters': meters})

@unauthenticated_user
def loginpage(request):
    if request.method == 'POST':
        meter_id = request.POST.get('meter_id')
        password = request.POST.get('password')

        user = authenticate(request, meter_id=meter_id, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'index.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@user_only
def dashboard(request):
    return render(request, 'users/dashboard.html')
