from django.urls import path
from . import admin_views

urlpatterns = [
    path('login/', admin_views.admin_login, name='admin_login'),
    path('logout/', admin_views.admin_logout, name='admin_logout'),
    path('', admin_views.admin_dashboard, name='admin_dashboard'),
    # Products
    path('products/', admin_views.admin_products, name='admin_products'),
    path('products/add/', admin_views.admin_product_add, name='admin_product_add'),
    path('products/<int:pk>/edit/', admin_views.admin_product_edit, name='admin_product_edit'),
    path('products/<int:pk>/delete/', admin_views.admin_product_delete, name='admin_product_delete'),
    # Brands
    path('brands/', admin_views.admin_brands, name='admin_brands'),
    path('brands/add/', admin_views.admin_brand_add, name='admin_brand_add'),
    path('brands/<int:pk>/edit/', admin_views.admin_brand_edit, name='admin_brand_edit'),
    path('brands/<int:pk>/delete/', admin_views.admin_brand_delete, name='admin_brand_delete'),
    # Contacts
    path('contacts/', admin_views.admin_contacts, name='admin_contacts'),
    # Blog
    path('blog/', admin_views.admin_blog, name='admin_blog'),
    path('blog/add/', admin_views.admin_blog_add, name='admin_blog_add'),
    path('blog/<int:pk>/edit/', admin_views.admin_blog_edit, name='admin_blog_edit'),
    path('blog/<int:pk>/delete/', admin_views.admin_blog_delete, name='admin_blog_delete'),
]
