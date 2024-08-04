from django.shortcuts import render
from django.db.models import Count
from ...models import Products, Categories
from ...helpers import pagination_page

def initial_page(request):
    data = {
        'products': Products.objects.order_by('?')[:4], # Menampilkan Acak dan Limit 4
    }
    
    return render(request, 'guest/template/initial_page.html', data)

def page_shop(request):
    product = Products.objects.all()
    pagination = pagination_page(request, product)
    
    data = {
        'data': pagination,
        'categories': Categories.objects.annotate(product_count=Count('products')), # Menghitung Total Jumlah Product Pada Setiap Category
    }
    
    return render(request, 'guest/page/shop.html', data)

def page_shop_detail(request):
    return render(request, 'guest/page/shop_detail.html')

def page_cart(request):
    return render(request, 'guest/page/cart.html')

def page_checkout(request):
    return render(request, 'guest/page/checkout.html')