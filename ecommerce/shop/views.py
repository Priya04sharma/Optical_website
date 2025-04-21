from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.utils import timezone
from django.shortcuts import render






# def get_absolute_url(self):
#     return reverse('shop:product_list_by_category', args=[self.slug])

# User signup view
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('shop:product_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


# Display product list (optionally filtered by category)
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'is_homepage': True,
    }
    return render(request, 'shop/product/list.html', context)


# Product detail page
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()

    context = {
        'product': product,
        'cart_product_form': cart_product_form,
        'is_homepage': False,
    }
    return render(request, 'shop/product/detail.html', context)


# Appointment form view
def appointment_view(request):
    return render(request, 'shop/appointment.html')

def base_view(request):
    return render(request, 'shop/base.html')

# Handle appointment form submission
@csrf_protect
def submit_appointment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        preferred_date = request.POST.get('preferredDate')
        preferred_time = request.POST.get('preferredTime')
        concerns = request.POST.get('anyConcerns')

        # TODO: Save to DB or email logic

        # Add a flash message
        messages.success(request, "Your appointment has been booked successfully!")

        return redirect('shop:appointment')  # Redirect to appointment page (or thank you page)
    else:
        return HttpResponse("Invalid request method.", status=405)
    



def your_view(request):
    today_date = timezone.now().date()
    return render(request, 'your_template.html', {'today_date': today_date})

def about_details(request):
    return render(request, 'shop/aboutdetails.html')

