import json
import requests
from django.shortcuts import render
from django.urls import reverse
from ...helpers import response_failed, pagination_page, response_success
from ...form import BrandForm

def page_brand(request):
    token = request.COOKIES.get('access_token_api_rest')
    
    if not token:
        return response_failed('Brand', 'Token tidak ditemukan')
    
    url = 'http://localhost:8000/apirest/brand'  # Sesuaikan dengan URL brand di apirest Anda
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        pagination = pagination_page(request, response.json())
        
        data = {
            'title': "Master Brand",
            'data': pagination
        }
        
        return render(request, 'brand/display.html', data)
    else:
        return response_failed('Brand', 'Gagal memuat data brand')

def form_brand(request, id=None):
    token = request.COOKIES.get('access_token_api_rest')
    
    if not token:
        return response_failed('Brand', 'Token tidak ditemukan')

    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    if id:
        # Ambil data dari API jika id diberikan
        url = f'http://localhost:8000/apirest/brand/{id}'  # Sesuaikan dengan URL API Anda
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            brand_data = response.json()
            form = BrandForm(request.POST or None, initial=brand_data)
            url_action = reverse('brand-restapi-update', kwargs={'id': id})
        else:
            return response_failed('Brand', 'Gagal memuat data dari API')
    else:
        form = BrandForm(request.POST or None)
        url_action = reverse('brand-restapi-form')

    if request.method == 'POST':
        form = BrandForm(request.POST)
        
        if form.is_valid():
            data_input = {
                'name': form.cleaned_data['name'],
                'description': form.cleaned_data['description'],
            }
            
            if id:
                response = requests.put(f'http://localhost:8000/apirest/brand_update/{id}', json=data_input, headers=headers)
            else:
                response = requests.post('http://localhost:8000/apirest/brand_create', json=data_input, headers=headers)
            
            if response.status_code in [200, 201]:
                return response_success('brand', 'Save', 'Successfully saved data')
            else:
                try:
                    error_data = response.json()
                except ValueError:
                    error_data = response.text

                return response_failed('Form', error_data)
        else:
            return response_failed('Form', form.errors.as_json())

    data = {
        'form': form,
        'url_action': url_action
    }
    
    return render(request, 'brand/form.html', data)

def delete_brand(request, id):
    token = request.COOKIES.get('access_token_api_rest')
    
    if not token:
        return response_failed('Brand', 'Token tidak ditemukan')

    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    # URL API untuk menghapus brand
    url = f'http://localhost:8000/apirest/brand_delete/{id}'  # Sesuaikan dengan URL API Anda

    # Kirim permintaan DELETE ke API
    response = requests.delete(url, headers=headers)
    
    if response.status_code == 204:  # No Content, penghapusan berhasil
        return response_success('brand', 'Delete', 'Successfully deleted data')
    else:
        try:
            error_data = response.json()
        except ValueError:
            error_data = response.text

        return response_failed('Brand', error_data)