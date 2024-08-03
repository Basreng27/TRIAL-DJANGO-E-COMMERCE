from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import Q
from ...models import Products
from ...form import ProductForm
from ...helpers import pagination_page, response_success, response_failed

def page_product(request):
    name = request.GET.get('name', '').strip()
    description = request.GET.get('description', '').strip()
    
    filters = Q()
    
    if name:
        filters |= Q(name__icontains=name)
    if description:
        filters |= Q(description__icontains=description)

    product = Products.objects.filter(filters)
    pagination = pagination_page(request, product)
    
    data = {
        'title': "Master Product",
        'data': pagination,
    }

    return render(request, 'product/display.html', data)

def form_product(request, id=None):
    if id:
        product = get_object_or_404(Products, id=id)
        form = ProductForm(request.POST or None, request.FILES or None, instance=product)
        url = reverse('product-form-update', kwargs={'id': id})
    else:
        form = ProductForm(request.POST or None, request.FILES or None)
        url = reverse('product-form')

    if request.method == 'POST':
        if form.is_valid():
            form.save()

            return response_success('product', 'Save', 'Successfully Save Data')
        else:
            return response_failed(form.errors.as_json())

    data = {
        'form': form,
        'url_action': url,
    }

    return render(request, 'product/form.html', data)

def delete_product(request, id):
    product = get_object_or_404(Products, id=id)
    
    if request.method == 'DELETE':
        product.delete()
        
        return response_success('product', 'Delete', 'Successfully Delete Data')
    else:
        return response_failed()
    