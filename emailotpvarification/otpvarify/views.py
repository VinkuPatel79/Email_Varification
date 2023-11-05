from django.shortcuts import render,redirect
from django.views.generic import View
from .form import *
from django.contrib import messages
from django.contrib.auth import authenticate,login
from .models import Profile
from django.core.mail import send_mail
# Create your views here.
from django.views import View
import uuid

from django.conf import settings
class Home(View):
    def get(self,request):
        return render(request, 'home.html')

def send_email_after_registration(email,token):
    subject="Varify Email"
    messages=f"click link varify your account http://127.0.0.1:8000/account-varify/{token}"
    from_email=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(message=messages,subject=subject,from_email=from_email,recipient_list=recipient_list)
    
class SignupView(View):
    def get(self, request):
        fm = SignUpForm()
        return render(request, 'signup.html',{'form':fm})
    def post(self, request):
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            new_user=fm.save()
            uid=uuid.uuid4()
            pro_obj=Profile(user=new_user,token=uid)
            pro_obj.save()
            send_email_after_registration(new_user.email,uid)
            messages.success(request, 'Account created successfully and Check your email for varification')
            return redirect('/signup')
        else:
            return render(request, 'signup.html',{'form':fm})

def account_verify(request,token):
    pf=Profile.objects.filter(token=token).first()
    pf.verify = True
    pf.save()
    messages.success(request,"Your account is varified")
    return redirect('/signup/')
    
class MylonginView(View):
    def get(self,request):
        fm = MyLoginForm()
        return render(request,"login.html",{'form':fm})
    def post(self,request):
        fm=MyLoginForm(request,data=request.POST)
        if fm.is_valid():
            username=fm.cleaned_data['username']
            password=fm.cleaned_data['password']
            user=User.objects.get(username=username)
            pro=Profile.objects.get(user=user)
            user=authenticate(request,username=username,password=password)
            if pro.verify:
                login(request,user)
                return redirect("/")
            else:
                messages.warning(request,"your account is not varified,Please check your email and varify your account")
                return redirect("/login")            
        else:
            return render(request,"login.html",{'form':fm})
