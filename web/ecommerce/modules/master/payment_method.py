import requests
from django.shortcuts import render
from django.urls import reverse
from ...helpers import response_failed, pagination_page, response_success
from ...form import PaymentMethodForm

url = 'http://127.0.0.1:8000/apininja/payment_method'
    
def page_payment_method(request):
    token = request.COOKIES.get('access_token_api_ninja')
    
    if not token:
        return response_failed('Payment Method', 'Undifined Token')
    
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    # Menggunakan requests.get untuk melakukan permintaan HTTP GET
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # Asumsikan pagination_page adalah fungsi yang memproses pagination
        pagination = pagination_page(request, response.json())

        data = {
            'title': "Master Payment Method",
            'data': pagination
        }
        
        return render(request, 'payment_method/display.html', data)
    else:
        return response_failed('Payment Method', 'Failed Load Payment Method')
    
def form_payment_method(request, id=None):
    token = request.COOKIES.get('access_token_api_ninja')
    
    if not token:
        return response_failed('Payment Method', 'Undifined Token')
    
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    if id:
        respone = requests.get(f'{url}/{id}', headers=headers)
        
        if respone.status_code == 200:
            payment_data = respone.json()
            form = PaymentMethodForm(request.POST or None, initial=payment_data)
            url_action = reverse('payment-method-ninjaapi-update', kwargs={'id':id})
        else:
            return response_failed('Payment Method', 'Failed Load Data From API')
    else:
        form = PaymentMethodForm(request.POST or None)
        url_action = reverse('payment-method-ninjaapi-form')
        
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        
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
                return response_success('payment_method', 'Save', 'Successfully saved data')
            else:
                try:
                    error_data = respone.json()
                except ValueError:
                    error_data = respone.text
                    
                return response_failed('Payment Method', error_data)
        else:
            return response_failed('Payment Method', form.errors.as_json())
            
    data = {
        'form': form,
        'url_action': url_action
    }
    
    return render(request, 'payment_method/form.html', data)

def delete_payment_method(request, id):
    token = request.COOKIES.get('access_token_api_ninja')
    
    if not token:
        return response_failed('Brand', 'Token tidak ditemukan')

    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    response = requests.delete(f'{url}/{id}', headers=headers)
    
    if response.status_code == 200:
        return response_success('payment_method', 'Delete', 'Successfully deleted data')
    else:
        try:
            error_data = response.json()
        except ValueError:
            error_data = response.text
            
        return response_failed('Payment Method', error_data)