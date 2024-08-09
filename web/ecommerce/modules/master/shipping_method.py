import requests
from django.shortcuts import render
from django.urls import reverse
from ...helpers import response_failed, pagination_page, response_success
from ...form import ShippingMethodForm

url = 'http://127.0.0.1:8000/apirest/shipping_method'
    
def page_shipping_method(request):
    token = request.COOKIES.get('access_token_api_rest')
    
    if not token:
        return response_failed('Shipping Method', 'Undifined Token')
    
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    # Menggunakan requests.get untuk melakukan permintaan HTTP GET
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # Asumsikan pagination_page adalah fungsi yang memproses pagination
        pagination = pagination_page(request, response.json())

        data = {
            'title': "Master Shipping Method",
            'data': pagination
        }
        
        return render(request, 'shipping_method/display.html', data)
    else:
        return response_failed('Shipping Method', 'Failed Load Shipping Method')
    
def form_shipping_method(request, id=None):
    token = request.COOKIES.get('access_token_api_rest')
    
    if not token:
        return response_failed('Shipping Method', 'Undifined Token')
    
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    if id:
        respone = requests.get(f'{url}/{id}', headers=headers)
        
        if respone.status_code == 200:
            shipping_data = respone.json()
            form = ShippingMethodForm(request.POST or None, initial=shipping_data)
            url_action = reverse('shipping-method-restapi-update', kwargs={'id':id})
        else:
            return response_failed('Shipping Method', 'Failed Load Data From API')
    else:
        form = ShippingMethodForm(request.POST or None)
        url_action = reverse('shipping-method-restapi-form')
        
    if request.method == 'POST':
        form = ShippingMethodForm(request.POST)
        
        if form.is_valid():
            data_input = {
                'name': form.cleaned_data['name'],
                'description': form.cleaned_data['description'],
            }
            
            if id:
                response = requests.put(f'{url}/{id}', json=data_input, headers=headers)
            else:
                response = requests.post(url, json=data_input, headers=headers)
                
            if response.status_code in [200, 201]:
                return response_success('shipping_method', 'Save', 'Successfully saved data')
            else:
                try:
                    error_data = respone.json()
                except ValueError:
                    error_data = respone.text
                    
                return response_failed('Shipping Method', error_data)
        else:
            return response_failed('Shipping Method', form.errors.as_json())
            
    data = {
        'form': form,
        'url_action': url_action
    }
    
    return render(request, 'shipping_method/form.html', data)

def delete_shipping_method(request, id):
    token = request.COOKIES.get('access_token_api_rest')
    
    if not token:
        return response_failed('Brand', 'Token tidak ditemukan')

    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    response = requests.delete(f'{url}/{id}', headers=headers)
    
    if response.status_code == 200:
        return response_success('shipping_method', 'Delete', 'Successfully deleted data')
    else:
        try:
            error_data = response.json()
        except ValueError:
            error_data = response.text
            
        return response_failed('Shipping Method', error_data)