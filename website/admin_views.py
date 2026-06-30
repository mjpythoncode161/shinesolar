from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
from products_brands_app.models import ProductCategory, Product, Brand
from .models import ContactEnquiry, BlogPost


def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')
    return render(request, 'admin_panel/login.html')


def admin_logout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='/admin-panel/login/')
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')
    context = {
        'product_count': Product.objects.count(),
        'brand_count': Brand.objects.count(),
        'contact_count': ContactEnquiry.objects.count(),
        'category_count': ProductCategory.objects.count(),
        'blog_count': BlogPost.objects.count(),
        'recent_products': Product.objects.select_related('category').order_by('-id')[:8],
        'recent_contacts': ContactEnquiry.objects.order_by('-created_at')[:8],
    }
    return render(request, 'admin_panel/dashboard.html', context)


# --- PRODUCTS ---
@login_required(login_url='/admin-panel/login/')
def admin_products(request):
    if not request.user.is_staff:
        return redirect('home')
    products = Product.objects.select_related('category').all()
    return render(request, 'admin_panel/products.html', {'products': products})


@login_required(login_url='/admin-panel/login/')
def admin_product_add(request):
    if not request.user.is_staff:
        return redirect('home')
    categories = ProductCategory.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        cat_id = request.POST.get('category')
        description = request.POST.get('description', '')
        order = int(request.POST.get('order', 0))
        is_active = 'is_active' in request.POST
        image = request.FILES.get('image')
        if name and cat_id and image:
            category = get_object_or_404(ProductCategory, id=cat_id)
            slug = slugify(name)
            # ensure unique slug within category
            base_slug = slug
            counter = 1
            while Product.objects.filter(category=category, slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            Product.objects.create(
                name=name, category=category, slug=slug,
                description=description, order=order,
                is_active=is_active, image=image
            )
            messages.success(request, f'Product "{name}" added successfully!')
            return redirect('admin_products')
        else:
            messages.error(request, 'Please fill all required fields.')
    return render(request, 'admin_panel/product_form.html', {'categories': categories})


@login_required(login_url='/admin-panel/login/')
def admin_product_edit(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    product = get_object_or_404(Product, id=pk)
    categories = ProductCategory.objects.all()
    if request.method == 'POST':
        product.name = request.POST.get('name', product.name).strip()
        cat_id = request.POST.get('category')
        if cat_id:
            product.category = get_object_or_404(ProductCategory, id=cat_id)
        product.description = request.POST.get('description', '')
        product.order = int(request.POST.get('order', 0))
        product.is_active = 'is_active' in request.POST
        if request.FILES.get('image'):
            product.image = request.FILES['image']
        product.save()
        messages.success(request, f'Product "{product.name}" updated!')
        return redirect('admin_products')
    return render(request, 'admin_panel/product_form.html', {'product': product, 'categories': categories})


@login_required(login_url='/admin-panel/login/')
def admin_product_delete(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    product = get_object_or_404(Product, id=pk)
    product.delete()
    messages.success(request, 'Product deleted.')
    return redirect('admin_products')


# --- BRANDS ---
@login_required(login_url='/admin-panel/login/')
def admin_brands(request):
    if not request.user.is_staff:
        return redirect('home')
    brands = Brand.objects.all()
    return render(request, 'admin_panel/brands.html', {'brands': brands})


@login_required(login_url='/admin-panel/login/')
def admin_brand_add(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        website = request.POST.get('website', '')
        order = int(request.POST.get('order', 0))
        is_active = 'is_active' in request.POST
        logo = request.FILES.get('logo')
        if name and logo:
            slug = slugify(name)
            base_slug = slug
            counter = 1
            while Brand.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            Brand.objects.create(name=name, slug=slug, website=website, order=order, is_active=is_active, logo=logo)
            messages.success(request, f'Brand "{name}" added!')
            return redirect('admin_brands')
        else:
            messages.error(request, 'Please fill all required fields.')
    return render(request, 'admin_panel/brand_form.html', {})


@login_required(login_url='/admin-panel/login/')
def admin_brand_edit(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    brand = get_object_or_404(Brand, id=pk)
    if request.method == 'POST':
        brand.name = request.POST.get('name', brand.name).strip()
        brand.website = request.POST.get('website', '')
        brand.order = int(request.POST.get('order', 0))
        brand.is_active = 'is_active' in request.POST
        if request.FILES.get('logo'):
            brand.logo = request.FILES['logo']
        brand.save()
        messages.success(request, f'Brand "{brand.name}" updated!')
        return redirect('admin_brands')
    return render(request, 'admin_panel/brand_form.html', {'brand': brand})


@login_required(login_url='/admin-panel/login/')
def admin_brand_delete(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    brand = get_object_or_404(Brand, id=pk)
    brand.delete()
    messages.success(request, 'Brand deleted.')
    return redirect('admin_brands')


# --- CONTACTS ---
@login_required(login_url='/admin-panel/login/')
def admin_contacts(request):
    if not request.user.is_staff:
        return redirect('home')
    contacts = ContactEnquiry.objects.all()
    return render(request, 'admin_panel/contacts.html', {'contacts': contacts})


# --- BLOG ---
@login_required(login_url='/admin-panel/login/')
def admin_blog(request):
    if not request.user.is_staff:
        return redirect('home')
    posts = BlogPost.objects.all()
    return render(request, 'admin_panel/blog.html', {'posts': posts})


@login_required(login_url='/admin-panel/login/')
def admin_blog_add(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        excerpt = request.POST.get('excerpt', '')
        content = request.POST.get('content', '')
        is_published = 'is_published' in request.POST
        image = request.FILES.get('image')
        if title and content:
            slug = slugify(title)
            base_slug = slug
            counter = 1
            while BlogPost.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            post = BlogPost.objects.create(
                title=title, slug=slug, excerpt=excerpt,
                content=content, is_published=is_published
            )
            if image:
                post.image = image
                post.save()
            messages.success(request, f'Blog post "{title}" created!')
            return redirect('admin_blog')
        else:
            messages.error(request, 'Title and content are required.')
    return render(request, 'admin_panel/blog_form.html', {})


@login_required(login_url='/admin-panel/login/')
def admin_blog_edit(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    post = get_object_or_404(BlogPost, id=pk)
    if request.method == 'POST':
        post.title = request.POST.get('title', post.title).strip()
        post.excerpt = request.POST.get('excerpt', '')
        post.content = request.POST.get('content', '')
        post.is_published = 'is_published' in request.POST
        if request.FILES.get('image'):
            post.image = request.FILES['image']
        post.save()
        messages.success(request, f'Blog post "{post.title}" updated!')
        return redirect('admin_blog')
    return render(request, 'admin_panel/blog_form.html', {'post': post})


@login_required(login_url='/admin-panel/login/')
def admin_blog_delete(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    post = get_object_or_404(BlogPost, id=pk)
    post.delete()
    messages.success(request, 'Blog post deleted.')
    return redirect('admin_blog')

