import requests
from django.shortcuts import render
from django.urls import reverse
from ...helpers import response_failed, response_success, pagination_page
from ...form import OrderForm

url = 'http://127.0.0.1:8000/apininja/order'

def page_order(request):
    token = request.COOKIES.get('access_token_api_ninja')
    
    if not token:
        return response_failed('Order', 'Undifined Token')
    
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        pagination = pagination_page(request, response.json())
        
        data = {
            'title': "Order",
            'data': pagination
        }
        
        return render(request, 'order/display.html', data)
    else:
        return response_failed('Order', 'Failed Load Order')
    
def form_order(request, id=None):
    token = request.COOKIES.get('access_token_api_ninja')
    
    if not token:
        return response_failed('Order', 'Undifined Token')
    
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    if id:
        response = requests.get(f'{url}/{id}', headers=headers)
        
        if response.status_code == 200:
            order_data = response.json()
            # If part not all field
            initial_data = {
                'status': order_data.get('status'),
            }
            form = OrderForm(request.POST or None, initial=initial_data)
            url_action = reverse('order-ninjaapi-update', kwargs={'id':id})
        else:
            return response_failed('Order', 'Failed Load Data API')
    else:
        form = OrderForm(request.POST or None)
        url_action = reverse('order-ninjaapi-form')
        
    if request.method == 'POST':
        form = OrderForm(request.POST)
        
        if form.is_valid():
            data_input = {
                'status': form.cleaned_data['status'],
            }
            
            if id:
                response = requests.put(f'{url}/{id}', json=data_input, headers=headers)
            else:
                response = requests.post(url, json=data_input, headers=headers)
                
            if response.status_code in [200, 201]:
                return response_success('order', 'Save', 'Successfully saved data')
            else:
                try:
                    error_data = response.json()
                except ValueError:
                    error_data = response.text
                    
                return response_failed('Order', error_data)
        else:
            return response_failed('Order', form.errors.as_json())
        
    data = {
        'form': form,
        'url_action': url_action
    }
    
    return render(request, 'order/form.html', data)