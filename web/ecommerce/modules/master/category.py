from django.shortcuts import render

def category_view(request):
    data = {
        'title': "Master Category"
    }
    
    return render(request, 'category/display.html', data)