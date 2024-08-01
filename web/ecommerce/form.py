from django import forms
from .models import Products

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'description', 'price', 'stock']
        labels = {
            'name': 'Name',
            'description': 'Description',
            'price': 'Price',
            'stock': 'Stock',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'description': forms.Textarea(attrs={'class': 'form-control mb-3'}),
            'price': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
        }
