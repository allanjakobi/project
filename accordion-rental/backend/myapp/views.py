from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import generics
from rest_framework.views import APIView

from .models import Agreements, Rates, Rendipillid, Users, Model, Invoices, Payment
from .serializers import ModelSerializer, RendipillidSerializer, AgreementSerializer
from django.shortcuts import render
from .forms import RendipillidForm
from dateutil.relativedelta import relativedelta


from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from rest_framework import viewsets
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q, Sum, F
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from rest_framework import status
from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from datetime import datetime, timedelta
import json
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
import jwt
from django.shortcuts import get_object_or_404
import logging
import tempfile
from dateutil.relativedelta import relativedelta
from weasyprint import HTML
from django.template.loader import render_to_string
import smtplib
import ssl
import certifi
from django.core.mail import EmailMessage
from io import BytesIO

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from django.utils import timezone
from django.db.models import Case, When, F, Value, DateField
from django.db.models.functions import Now
from .tasks import reset_instrument_status
from rest_framework.permissions import IsAdminUser

from django.db import IntegrityError
from xml.etree import ElementTree as ET
from django.utils.timezone import make_aware




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

""" def rendipillid_list_view(request):
    # Fetch all rendipillid entries, including related model data
    rendipillid_list = Rendipillid.objects.select_related('modelId', 'price_level').all()
    return render(request, 'rendipillid_list.html', {'rendipillid_list': rendipillid_list})

#@method_decorator(csrf_exempt, name='dispatch')
class AvailableInstrumentsViewSet(viewsets.ViewSet):
    def list(self, request):
        available_instruments = Rendipillid.objects.filter(Q(status="Available") | Q(status="Reserved") | Q(status="AgreementInProgress") | Q(status="Rented") | Q(status="Other")).select_related('modelId', 'price_level')  # Use modelId
        serializer = RendipillidSerializer(available_instruments, many=True)
        return Response(serializer.data) """

class AvailableInstrumentsViewSet(viewsets.ViewSet):
    def list(self, request):
        today = timezone.now().date()
        
        # Fetch instruments and their related models
        available_instruments = Rendipillid.objects.filter(
            Q(status="Available") | Q(status="Reserved") | Q(status="AgreementInProgress") | Q(status="Rented") | Q(status="Other")
        ).select_related('modelId', 'price_level')
        
        # Prepare the serialized data with a calculated `date`
        instrument_data = []
        for instrument in available_instruments:
            if instrument.status in ["Available"]:
                date = today
            elif instrument.status in ["Reserved"]:
                date = today+relativedelta(days=1)
            elif instrument.status in ["AgreementInProgress", "Rented"]:
                # Retrieve the related agreement and calculate the end date
                agreement = Agreements.objects.filter(instrumentId=instrument.instrumentId).last()
                if agreement:
                    
                    # Calculate the end date based on `startDate` and `months` interval
                    end_date = agreement.startDate + relativedelta(months=agreement.months)
                    print("agreement: ", end_date)
                    date = max(end_date, today) if end_date > today else today
                else:
                    date = today  # Default to today if no agreement found
            else:
                # Default case for "Other": set to today + 1 year
                date = today.replace(year=today.year + 1)
            
            # Append calculated date to each instrument's data
            instrument_dict = RendipillidSerializer(instrument).data
            instrument_dict['predicted_availability'] = f"Predicted to be available: {date.strftime('%d.%m.%Y')}"
            instrument_data.append((date, instrument_dict))
        
        # Sort by the calculated date and return only the serialized data
        instrument_data.sort(key=lambda x: x[0])
        sorted_data = [item[1] for item in instrument_data]
        
        return Response(sorted_data)


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
            if user.is_staff:
                print("STAFF", user)
                redirect_url = "/admin"
            else:
                
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
    
    if access_token:
        user_id = get_user_id_from_token(access_token)
        username = get_user_from_token(access_token)
        
        if not user_id:
            return Response({"error": "Invalid or missing access token"}, status=401)
    else:
        return Response({"error": "Access token required"}, status=401)

    try:
        # Fetch the auth_user entry based on user_id
        auth_user = User.objects.get(id=user_id)
        auth_user_email = auth_user.email
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    
    # Try to fetch or create a user profile based on user_id
    user_profile, created = Users.objects.get_or_create(
        user_id=user_id,
        defaults={'user_id': user_id, 'email': auth_user_email}  # set email by default if profile is created
    )

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
            "email2": auth_user_email,
            "email": user_profile.email,
        }
        return Response(profile_data)

    elif request.method == 'POST':
        # Update fields with request data if provided
        user_profile.firstName = request.data.get('firstName', user_profile.firstName)
        user_profile.lastName = request.data.get('lastName', user_profile.lastName)
        user_profile.email = request.data.get('email', user_profile.email)
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
    user = get_user_id_from_token(access_token)
    data = json.loads(request.body)
    
    instrument_id = int(data.get('instrumentId'))
    rental_period = int(data.get('months'))
    additional_info = data.get('info')
    rate = int(data.get('rate'))
    invoice_interval = int(data.get('invoiceInterval'))
    
    startDate = datetime.now()
    print("startDate", startDate)
    date1 = startDate + timedelta(days=7)
    date2 = date1 + relativedelta(months=1)
    date3 = date2 + relativedelta(months=1)
    
    if not instrument_id:
        return JsonResponse({"error": "Instrument ID is required"}, status=400)
    
    try:
        instrument = Rendipillid.objects.get(instrumentId=instrument_id)
        if rate:
            rate = calculate_rate(rate, rental_period)  # Helper function for rate calculation
        
        user_instance = get_object_or_404(Users, user_id=user)
        agreement = Agreements.objects.create(
            userId=user_instance,
            instrumentId=instrument,
            startDate=startDate,
            months=rental_period,
            rate=rate,
            info=additional_info,
            status='Created',
            invoice_interval=invoice_interval,
        )
        
        language = user_instance.language
        template_name = 'agreement_template_est.html' if language in ['Eesti', 'Estonian'] else 'agreement_template_eng.html'
        context = {
            'agreement': agreement,
            'instrument': instrument,
            'startDate': agreement.startDate,
            'date1': date1,
            'date2': date2,
            'date3': date3,
            'rate': rate,
            'rental_period': rental_period,
        }
        
        html_content = render_to_string(template_name, context)
        pdf_file = HTML(string=html_content).write_pdf()
        
        smtp_server = settings.EMAIL_HOST  # Replace with your SMTP server
        smtp_port = settings.EMAIL_PORT
        # Typically 587 for STARTTLS

        # Create an SSL context without certificate verification (not recommended for production)
        context = ssl.create_default_context()
        context.check_hostname = False  # Disable hostname check
        context.verify_mode = ssl.CERT_NONE  # Disable certificate verification

        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = user_instance.email
        msg['Subject'] = 'Your Rental Agreement'

        body = 'Please find attached your rental agreement.\n Please send the agreement digitally signed to the e-mail info@akordion.ee \n'
        msg.attach(MIMEText(body, 'plain'))
        #attachment       
        part = MIMEApplication(pdf_file, _subtype='pdf')
        part.add_header('Content-Disposition', 'attachment', filename=f"agreement_{agreement.agreementId}.pdf")
        msg.attach(part)

        # Establish SMTP connection
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls(context=context)  # Use the context with no verification
                server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)  # Use your SMTP credentials
                server.sendmail(msg['From'], msg['To'], msg.as_string())
            print("Email sent successfully.")
        except Exception as e:
            print(f"Error sending email: {e}") 
        
        instrument.status="AgreementInProgress"
        instrument.save()
        
        return JsonResponse({
            "message": "Agreement created successfully and sent via email.",
            "agreement_id": agreement.agreementId,
            "instrument": {"instrument_id": instrument.instrumentId, "rate": rate},
            "rental_period": rental_period,
            "start_date": agreement.startDate,
        }, status=201)
          
    except Rendipillid.DoesNotExist:
        return JsonResponse({"error": "Instrument not found."}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500) 

def calculate_rate(base_rate, rental_period):
    if 0 <= rental_period < 4:
        return round(base_rate * 2.1)
    elif 4 <= rental_period < 12:
        return round(base_rate * 1.4)
    return base_rate
    
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
    year = datetime.now().year
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


def download_contract(request, contract_id):
    # Fetch the contract, related agreement, and user data
    agreement = get_object_or_404(Agreements, pk=contract_id)
    instrument = agreement.instrumentId
    model = instrument.modelId  # Assuming each instrument has a related model
    user_profile = agreement.userId  # Assuming agreement.userId is a foreign key to Users
    startDate = agreement.startDate
    date1 = startDate + timedelta(days=7)
    date2 = date1 + relativedelta(months=1)
    date3 = date2 + relativedelta(months=1)
    
    # Prepare the data to pass into the template
    
    
    contract_data = {
        'agreement': agreement,
        'instrument': instrument,
        'model': model,
        'user_profile': user_profile,
        'startDate': agreement.startDate,
        'endDate': agreement.endDate,
        'rate': agreement.rate,
        'rental_period': f"{agreement.startDate} to {agreement.endDate}",
        'instrument_details': {
            'serial': instrument.serial,
            'instrumentId': instrument.instrumentId,
            'status': instrument.status,
            'color': instrument.color,
        },
        'date1': date1,
        'date2': date2,
        'date3': date3,
    }
   
    #user_profile = agreement.userId
   # user_instance = get_object_or_404(Users, user_id=user_profile.userId)
   
    language = user_profile.language
    
    template_name = 'agreement_template_est.html' if language in ['Eesti', 'Estonian'] else 'agreement_template_eng.html'
    
    # Render the HTML template for the contract
    html_content = render_to_string(template_name, contract_data)
    
    
    # Generate the PDF from the HTML content
    pdf_file = HTML(string=html_content).write_pdf()

    # Create the response and set the content type as PDF
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Contract_{agreement.agreementId}.pdf"'
    return response


@api_view(['GET'])
def invoices_view(request):
    access_token = request.COOKIES.get('access_token')
    user_id = get_user_id_from_token(access_token)
    print("UID: ", user_id)
   
    try:
        user_profile = Users.objects.get(user_id=user_id)
        profileId = user_profile.userId  # Assuming `userId` is the primary key in Users
    except Users.DoesNotExist:
        return JsonResponse({"error": "User profile not found"}, status=404)
   
    agreements = Agreements.objects.filter(userId=profileId)
    data = []
    
    for agreement in agreements:
        try:
            # Prepare agreement data
            agreement_data = {
                "agreement": {
                    "agreementId": agreement.agreementId,
                    "referenceNr": agreement.referenceNr,
                    "instrumentID": agreement.instrumentId_id,
                    "startDate": agreement.startDate,
                    "months": agreement.months,
                    "rate": agreement.rate,
                    "status": agreement.status,
                    "invoice_interval": agreement.invoice_interval,
                    # add other agreement fields as needed
                },
                "user": {
                    "firstName": user_profile.firstName,
                    "lastName": user_profile.lastName,
                    "street": user_profile.street,
                    "house": user_profile.house,
                    "apartment": user_profile.apartment,
                    "country": user_profile.country,
                    "province": user_profile.province,
                    "municipality": user_profile.municipality,
                    "settlement": user_profile.settlement,
                    "municipality": user_profile.municipality,
                },
                "invoices": []
            }
            
            # Retrieve and add invoices related to the agreement
            invoices = Invoices.objects.filter(agreement=agreement.agreementId)
            for invoice in invoices:
                invoice_data = {
                    "id": invoice.id,
                    "date": invoice.date,
                    "price": invoice.price,
                    "quantity": invoice.quantity,
                    "status": invoice.status,
                }
                agreement_data["invoices"].append(invoice_data)
                
            data.append(agreement_data)

        except Rendipillid.DoesNotExist:
            continue

    return JsonResponse(data, safe=False)


@api_view(['GET'])
def download_invoice(request, invoice_id):
    # Fetch the invoice, related agreement, and user data
    invoice = get_object_or_404(Invoices, pk=invoice_id)
    agreement = invoice.agreement
    user_profile = agreement.userId  # Assuming agreement.userId is a foreign key to Users
    imageLink = "/media/300/R"+str(agreement.instrumentId_id)+".jpg"
    invoice_data = {
        "agreement": agreement,
        "invoice": {
            "id": invoice.id,
            "date": invoice.date,
            "price": invoice.price,
            "quantity": invoice.quantity,
            "status": invoice.status,
            "total": invoice.price * invoice.quantity
        },
        "user": {     
            "firstName": user_profile.firstName,
            "lastName": user_profile.lastName,
            "street": user_profile.street,
            "house": user_profile.house,
            "apartment": user_profile.apartment,
            "country": user_profile.country,
            "province": user_profile.province,
            "municipality": user_profile.municipality,
            "settlement": user_profile.settlement,
            "municipality": user_profile.municipality,
        },
        "instrument": {
            "brand": agreement.instrumentId.modelId.brand,
            "model": agreement.instrumentId.modelId.model,
            "imageLink": imageLink,
        },
         
        
         
        
         "logoLink": '/media/logo.jpg'
    }
    
    language = user_profile.language
    
    template_name = 'invoice_template_est.html' if language in ['Eesti', 'Estonian'] else 'invoice_template.html'

    # Render HTML template
    html_content = render_to_string(template_name, invoice_data)
    pdf_file = HTML(string=html_content).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice_{invoice.id}.pdf"'
    return response


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
    
@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def reserve_instrument(request, instrument_id):
    try:
        # Find the instrument by ID
        instrument = Rendipillid.objects.get(instrumentId=instrument_id)        
        # Update the status to "Reserved"
        if instrument.status == "Available":
            instrument.status = "Reserved"
            instrument.save()
            
            # Schedule the reset task to run in 3 minutes
            reset_instrument_status(instrument.instrumentId)
            
            return Response({"message": "Instrument reserved successfully."})
        else:
            return Response({"message": "Instrument is not available."}, status=400)
    
    except Rendipillid.DoesNotExist:
        return Response({"error": "Instrument not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class ReserveInstrumentView(APIView):
    # Uncomment the following line if you want to require authentication
    # permission_classes = [IsAuthenticated]

    def post(self, request, instrument_id):
        try:
            # Find the instrument by ID
            instrument = get_object_or_404(Rendipillid, instrumentId=instrument_id)
            
            # Update the status to "Reserved" if it’s currently "Available"
            if instrument.status == "Available":
                instrument.status = "Reserved"
                instrument.save()
                print("about to reset.. in 3 min")
                
                # Schedule the reset task to run in 3 minutes
                reset_instrument_status(instrument.instrumentId)

                return Response({"message": "Instrument reserved successfully."})
            else:
                return Response({"message": "Instrument is not available."}, status=status.HTTP_400_BAD_REQUEST)

        except Rendipillid.DoesNotExist:
            return Response({"error": "Instrument not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['POST'])
#@permission_classes([IsAdminUser])  # Ensure only staff can access
def upload_payments(request):
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file uploaded'}, status=400)
    
    file = request.FILES['file']
    
    try:
        # Parse the XML file
        tree = ET.parse(file)
        root = tree.getroot()
        
        # Define the namespace
        ns = {'ns': 'urn:iso:std:iso:20022:tech:xsd:camt.053.001.02'}
        
        # Find all Ntry elements
        for ntry in root.findall(".//ns:Ntry", ns):
            
            reference_number_element = ntry.find(".//ns:CdtrRefInf/ns:Ref", ns)
            if reference_number_element is None:
                continue  # Skip this entry if reference number element is missing

            reference_number = reference_number_element.text.strip()
            if not reference_number.startswith("20") or not reference_number.isdigit():
                continue  # Skip this entry if reference number is invalid
            
            if reference_number.isdigit():  # Check if it is a valid integer-like string
                reference_number_int = int(reference_number)
            else:
                reference_number_int = None  # Handle non-integer strings

            # Extract other fields only if reference number is valid
            amount_element = ntry.find("ns:Amt", ns)
            amount = float(amount_element.text) if amount_element is not None else 0.0

            currency = amount_element.get("Ccy") if amount_element is not None else ""

            transaction_id_element = ntry.find("ns:AcctSvcrRef", ns)
            transaction_id = transaction_id_element.text.strip() if transaction_id_element is not None else ""

            payment_date_element = ntry.find("ns:BookgDt/ns:Dt", ns)
            payment_date = (
                make_aware(datetime.strptime(payment_date_element.text, "%Y-%m-%d"))
                if payment_date_element is not None
                else None
            )

            payer_name_element = ntry.find(".//ns:Dbtr/ns:Nm", ns)
            payer_name = payer_name_element.text.strip() if payer_name_element is not None else ""

            payer_account_element = ntry.find(".//ns:DbtrAcct/ns:Id/ns:IBAN", ns)
            payer_account = payer_account_element.text.strip() if payer_account_element is not None else ""

            status_element = ntry.find("ns:Sts", ns)
            status = status_element.text.strip() if status_element is not None else ""

            # Check for existing payment
            if not Payment.objects.filter(transaction_id=transaction_id).exists():
                # Check if the reference number matches any agreement
                if Agreements.objects.filter(referenceNr=(reference_number_int)).exists():
                    # Create a new payment
                    Payment.objects.create(
                        transaction_id=transaction_id,
                        reference_number=reference_number,
                        amount=amount,
                        currency=currency,
                        payer_name=payer_name,
                        payer_account=payer_account,
                        payment_date=payment_date,
                        status=status
                    )

        return JsonResponse({'status': 'Success', 'message': 'Payments uploaded successfully'})
    
    except ET.ParseError:
        return JsonResponse({'error': 'Invalid XML file'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
#@permission_classes([IsAdminUser])  # Ensure only staff can access
def list_agreements(request):
    agreements = Agreements.objects.select_related('instrumentId__modelId', 'userId') \
        .order_by('-startDate')  # Sorting by date descending
    
    data = []
    for agreement in agreements:
        """ payments_due = -sum(
            invoice.quantity * invoice.price 
            for invoice in agreement.invoices_set.exclude(status='Paid')
        ) """
        
        total_payments = Payment.objects.filter(reference_number=agreement.referenceNr) \
            .aggregate(total=Sum('amount'))['total'] or 0

        # Sum of invoice amounts (quantity * price) where the invoice is not 'Paid'
        unpaid_invoices = agreement.invoices_set.exclude(status='Paid') \
            .aggregate(total=Sum(F('quantity') * F('price')))['total'] or 0

        # Calculate payments due
        payments_due = total_payments - unpaid_invoices
        data.append({
            'agreementId': agreement.agreementId,
            'startDate': agreement.startDate,
            'endDate': agreement.endDate,
            'status': agreement.status,
            'info': agreement.info,
            
            'instrument': {
                'brand': agreement.instrumentId.modelId.brand,
                'model': agreement.instrumentId.modelId.model,
                'color': agreement.instrumentId.color,
            },
            'user': {
                'firstName': agreement.userId.firstName,
                'lastName': agreement.userId.lastName,
                'phone': agreement.userId.phone,
                'email': agreement.userId.email,
                
            },
            'paymentsDue': payments_due,
        })

    return JsonResponse({'agreements': data})

@api_view(['POST'])
#@permission_classes([IsAdminUser])  # Ensure only staff can access
def send_email(request, agreement_id):
    
    try:
        # Fetch agreement and user details
        agreement = Agreements.objects.get(agreementId=agreement_id)
        
        user_instance = agreement.userId  # Assuming the agreement has a linked user
        print("sending started: ", user_instance)
        # Get the message content from the request body
        email_message = request.data.get('email_message', '')
        print("sending started: ", email_message)
        
        
        # Set up the SMTP server and email details
        smtp_server = settings.EMAIL_HOST
        smtp_port = settings.EMAIL_PORT
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = user_instance.email       
        msg['Subject'] = f'{agreement.instrumentId.modelId.brand} {agreement.instrumentId.modelId.model}'

        
        if user_instance.language in ['Eesti', 'Estonian']:    
            body = f'{email_message}\n\nParimate soovidega, \n Akordioni rent'
        else:    
            body = f'{email_message}\n\nBest regards,\n Accordion Rent.'
        msg.attach(MIMEText(body, 'plain'))
        
        # Establish SMTP connection
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
        
        return Response({'message': 'Email sent successfully'}, status=200)
    
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def admin_dashboard(request):
    if not request.user.is_staff:
        return Response({'detail': 'Not authorized'}, status=403)
    
@api_view(['PUT'])
def update_agreement_info(request, agreement_id):
    try:
        # Retrieve the agreement by ID
        agreement = Agreements.objects.get(agreementId=agreement_id)

        # Check if 'info' is present in the request data
        info = request.data.get('info')
        if info is None:
            return Response({"error": "Info field is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the info field in the agreement
        agreement.info = info
        agreement.save()  # Save the updated agreement object

        # Serialize the updated agreement object
        serializer = AgreementSerializer(agreement)

        # Return the updated agreement data in the response
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Agreements.DoesNotExist:
        return Response({"error": "Agreement not found."}, status=status.HTTP_404_NOT_FOUND)