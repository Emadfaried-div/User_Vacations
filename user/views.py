from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView , DetailView , View, CreateView, FormView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm , UserUpateForm
# Create your views here.


def register(request):
    if request.method == "POST":
        form =CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user-login")
    else:
        form =CreateUserForm()
    return render(request,"user/register.html",{"form":form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        print("we have login post")
        if form.is_valid():
            user=form.get_user()

            login(request, user)
            
            return redirect ("home")
        
            
    else:
       form = AuthenticationForm()
    return render (request,'user/login.html',{'form':form})


#





class CustomerLogoutView(View):
    def get(self,request):
        logout(request)
        return redirect("home")



    