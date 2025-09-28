
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# REST Framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions

# Models and Forms
from website.models import Product, ProductImage, Cart, CartItem
from website.forms import ProductForm, CustomUserCreationForm

# -------------------------
# CSRF-exempt authentication for API
# -------------------------
class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return

# -------------------------
# Simple API login view
# -------------------------
class SimpleLoginView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        auth_login(request, user)
        return Response({
            "ok": True,
            "user": {"id": user.id, "username": user.username, "is_staff": user.is_staff}
        }, status=status.HTTP_200_OK)

# -------------------------
# Public Views
# -------------------------
def home(request):
    products = Product.objects.all()
    return render(request, "website/home.html", {"products": products})

def product_page(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'website/products/product_page.html', {'product': product})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('product_list')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'website/login.html', {'error': "Invalid credentials"})
    return render(request, 'website/login.html')

@login_required
def logout_view(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('product_list')
        else:
            return render(request, 'website/signup.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'website/signup.html', {'form': form})

def api_product_list(request):
    products = Product.objects.all().values('id', 'name', 'price', 'description')
    return JsonResponse(list(products), safe=False)

# -------------------------
# Dashboard / CRUD Views
# -------------------------
@login_required
def product_list(request):
    products = Product.objects.all().order_by('id')
    return render(request, 'website/products/product_list.html', {'products': products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'website/products/add_product.html', {'form': form})

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product {product.name} updated successfully!")
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'website/products/add_product.html', {'form': form, 'product': product})

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, f"Product {product.name} deleted.")
    return redirect('product_list')

# -------------------------
# User Management Views
# -------------------------
CustomUser = get_user_model()  # website.AuthUser

@login_required
def users_list(request):
    users = CustomUser.objects.all().order_by('id')
    return render(request, 'website/users/users_list.html', {'users': users})

@login_required
def add_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User added successfully!")
            return redirect('users_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'website/users/add_user.html', {'form': form})

# -------------------------
# Dashboard Overview
# -------------------------
@login_required
def dashboard(request):
    products = Product.objects.all()
    users = CustomUser.objects.all()  # Use AuthUser here
    return render(request, "website/dashboard.html", {
        "products": products,
        "users": users,
    })

# -------------------------
# Cart / Shopping Views
# -------------------------
from website.models import Product, Cart, CartItem

# Add to Cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.stock <= 0:
        messages.error(request, f"{product.name} is out of stock!")
        return redirect('product_list')

    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} added to cart!")
    return redirect('product_list')

#logout
@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    return render(request, 'website/cart.html', {'cart': cart, 'items': items})


# Remove from Cart
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart_view')

# Update Quantity
@login_required
def update_cart(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get("quantity", 1))
        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()
    return redirect('cart_view')
from website.models import Cart

def ensure_cart(user):
    if user.is_authenticated:
        Cart.objects.get_or_create(user=user)

        