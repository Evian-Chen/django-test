from django.shortcuts import render, HttpResponse

# Create your views here.

def home(request):
    return render(request, "home.html")  # Render the home.html template
