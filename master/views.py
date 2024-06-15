from django.shortcuts import render, get_object_or_404
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate , login,logout
from django.urls import reverse
from django.core.mail import send_mail
import random
# Create your views here.
def home(request):
    return render(request,'home.html')


def masrter_registration(request):
    EMFO=MasterForm()
    d={'EMFO':EMFO}
    if request.method == 'POST':
        MFDO=MasterForm(request.POST)
        if MFDO.is_valid():
            pw = MFDO.cleaned_data['password']
            MMFDO=MFDO.save(commit=False)
            MMFDO.set_password(pw)
            MMFDO.is_staff = True
            MMFDO.save()
            return HttpResponse('Your restaurant is now registered to Zomarto')
    return render(request,'masrter_registration.html',d)

def add_item(request):
    EIFO=ItemForm()
    d={'EIFO':EIFO}
    if request.method == 'POST' and request.FILES:
        IFDO=ItemForm(request.POST, request.FILES)
        if IFDO.is_valid():
            IFDO.save()
            return HttpResponseRedirect(reverse('add_item'))
    return render (request,'addietm.html',d)


def master_login(request):
    if request.method == 'POST':
        un=request.POST.get('un')
        pw=request.POST.get('pw')
        AMO=authenticate(username=un,password=pw)
        if AMO and AMO.is_active and AMO.is_staff:
            login(request,AMO)
            request.session['username']=un
            return HttpResponseRedirect(reverse('home'))
        return HttpResponse("User not found")
    return render (request,'login.html')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def menu(request):
    item=Item.objects.all()
    d={'items':item}
    return render (request,'menu.html',d)


def update(request,pk):
    EIFO= ItemForm()
    d={'EIFO':EIFO}
    IO=get_object_or_404(Item,item_id=pk)
    if request.method == 'POST' and request.FILES:
        IFDO=ItemForm(request.POST,request.FILES, instance=IO)
        if IFDO.is_valid():
         IFDO.save()
         return HttpResponse('Item Updated')               
    return render(request,'addietm.html',d)



def change_password(request):
    if request.method == 'POST':
        cpw=request.POST.get('cpw')
        pw=request.POST.get('pw')
        UO=User.objects.get(username=request.session['username'])
        otp=random.randint(100000,999999)
        if cpw==pw:
            send_mail('OTP to Change Your Passwor',str(otp),'abhirammohapatra25@gmail.com',[UO.email],fail_silently=True)
            request.session['otp']=str(otp)
            request.session['npw']=cpw
            return HttpResponseRedirect(reverse('otp'))
    return render (request,'change_password.html')

def otp(request):
    if request.method == 'POST':
        otp=request.POST.get('otp')
        if otp==request.session['otp']:
            UO=User.objects.get(username=request.session['username'])
            UO.password=request.session['npw']
            UO.save()
            return HttpResponse('Password is changed')
    return render(request,'otp.html')



def delete(request,pk):
    IO=Item.objects.get(item_id=pk)
    IO.delete()
    return HttpResponseRedirect(reverse('menu'))