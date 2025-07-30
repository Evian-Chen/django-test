from django.shortcuts import render, HttpResponse
from .models import TodoItem

# Create your views here.

def home(request):
    return render(request, "home.html")  # Render the home.html template

def todos(request):
    items = TodoItem.objects.all()
    return render(request, "todos.html", {"todos": items})  # Render the todos.html template