from django.shortcuts import render,redirect
from django.urls import reverse
# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import requests
from .forms import SignupForm, LoginForm
from .models import Product
from django.http import JsonResponse
from .serializers import  ProductSerializer
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView

@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        return Response({'error': 'Please provide all required fields'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)

    
    return Response({'success': 'User created successfully'}, status=status.HTTP_201_CREATED)
    

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if not user:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

    login(request, user)
    return redirect ('dashboard')
 
    

    return Response({'success': 'Login successful'}, status=status.HTTP_200_OK)
def dashboard(request):
     response = requests.get(' http://127.0.0.1:8000/api/shopping')
     products = response.json()
     
     return render(request, 'myapp/dashboard.html', {'products': products})
      
 
@api_view(['GET'])
def shopping_items(request):
    items = [
        {
            'name': 'Milk',
            'price': 1,
            'quantity': 2
        },
        {
            'name': 'Eggs',
            'price': 2,
            'quantity': 12
        },
        {
            'name': 'Bread',
            'price': 3,
            'quantity': 4
        }
    ]
    return Response(items)

def signup_view(request):
       if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
           
            data = {
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password']
            }
            response = requests.post('http://127.0.0.1:8000/api/signup/', data=data)
            if response.status_code == 201: # or any other successful status code
                return redirect('login_view_view')
            else:
                error_message = response.json().get('error', 'Signup failed. Please try again later.')
                form.add_error(None, error_message)
           
               
       else:
        form = SignupForm()

       return render(request, 'myapp/signup.html', {'form': form})
def login_view_view(request):
       if request.method == 'POST':

        form = LoginForm(request.POST)

        if form.is_valid():


           
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            response = requests.post('http://127.0.0.1:8000/api/login/',data={'username': username, 'password': password})
            if response.status_code == 201: # or any other successful status code

                return redirect('dashboard')
            else:
                form.add_error(None, 'Invalid username or password.')
               
       else:
        form = LoginForm()

       return render(request, 'myapp/login.html', {'form': form})
class ProductFilterAPIView(APIView):

    def get(self, request, format=None):
       
       
       products = Product.objects.all()
       price = request.GET.get('price')
       name = request.GET.get('name')

       if price:
            products = products.filter(price__lte=price)
       if name:
            products = products.filter(name=name)

       serializer = ProductSerializer(products, many=True)
       return Response(serializer.data)
