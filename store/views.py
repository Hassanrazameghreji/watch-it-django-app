from django.shortcuts import redirect, render
from django.http import JsonResponse,HttpResponsePermanentRedirect

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from .forms import RegisterForm
from .models import *
from .utils import cartData, guestOrder

import json
import datetime

# Create your views here.
def registerUser(request):
    if request.user.is_authenticated:
            return redirect('home')
    form = RegisterForm()
    if request.POST:
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            Customer.objects.create(user=user, name=firstname+' '+lastname, email=email)
            login(request,user)
            return redirect('home')
    context = {
        'form':form
    }    
    return render(request, 'store/auth/register.html',context)

def loginUser(request):
    if request.user.is_authenticated:
            return redirect('home')
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
            username = user.username

            user_auth = authenticate(request, username=username, password=password)
            if user_auth is not None:
                login(request,user_auth)
                return redirect('home')
            else:
                messages.error(request,'Invalid Password')
        except:
            messages.error(request, 'Account Does Not Exists!')

    return render(request, 'store/auth/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all().order_by('id')
    context = {
        'products':products,
        'cartItems':cartItems
    }
    return render(request, 'store/main/home.html', context)

def cart(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    context={
        'items':items,
        'order': order,
        'cartItems':cartItems
    }
    return render(request,'store/main/cart.html', context)

def checkout(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    context={
        'items':items,
        'order': order,
        'cartItems':cartItems
    }
    return render(request,'store/main/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    ProductId = data['productId']
    action = data['action']
    
    customer = request.user.customer
    product = Product.objects.get(id=ProductId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item Was Added', safe=False)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def processOrder(request):
    transaction_id = "T"+datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)


    total = data['form']['total']
    order.transaction_id = transaction_id
    if int(total) == int(order.get_cart_total):
            order.complete = True
    order.save()

    ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zip']
        )

    return JsonResponse('Payment Completed', safe=False)