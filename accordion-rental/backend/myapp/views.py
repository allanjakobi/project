from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import generics
from .models import Agreements, Rates, Rendipillid, Users
from .serializers import ModelSerializer, RendipillidSerializer
from django.shortcuts import render
from .forms import RendipillidForm
from .models import Rendipillid, Model
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Invoices
from rest_framework import viewsets
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from datetime import datetime
import json



class InvoiceList(ListView):
    model = Invoices
    template_name = 'invoices/invoice_list.html'  # Adjust to your template path
    context_object_name = 'invoices'

class InvoiceDetail(DetailView):
    model = Invoices
    template_name = 'invoices/invoice_detail.html'  # Adjust to your template path

class InvoiceCreate(CreateView):
    model = Invoices
    fields = ['date', 'agreementId', 'quantity', 'price']  # Adjust fields to your model
    template_name = 'invoices/invoice_form.html'  # Adjust to your template path
    success_url = reverse_lazy('invoice-list')

class InvoiceUpdate(UpdateView):
    model = Invoices
    fields = ['date', 'agreementId', 'quantity', 'price']  # Adjust fields to your model
    template_name = 'invoices/invoice_form.html'  # Adjust to your template path
    success_url = reverse_lazy('invoice-list')

class ModelList(generics.ListCreateAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer

class RendipillidList(generics.ListCreateAPIView):
    queryset = Rendipillid.objects.all()
    serializer_class = RendipillidSerializer

class RendipillidListCreate(generics.ListCreateAPIView):
    queryset = Rendipillid.objects.all()
    serializer_class = RendipillidSerializer


def rendipillid_create(request):
    if request.method == "POST":
        form = RendipillidForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = RendipillidForm()

    return render(request, 'rendipillid_form.html', {'form': form})

""" class RendipillidList(generics.ListAPIView):
    queryset = Rendipillid.objects.all()
    serializer_class = RendipillidSerializer """

def rendipillid_list_view(request):
    # Fetch all rendipillid entries, including related model data
    rendipillid_list = Rendipillid.objects.select_related('modelId', 'price_level').all()
    return render(request, 'rendipillid_list.html', {'rendipillid_list': rendipillid_list})

#@method_decorator(csrf_exempt, name='dispatch')
class AvailableInstrumentsViewSet(viewsets.ViewSet):
    def list(self, request):
        available_instruments = Rendipillid.objects.filter(Q(status="Available") | Q(status="Reserved")).select_related('modelId', 'price_level')  # Use modelId
        serializer = RendipillidSerializer(available_instruments, many=True)
        return Response(serializer.data)


def is_admin(user):
    return user.groups.filter(name='Admin').exists()

@ensure_csrf_cookie
def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})

# Protect a view so that only Admin users can access it
@user_passes_test(is_admin)
def admin_view(request):
    # Only accessible by users in the 'Admin' group
    return render(request, 'admin_page.html')

@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    if User.objects.filter(username=username).exists():
        return Response({"username": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()
    return Response({"success": "User registered successfully"}, status=status.HTTP_201_CREATED)

def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})

##@csrf_exempt  # Remove this after testing
@api_view(['POST'])
def login_user(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')
    user = authenticate(request, username=username, password=password)

    if user is not None:
        try:
            user_profile = Users.objects.get(user=user)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Determine if redirection is needed
            missing_data = (
                not user_profile.firstName or
                not user_profile.lastName or
                not user_profile.country or
                not user_profile.province or
                not user_profile.municipality or
                not user_profile.settlement or
                not user_profile.street or
                not user_profile.house or
                not user_profile.phone or
                not user_profile.language
            )
            
            print("access", access_token)
            print("refresh", refresh_token)
            redirect_url = "/profile" if missing_data else "/"

            # Create the response object
            response = JsonResponse({"redirect": redirect_url})

            # Set cookies for access and refresh tokens
            response.set_cookie(
                'access_token',
                access_token,
                httponly=True,
                secure=True,  # Set to False for local development
                samesite='None',  # Set from Lax to None for local development
                max_age=3600  # 1 hour
            )
            response.set_cookie(
                'refresh_token',
                refresh_token,
                httponly=True,
                secure=True,  # Set to False for local development
                samesite='None',  # Set from Lax to None for local development
                max_age=7 * 24 * 3600  # 7 days
                        )

            return response

        except Users.DoesNotExist:
            return JsonResponse({"error": "User profile not found"}, status=400)
    else:
        return JsonResponse({"error": "Incorrect username or password"}, status=400)
    
@api_view(['GET', 'POST'])
def profile_view(request):
    user = request.user
    user_profile = Users.objects.get(user=user)
    
    if request.method == 'GET':
        profile_data = {
            "firstName": user_profile.firstName,
            "lastName": user_profile.lastName,
            "country": user_profile.country,
            "province": user_profile.province,
            "municipality": user_profile.municipality,
            "settlement": user_profile.settlement,
            "street": user_profile.street,
            "house": user_profile.house,
            "apartment": user_profile.apartment,
            "phone": user_profile.phone,
            "language": user_profile.language,
        }
        return JsonResponse(profile_data)

    elif request.method == 'POST':
        # Update profile data
        user_profile.firstName = request.data.get('firstName', user_profile.firstName)
        user_profile.lastName = request.data.get('lastName', user_profile.lastName)
        user_profile.country = request.data.get('country', user_profile.country)
        user_profile.province = request.data.get('province', user_profile.province)
        user_profile.municipality = request.data.get('municipality', user_profile.municipality)
        user_profile.settlement = request.data.get('settlement', user_profile.settlement)
        user_profile.street = request.data.get('street', user_profile.street)
        user_profile.house = request.data.get('house', user_profile.house)
        user_profile.apartment = request.data.get('apartment', user_profile.apartment)
        user_profile.phone = request.data.get('phone', user_profile.phone)
        user_profile.language = request.data.get('language', user_profile.language)
        

        user_profile.save()
        return JsonResponse({"success": "Profile updated successfully"})
    
@api_view(['POST'])
def logout_user(request):
    # Log the user out
    logout(request)
    
    # Send a response confirming the logout
    return JsonResponse({"message": "Logged out successfully"}, status=200)

@api_view(['GET'])
def check_login(request):
    if request.user.is_authenticated:
        return JsonResponse({"logged_in": True}, status=200)
    else:
        return JsonResponse({"logged_in": False}, status=401)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Only allow authenticated users
@csrf_exempt  # Make sure to include CSRF token handling in frontend
def create_agreement(request):
    try:
        data = json.loads(request.body)
        user = request.user
        instrument_id = data.get('instrumentId')
        rental_period = data.get('months')
        additional_info = data.get('info')
        price_level_id = data.get('rate')

        # Retrieve the rate based on price level
        rate = Rates.objects.get(id=price_level_id).rate
        instrument = Rendipillid.objects.get(id=instrument_id)

        # Create a new agreement
        agreement = Agreements.objects.create(
            user=user,
            instrument=instrument,
            start_date=datetime.now(),
            months=rental_period,
            rate=rate,
            additional_info=additional_info,
            status='created'
        )

        return JsonResponse({
            "message": "Agreement created successfully.",
            "agreement_id": agreement.id,
            "instrument": {
                "brand": instrument.modelId.brand,
                "model": instrument.modelId.model,
                "price_level": price_level_id,
                "rate": rate
            },
            "rental_period": rental_period,
            "start_date": agreement.start_date,
        }, status=201)

    except Rates.DoesNotExist:
        return JsonResponse({"error": "Rate not found for specified price level."}, status=400)
    except Rendipillid.DoesNotExist:
        return JsonResponse({"error": "Instrument not found."}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@api_view(['GET'])
def get_rate(request, price_level_id):
    try:
        # Fetch the rate object based on the price level ID
        rate = Rates.objects.get(id=price_level_id)
        
        return JsonResponse({
            "id": rate.id,
            "rate": rate.rate,  # Assuming 'rate' is a field in your Rate model
            #"price_level": rate.price_level,  # Include any other relevant fields
        }, status=200)

    except Rates.DoesNotExist:
        return JsonResponse({"error": "Rate not found."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)