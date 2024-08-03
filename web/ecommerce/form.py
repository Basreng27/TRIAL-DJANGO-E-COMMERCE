from django import forms
from .models import Products, Categories
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Auth
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        labels = {
            'username': 'Username',
            'password': 'Password',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control mb-3'}),
        }
class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'username': 'Username',
            'password': 'Password',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control mb-3'}),
            'last_name': forms.TextInput(attrs={'class':'form-control mb-3'}),
            'email': forms.EmailInput(attrs={'class':'form-control mb-3'}),
            'username': forms.TextInput(attrs={'class':'form-control mb-3'}),
            'password': forms.PasswordInput(attrs={'class':'form-control mb-3'}),
        }

    # Cek Password Must Same With Password2
    def clean(self):
        cleaned_data = super().clean()
        
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user

# Master
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['name', 'description']
        labels = {
            'name': 'Name',
            'description': 'Description',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'description': forms.Textarea(attrs={'class': 'form-control mb-3'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['category_id', 'image', 'name', 'description', 'price', 'stock']
        labels = {
            'category_id': 'Category',
            'image': 'Upload Image',
            'name': 'Name',
            'description': 'Description',
            'price': 'Price',
            'stock': 'Stock',
        }
        widgets = {
            'category_id': forms.Select(attrs={'class': 'form-control mb-3 select2', 'id':'category', 'style': 'width:100% !important'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control mb-3'}),
            'name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'description': forms.Textarea(attrs={'class': 'form-control mb-3'}),
            'price': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        
        self.fields['category_id'].empty_label = '--Select--'