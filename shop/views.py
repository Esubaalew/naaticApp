from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})


def order_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        # Handle the order form submission
        quantity = int(request.POST.get('quantity', 1))
        # Additional order processing logic
        # Save the order or do whatever is needed
        return redirect('product_detail', product_id=product.id)

    return render(request, 'order_form.html', {'product': product})
