from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Order
import json

# Product List View
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

# Product Detail View
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})

# Order Product View
@login_required
def order_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        total_price = product.price * quantity
        Order.objects.create(
            product=product,
            user=request.user,  # Use the logged-in user
            quantity=quantity,
            total_price=total_price
        )
        return redirect('order_success')  # Redirect to an order success page
    return render(request, 'order.html', {'product': product})

# Signup View
class SignupView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'signup.html', {'form': form})

# Profile View
@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('profile')
    else:
        form = UserChangeForm(instance=request.user)
    
    return render(request, 'profile.html', {'form': form})

# Custom Logout View
def custom_logout_view(request):
    logout(request)
    return render(request, 'logged_out.html')

# Order Success View
def order_success(request):
    return render(request, 'order_success.html')

# Mini App View
def mini_app_view(request):
    products = Product.objects.all()
    return render(request, 'mini_app.html', {'products': products})

# API Product List
def api_product_list(request):
    products = Product.objects.all()
    product_list = [{'id': p.id, 'name': p.name, 'price': str(p.price), 'image': p.image.url} for p in products]
    return JsonResponse({'products': product_list})

# API Order Create
@csrf_exempt
def api_order_create(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=401)

        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)

        # Ensure quantity is an integer
        try:
            quantity = int(quantity)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid quantity'}, status=400)

        try:
            product = Product.objects.get(id=product_id)
            total_price = product.price * Decimal(quantity)

            order = Order.objects.create(
                product=product,
                user=request.user,  # Ensure that user is authenticated
                quantity=quantity,
                total_price=total_price,
            )
            return JsonResponse({'status': 'success', 'order_id': order.id})
        except Product.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

# API Login
def api_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid credentials'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
