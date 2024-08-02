from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import Q
from ...models import Categories
from ...form import CategoryForm
from ...helpers import pagination_page, response_success, response_failed

def page_category(request):
    name = request.GET.get('name', '').strip()
    description = request.GET.get('description', '').strip()
    
    filters = Q()
    
    if name:
        filters |= Q(name__icontains=name)
    if description:
        filters |= Q(description__icontains=description)
        
    category = Categories.objects.filter(filters)
    pagination = pagination_page(request, category)

    data = {
        'title': "Master Category",
        'data': pagination,
    }
    
    return render(request, 'category/display.html', data)

def form_category(request, id=None):
    if id:
        category = get_object_or_404(Categories, id=id)
        form = CategoryForm(request.POST or None, instance=category)
        url = reverse('category-form-update', kwargs={'id':id})
    else:
        form = CategoryForm(request.POST or None)
        url = reverse('category-form')
        
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            
            return response_success('category', 'Save', 'Successfully Save Data')
        else:
            return response_failed(form.errors.as_json())
        
    data = {
        'form': form,
        'url_action': url
    }
    
    return render(request, 'category/form.html', data)

def delete_category(request, id):
    category = get_object_or_404(Categories, id=id)
    
    if request.method == 'DELETE':
        category.delete()
        
        return response_success('category', 'Save', 'Successfully Save Data')
    else:
        return response_failed()