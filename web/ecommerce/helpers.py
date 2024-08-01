from django.http import JsonResponse
from django.core.paginator import Paginator

def save_success(url):
    return JsonResponse({
                'status': True,
                'title': "Save Data",
                'message': "Successfully Save Data",
                'icon': 'success',
                'redirect': url
            })

def save_failed():
    return JsonResponse({
                'status': False,
                'title': "Save Data",
                'message': "Failed Save Data",
                'icon': 'error'
            })
    
def delete_success(url):
    return JsonResponse({
                'status': True,
                'title': "Delete Data",
                'message': "Successfully Delete Data",
                'icon': 'success',
                'redirect': url
            })

def delete_failed():
    return JsonResponse({
                'status': False,
                'title': "Delete Data",
                'message': "Failed Delete Data",
                'icon': 'error'
            })
    
def pagination_page(request, list):
    pagination = Paginator(list, 10)
    page_number = request.GET.get('page')
    
    return pagination.get_page(page_number)