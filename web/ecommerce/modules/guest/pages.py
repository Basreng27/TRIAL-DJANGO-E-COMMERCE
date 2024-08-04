from django.shortcuts import render

def initial_page(request):
    return render(request, 'guest/template/initial_page.html')

def page_shop(request):
    return render(request, 'guest/page/shop.html')

def page_shop_detail(request):
    return render(request, 'guest/page/shop_detail.html')

def page_cart(request):
    return render(request, 'guest/page/cart.html')

def page_checkout(request):
    return render(request, 'guest/page/checkout.html')