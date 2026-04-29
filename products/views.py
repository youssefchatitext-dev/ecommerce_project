<<<<<<< HEAD
from decimal import Decimal

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, Category

def _get_cart(request):
    return request.session.setdefault('cart', {})

def _cart_quantity(cart):
    return sum(cart.values())

def _build_base_context(request):
    cart = request.session.get('cart', {})
    return {
        'cart_count': _cart_quantity(cart),
    }

def _build_cart_context(request):
    cart = request.session.get('cart', {})
    product_ids = [int(product_id) for product_id in cart.keys()]
    products = Product.objects.filter(id__in=product_ids).select_related('category')
    product_map = {product.id: product for product in products}
    items = []
    total = Decimal('0.00')

    for product_id, quantity in cart.items():
        product = product_map.get(int(product_id))
        if not product:
            continue
        subtotal = product.price * quantity
        total += subtotal
        items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return {
        **_build_base_context(request),
        'cart_items': items,
        'cart_total': total,
    }

def product_list(request):
    products = Product.objects.select_related('category').all()
    context = {
        **_build_base_context(request),
        'products': products,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, id):
    product = get_object_or_404(Product.objects.select_related('category'), id=id)
    context = {
        **_build_base_context(request),
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)

def category_list(request):
    categories = Category.objects.annotate(product_count=Count('products')).all()
    context = {
        **_build_base_context(request),
        'categories': categories,
    }
    return render(request, 'products/category_list.html', context)

def category_detail(request, id):
    category = get_object_or_404(Category, id=id)
    products = category.products.select_related('category').all()
    context = {
        **_build_base_context(request),
        'category': category,
        'products': products,
    }
    return render(request, 'products/category_detail.html', context)

def cart(request):
    return render(request, 'products/cart.html', _build_cart_context(request))

def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart = _get_cart(request)
    product_id = str(product.id)
    current_quantity = cart.get(product_id, 0)
    cart[product_id] = min(current_quantity + 1, product.stock or current_quantity + 1)
    request.session.modified = True
    messages.success(request, f"{product.name} a ete ajoute au panier.")
    return redirect(request.POST.get('next') or 'cart')

def remove_from_cart(request, id):
    cart = _get_cart(request)
    product_id = str(id)
    if product_id in cart:
        del cart[product_id]
        request.session.modified = True
        messages.success(request, "Le produit a ete retire du panier.")
    return redirect('cart')

def update_cart_quantity(request, id):
    cart = _get_cart(request)
    product_id = str(id)
    product = get_object_or_404(Product, id=id)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1

    if quantity <= 0:
        cart.pop(product_id, None)
    else:
        cart[product_id] = min(quantity, product.stock)

    request.session.modified = True
    return redirect('cart')
=======
from django.shortcuts import get_object_or_404, render
from .models import Product, Category

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'products/product_detail.html', {'product': product})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {'categories': categories})

def category_detail(request, id):
    category = get_object_or_404(Category, id=id)
    products = category.products.all()
    return render(request, 'products/category_detail.html', {'category': category, 'products': products})
>>>>>>> f81f612207979a3dec3531f73deb3ea7a70a8c73
