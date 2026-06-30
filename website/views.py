from django.shortcuts import render, redirect
from django.contrib import messages

from products_brands_app.models import ProductCategory, Product, Brand
from .models import ContactEnquiry, BlogPost


def home(request):
    brands = Brand.objects.filter(is_active=True)
    featured_products = Product.objects.filter(is_active=True).select_related('category')[:4]
    context = {
        'brands': brands,
        'featured_products': featured_products,
    }
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')


def services(request):
    return render(request, 'services.html')


def products(request):
    """General products page on the main site, backed by products_brands_app models."""
    categories = ProductCategory.objects.all()
    brands = Brand.objects.filter(is_active=True)
    selected_category_slug = request.GET.get('category')

    if selected_category_slug:
        selected_category = categories.filter(slug=selected_category_slug).first()
        products_qs = Product.objects.filter(category=selected_category, is_active=True) if selected_category else Product.objects.none()
    else:
        selected_category = None
        products_qs = Product.objects.filter(is_active=True).select_related('category')

    context = {
        'categories': categories,
        'products': products_qs,
        'brands': brands,
        'selected_category': selected_category,
    }
    return render(request, 'products.html', context)


def projects(request):
    return render(request, 'projects.html')


def calculator(request):
    return render(request, 'calculator.html')


def blog(request):
    posts = BlogPost.objects.filter(is_published=True)
    return render(request, 'blog.html', {'posts': posts})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        service = request.POST.get('service', '').strip()
        message = request.POST.get('message', '').strip()

        if name and phone and message:
            ContactEnquiry.objects.create(
                name=name, phone=phone, email=email,
                service=service, message=message,
            )
            messages.success(request, 'Thank you! Your enquiry has been submitted. We will get back to you soon.')
            return redirect('contact')
        else:
            messages.error(request, 'Please fill all required fields.')

    return render(request, 'contact.html')
