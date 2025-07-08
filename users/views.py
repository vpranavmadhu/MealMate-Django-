from django.shortcuts import render, redirect
from .models import Customer
from django.http import HttpResponse
from delivery.models import Restaurant

# Create your views here.
def index(request):
    return render(request,'users/sign_in.html')

def signin(request):
    return render(request,'users/sign_in.html')

def signup(request):
    return render(request,'users/sign_up.html')

def handle_signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        role = request.POST.get("role")
        try:
            cus = Customer.objects.get(username=username)
            return render(request, 'users/sign_up.html', {'error': 'username already found'})
        except Customer.DoesNotExist:
            cus = Customer(username = username, password = password, email = email, mobile = mobile, address = address, role=role)
            cus.save()
        return render(request, 'users/sign_in.html')
    else:
        return HttpResponse("Invalid request")
        
def handle_signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("Username:", username)   # Debug check
        print("Password:", password)  #Debug check
        
        cus = Customer.objects.filter(username=username, password=password).first()
        li = Restaurant.objects.all()

        if cus:
            if cus.role.lower() == 'vendor':
                return render(request, 'users/admin_home.html', {'li': li})
            else:
                print("Found customer:", cus)
                return render(request, 'users/cus_home.html', {'username': username, 'li': li})
        else:
            return render(request,'users/sign_in.html',{'error':'Invalid username or password'})

    else:
        return HttpResponse("Invalid Request")
    
def cus_home(request,username):
    li = Restaurant.objects.all()
    return render(request, 'users/cus_home.html', {'li':li, 'username': username})

def admin_home(request):
    li = Restaurant.objects.all()
    return render(request,'users/admin_home.html',{"li":li}) 
