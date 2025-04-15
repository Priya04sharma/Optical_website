from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
# shop/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404
from .models import Product
from cart.forms import CartAddProductForm
from django.db.models import Avg



def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Optional: log the user in after signup
            return redirect('shop:product_list')  # Redirect to home or desired page
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'products': products
    }
    return render(request, 'shop/product/list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()

    # Get related products in the same category, excluding the current one
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    # Calculate average rating and total reviews
    avg = product.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    review_count = product.reviews.count()

    context = {
        'product': product,
        'cart_product_form': cart_product_form,
        'related_products': related_products,
        'avg': avg,
        'review_count': review_count,
    }
    return render(request, 'shop/product/detail.html', context)

