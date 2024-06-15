from django.shortcuts import render
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from master.models import Item
from django.urls import reverse
import random
from django.core.mail import send_mail
# Create your views here.
def home(request):
    return render(request,'home.html')

def user_regitration(request):
    EUFO= CostumerForm()
    d={'EUFO':EUFO}
    if request.method == 'POST':
        UFDO=CostumerForm(request.POST)
        if UFDO.is_valid():
            pw=UFDO.cleaned_data['password']
            MFDO=UFDO.save(commit=False)
            MFDO.set_password(pw)
            MFDO.save()
            return HttpResponse('You are registered to Zomato')
    return render(request,'user_regitration.html',d)

def user_login(request):
    if request.method == 'POST':
        un=request.POST.get('un')
        pw=request.POST.get('pw')
        UO=User.objects.get(username=un)
        AMO=authenticate(username=un,password=pw)
        if AMO and AMO.is_active:
            login(request,AMO)
            request.session['username']=un
            if UO.is_staff :
                return render (request,'additem.html')
            return HttpResponseRedirect(reverse('home'))
    return render (request,'login.html')

def go_to_menu(request):
    d={'items':Item.objects.all()}
    return render(request,'user_menu.html',d)

def user_logout(request):
    logout(request)
    return render (request,'home.html')

def add_cart(request,pk):
    if request.method=='POST':
        qty=request.POST.get('qty')
        IO=Item.objects.get(item_id=pk)
        un=User.objects.get(username=request.session['username'])
        print(IO,un)
        try:
            CO=Cart.objects.get(cart_id=un,name=IO)
            CO.name==IO
            CO.qty+=int(qty)
            CO.save()
        except Cart.DoesNotExist:
            CO=Cart(cart_id=un,price=IO.item_price,qty=qty,name=IO.item_name)
            CO.save()
        return HttpResponseRedirect(reverse('cart'))
    return HttpResponseRedirect(reverse('go_to_menu'))


# def cart(request):
#     CO=Cart.objects.get(cart_id=request.sessio['username'])
#     d={'CO':CO}
#     for i in d:
#         i['total']=i['qty']*i['price']    
#     return render(request,'cart.html',d)
def forget_pw(request):
    if request.method == 'POST':
        un=request.POST.get('un')
        cpw=request.POST.get('cpw')
        pw=request.POST.get('pw')
        UO=User.objects.get(username=un)
        otp=random.randint(100000,999999)
        
        if UO:
            if cpw==pw:
                send_mail('OTP to Change Your Passwor',str(otp),'abhirammohapatra25@gmail.com',[UO.email],fail_silently=True)
                request.session['otp']=str(otp)
                request.session['npw']=cpw
                request.session['username']=un
                return HttpResponseRedirect(reverse('otp'))
            return HttpResponse('Re-Confirm Password')
        return HttpResponse('USER NOT FOUNd')
    return render (request,'forget_pw.html')

def change_password(request):
    if request.method == 'POST':
        cpw=request.POST.get('cpw')
        pw=request.POST.get('pw')
        UO=User.objects.get(username=request.session['username'])
        d={'UO',UO}
        otp=random.randint(100000,999999)
        if cpw==pw:
            send_mail('OTP to Change Your Passwor',str(otp),'abhirammohapatra25@gmail.com',[UO.email],fail_silently=True)
            request.session['otp']=str(otp)
            request.session['npw']=cpw
            return HttpResponseRedirect(reverse('otp'))
    return render (request,'change_password.html',d)

def otp(request):
    if request.method == 'POST':
        
        otp=request.POST.get('otp')
        if otp==request.session['otp']:
            UO=User.objects.get(username=request.session['username'])
            UO.password=request.session['npw']
            UO.save()
            return HttpResponse('Password is changed')
    return render(request,'otp.html')

def cart(request):
    Grand_total=0
    UO=Cart.objects.all()
    CO=list(filter(lambda i: i.cart_id.username== request.session['username'], UO))
    for i in CO:
        i.total=i.qty*i.price
        Grand_total+= i.total
    d={'CO':CO,'Grand_total':Grand_total}
    return render(request,'cart.html',d)


def Buy(request):
   UO=Cart.objects.all()
   try:
        CO=list(filter(lambda i: i.cart_id.username== request.session['username'], UO))
        for i in CO:
            i.delete()
            i.save()
   except:
       print('No cart present')
   return HttpResponse('YOUr Order is placed "Thank You For Shoping With Us"')