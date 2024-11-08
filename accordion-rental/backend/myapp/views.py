from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
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
from django.conf import settings
from rest_framework import status
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from datetime import datetime
import json
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
import jwt
from django.shortcuts import get_object_or_404
import logging
from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_auth_view(request):
    return Response({"message": "Authenticated successfully"})

##@csrf_exempt  # Remove this after testing
@api_view(['POST'])
def login_user(request):
    #data = request.data
    data = json.loads(request.body)
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
            
            redirect_url = "/profile" if missing_data else "/"

            # Create the response object
            response = JsonResponse({"redirect": redirect_url})

            # Set cookies for access and refresh tokens
            response.set_cookie(
                'access_token',
                access_token,
                httponly=False, # Set to False for local development
                secure=False,  # Set to False for local development, Ensure this is True in production
                samesite='Lax',  # Set from Lax to None for local development
                max_age=3600  # 1 hour
            )
           
            response.set_cookie(
                'refresh_token',
                refresh_token,
                httponly=False, # Set to False for local development, Ensure this is True in production
                secure=False,  # Set to False for local development
                samesite='Lax',  # Set from Lax to None for local development
                max_age=7 * 24 * 3600  # 7 days
                        )

            return response

        except Users.DoesNotExist:
            return JsonResponse({"error": "User profile not found"}, status=400)
    else:
        return JsonResponse({"error": "Incorrect username or password"}, status=400)
    
@api_view(['GET', 'POST'])
def profile_view(request):
    access_token = request.COOKIES.get('access_token')
    
    # Extract user information from token
    if access_token:
        user_id = get_user_id_from_token(access_token)
        username = get_user_from_token(access_token)
        
        if not user_id:
            return Response({"error": "Invalid or missing access token"}, status=401)
    else:
        return Response({"error": "Access token required"}, status=401)

    # Try to fetch or create a user profile based on user_id
    user_profile, created = Users.objects.get_or_create(user_id=user_id, defaults={'user_id': user_id})

    if request.method == 'GET':
        # Return profile data
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
        return Response(profile_data)

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
        return Response({"success": "Profile updated successfully"})

    return Response({"error": "Invalid request method"}, status=400)
    
@api_view(['POST'])
def logout_user(request):
    # Log the user out (clears Django session)
    logout(request)

    # Create response with a success message
    response = JsonResponse({"message": "Logged out successfully"}, status=200)
    
    # Delete JWT token cookies
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    
    # Delete CSRF cookie, if applicable
    response.delete_cookie('csrftoken')
    
    # Delete Django session cookie, if using sessions
    response.delete_cookie('sessionid')
    
    return response

@api_view(['GET'])
def check_login(request):
    if request.user.is_authenticated:
        return JsonResponse({"logged_in": True}, status=200)
    else:
        print("logged_in: False")
        return JsonResponse({"logged_in": False}, status=401)
    
@api_view(['POST'])
@csrf_exempt  # Make sure to include CSRF token handling in frontend#        
#@permission_classes([IsAuthenticated])  # Only allow authenticated users
def create_agreement(request):
    access_token = request.COOKIES.get('access_token')
    username = get_user_from_token(access_token)
    user = get_user_id_from_token(access_token)
    
  
    
    data = json.loads(request.body)
    authorization_header = request.headers.get('Authorization')
    


    # Extracting instrumentId and other necessary fields
    instrument_id = data.get('instrumentId')
    rental_period = data.get('months')
    additional_info = data.get('info')
    rate = data.get('rate')
    invoice_interval = data.get('invoiceInterval')
    
    
 

    # Check if instrument_id is provided
    if not instrument_id:
        return JsonResponse({"error": "Instrument ID is required"}, status=400)

    try:
        # Fetch the instrument instance from the Rendipillid model
        instrument = Rendipillid.objects.get(instrumentId=instrument_id)
        if rate:
            if 0 <= rental_period < 4:
                rate = round(rate * 2.1)  # 0-3 months
            elif 4 <= rental_period < 12:
                rate = round(rate * 1.4)  # 4-11 months
            else:
                rate = rate  # 12 months or greater

        user_instance = get_object_or_404(Users, user=user)  # Retrieve the actual Users instance

        
        # Create a new agreement
        agreement = Agreements.objects.create(
            userId=user_instance,
            instrumentId=instrument,  # Use the fetched instrument instance
            startDate=datetime.now(),
            months=rental_period,
            rate=rate,
            info=additional_info,
            status='Created',  # Ensure the status matches your choices
            invoice_interval=invoice_interval,
        )

        return JsonResponse({
            "message": "Agreement created successfully.",
            "agreement_id": agreement.agreementId,
            "instrument": {
                "instrument_id": instrument.instrumentId,
                "rate": rate
            },
            "rental_period": rental_period,
            "start_date": agreement.startDate,
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
    
def calculate_reference_number(agreementId):
    year = datetime.datetime.now().year
    base_number = f"{year}{agreementId}"

    if not base_number.isdigit():
        raise ValueError("Base number must be numeric")

    # Calculating control digit (modulo 10 approach)
    weights = [7, 3, 1]
    total = 0
    for i, digit in enumerate(reversed(base_number)):
        total += int(digit) * weights[i % len(weights)]

    control_digit = (10 - (total % 10)) % 10
    reference_number = f"{base_number}{control_digit}"

    return int(reference_number)


@api_view(['GET'])
def contracts_view(request):
    access_token = request.COOKIES.get('access_token')
    user_id = get_user_id_from_token(access_token)
   
    try:
        user_profile = Users.objects.get(user_id=user_id)
        profileId = user_profile.userId  # Assuming `id` is the primary key in Users
    except Users.DoesNotExist:
        return JsonResponse({"error": "User profile not found"}, status=404)
   
    
    agreements = Agreements.objects.filter(userId=profileId)
    data = []
    
    for agreement in agreements:
        # Get related rendipillid and model
        try:
            instrument = Rendipillid.objects.get(instrumentId=agreement.instrumentId_id)
            model = Model.objects.get(modelId=instrument.modelId_id)
            
            image_link = f"/media/700/R{agreement.instrumentId_id}.jpg"
            
            end_date = agreement.startDate + relativedelta(months=agreement.months)

            agreement_data = {
                "agreement": {
                    "agreementId": agreement.agreementId,
                    "referenceNr": agreement.referenceNr,
                    "instrumentID": agreement.instrumentId_id,
                    "startDate": agreement.startDate,
                    "endDate": end_date,
                    "months": agreement.months,
                    "rate": agreement.rate,
                    "info": agreement.info,
                    "status": agreement.status,
                    "invoice_interval": agreement.invoice_interval,
                    # add other agreement fields as needed
                },
                "instrument": {
                    "serial": instrument.serial,
                    "instrumentId": instrument.instrumentId,
                    "color" : instrument.color,
                    "status" : instrument.status,
                    # add other instrument fields
                },
                "model": {
                    "model": model.model,
                    "brand": model.brand,
                    "keys": model.keys,
                    "sb": model.sb,
                    # add other model fields
                },
                "imageLink": image_link
               
            }
            data.append(agreement_data)
        except Rendipillid.DoesNotExist:
            continue

    return JsonResponse(data, safe=False)

def get_user_from_token(access_token):
    try:
        # Decode the token
        token = AccessToken(access_token)

        # Get the user ID from the token payload
        user_id = token['user_id']  # This assumes 'user_id' is the identifier key in the payload

        # Retrieve the user instance
        user = User.objects.get(id=user_id)
        return user

    except Exception as e:  # General exception for any token/user retrieval issues
        # Handle token or user retrieval errors
        return JsonResponse({"error": "Invalid or expired token."}, status=401)

def get_user_id_from_token(token):
    try:
        # Decode the token using Simple JWT's UntypedToken to validate it
        UntypedToken(token)
        decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_payload.get('user_id')
        
        if user_id:
            return user_id
        else:
            return JsonResponse({"error": "User ID not found in token"}, status=400)
    
    except TokenError:
        return JsonResponse({"error": "Invalid token"}, status=401)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)