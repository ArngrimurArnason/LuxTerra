from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about_us.html')

def contact(request):
    return render(request, 'contact_us.html')

