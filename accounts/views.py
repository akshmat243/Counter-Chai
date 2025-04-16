from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomUser, UserRoles, Product
from .forms import AddVendorForm, AddCounterForm, AddSuperAdminForm, ProductForm, AddCustomerForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def register_view(request):
    if request.method =='POST':
        form = AddSuperAdminForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = UserRoles.SUPERADMIN
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = AddSuperAdminForm()
        return render(request, 'register.html', {'form':form})
            
            

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'username or/ password is invalid!!!')
            return redirect('login')
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form':form})
        
        
def logout_view(request):
    logout(request)
    return redirect('login')
  
  
@login_required(login_url = 'login')
def dashboard_view(request):
    vendors = CustomUser.objects.all()
    user = request.user
    products = []

    if user.role == 'customer':
        counter = user.created_by  
        if counter:
            products = Product.objects.filter(user=counter)
    elif user.role == 'counter':
        products = Product.objects.filter(user=user)
    else:
        products = Product.objects.all()
    return render(request, 'dashboard.html', {'vendors':vendors, 'products':products})

def is_superadmin(user):
    return user.is_authenticated and user.role == UserRoles.SUPERADMIN

@login_required
@user_passes_test(is_superadmin)
def add_vendor(request):
    if request.method == 'POST':
        form = AddVendorForm(request.POST)
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.role = UserRoles.VENDOR  
            vendor.set_password(form.cleaned_data['password'])
            vendor.created_by = request.user
            vendor.save()
            return redirect('dashboard')  
        else:
            return render(request, 'add_vendor.html', {'form': form})
    else:
        form = AddVendorForm()
        return render(request, 'add_vendor.html', {'form': form})
    
def can_add_teacounter(user):
    return user.is_authenticated and (user.role == UserRoles.SUPERADMIN or user.role == UserRoles.VENDOR)

@login_required
@user_passes_test(can_add_teacounter)
def add_counter(request):
    if request.method == 'POST':
        form = AddCounterForm(request.POST)
        if form.is_valid():
            teacounter = form.save(commit=False)
            teacounter.role = UserRoles.COUNTER
            teacounter.set_password(form.cleaned_data['password'])
            teacounter.created_by = request.user
            teacounter.save()
            return redirect('dashboard')  
    else:
        form = AddCounterForm()
    return render(request, 'add_counter.html', {'form': form})

def can_add_product_user(user):
    return user.is_authenticated and (user.role == UserRoles.COUNTER)

@login_required
@user_passes_test(can_add_product_user)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('dashboard')
    else:
        form = ProductForm()
        return render(request, 'add_product.html', {'form': form})
    

@login_required
@user_passes_test(can_add_product_user)
def add_customer(request):
    if request.method == 'POST':
        form = AddCustomerForm(request.POST)
        if form.is_valid():
            teacounter = form.save(commit=False)
            teacounter.role = UserRoles.CUSTOMER
            teacounter.set_password(form.cleaned_data['password'])
            teacounter.created_by = request.user
            teacounter.save()
            return redirect('dashboard')  
    else:
        form = AddCustomerForm()
    return render(request, 'add_customer.html', {'form': form})















@login_required
def product_view(request):
    user = request.user
    if user.role == 'counter':
        products = Product.objects.filter(user=user)
        return render(request, 'menu.html', {'products': products})
    else:
        return render(request, 'menu.html')



import qrcode
from io import BytesIO
from django.http import HttpResponse

def generate_qr(request):
    url = 'http://127.0.0.1:8000/account/products/'

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    return HttpResponse(buffer, content_type='image/png')