from django.http import JsonResponse
from django.core.paginator import Paginator
import json

# Response Json Success
def response_success(url, title, message):
    return JsonResponse({
                'status': True,
                'title': title,
                'message': message,
                'icon': 'success',
                'redirect': url
            })

# Response Json Failed
def response_failed(title, errors=None):
    return JsonResponse({
                'status': False,
                'title': title,
                'message': format_errors(json.loads(errors)),
                'icon': 'error'
            })

# Formating Error
def format_errors(errors):
    formatted_errors = []
    
    for field, error_list in errors.items():
        for error in error_list:
            message = error.get('message', '')
            formatted_errors.append(f"{field} ({message})")
    
    return "Failed Register: " + ", ".join(formatted_errors)

def pagination_page(request, list):
    pagination = Paginator(list, 10)
    page_number = request.GET.get('page')
    
    return pagination.get_page(page_number)