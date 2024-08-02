from django.shortcuts import render
from ...form import RegisterForm
from ...helpers import response_success, response_failed

# Function Page Register
def page_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        
        if form.is_valid():
            form.save()
        
            return response_success('', 'Register', 'Successfully Register')
        else:
            return response_failed('Register', form.errors.as_json())
    else:
        form = RegisterForm(request.POST or None)
    
    data = {
        'form': form
    }
    
    return render(request, 'auth/register.html', data)