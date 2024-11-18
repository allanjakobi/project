from background_task import background
from django.utils import timezone
from django.template.loader import render_to_string
from weasyprint import HTML
from django.utils.timezone import now
from .models import Invoices, Rendipillid
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import ssl

@background(schedule=120)  # 120 seconds (2 min)
def reset_instrument_status(instrument_id):
    print("RESET STARTED")
    try:
        instrument = Rendipillid.objects.get(instrumentId=instrument_id)
        # Check if the instrument is still "Reserved"
        if instrument.status == "Reserved":
            instrument.status = "Available"
            instrument.save()
            print("RESET successful")
            print(f"Instrument {instrument_id} status reset to 'Available'")
    except Rendipillid.DoesNotExist:
        print(f"Instrument {instrument_id} does not exist.")
