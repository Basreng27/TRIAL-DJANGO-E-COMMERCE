from django.shortcuts import render

def product_view(request):
    data = {
        'title': "Master Product"
    }
    
    return render(request, 'product/display.html', data)