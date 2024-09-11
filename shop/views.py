from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order
from django.views import View
from django.contrib.auth.forms import UserCreationForm
#import logingrequired
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import update_session_auth_hash

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})


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

def custom_logout_view(request):
    logout(request)
    return render(request, 'logged_out.html')


def order_success(request):
    return render(request, 'order_success.html')
