from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from weasyprint import HTML
from myapp.models import Invoices
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import ssl
from django.utils.timezone import now

class Command(BaseCommand):
    help = "Process all invoices with status 'Issued'"

    def handle(self, *args, **kwargs):
        print(f"[{now()}] Starting invoice processing...XX")
        invoices = Invoices.objects.filter(status="Issued")

        for invoice in invoices:
            try:
                agreement = invoice.agreement
                user_profile = agreement.userId  # Assuming agreement.userId is a foreign key to Users
                imageLink = f"/media/300/R{agreement.instrumentId_id}.jpg"

                # Prepare invoice data
                invoice_data = {
                    "agreement": agreement,
                    "invoice": {
                        "id": invoice.id,
                        "date": invoice.date,
                        "price": invoice.price,
                        "quantity": invoice.quantity,
                        "status": invoice.status,
                        "total": invoice.price * invoice.quantity,
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
                    },
                    "instrument": {
                        "brand": agreement.instrumentId.modelId.brand,
                        "model": agreement.instrumentId.modelId.model,
                        "imageLink": imageLink,
                    },
                    "logoLink": '/media/logo.jpg',
                }

                language = user_profile.language
                template_name = (
                    'invoice_template_est.html'
                    if language in ['Eesti', 'Estonian']
                    else 'invoice_template.html'
                )

                # Render the PDF
                html_content = render_to_string(template_name, invoice_data)
                pdf_file = HTML(string=html_content).write_pdf()

                # Send email
                smtp_server = 'smtp.zone.eu'
                smtp_port = 587

                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE

                msg = MIMEMultipart()
                msg['From'] = 'info@akordion.ee'
                msg['To'] = user_profile.email
                msg['Subject'] = 'Your Invoice'

                if language in ['Eesti', 'Estonian']:
                    body = (
                        "Arve on lisatud manuses pdf-na.\n"
                        "Küsimuste korral, kontakteeruge info@akordion.ee."
                    )
                else:
                    body = (
                        "Please find attached your invoice.\n"
                        "For any queries, contact info@akordion.ee."
                    )
                msg.attach(MIMEText(body, 'plain'))

                part = MIMEApplication(pdf_file, _subtype='pdf')
                part.add_header(
                    'Content-Disposition', 'attachment',
                    filename=f"Invoice_{invoice.id}.pdf"
                )
                msg.attach(part)

                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls(context=context)
                    server.login('info@akordion.ee', 'ogrmactpyqsgvqks')
                    server.sendmail(msg['From'], msg['To'], msg.as_string())

                # Update invoice status
                invoice.status = "Sent"
                invoice.save()

                print(f"[{now()}] Invoice {invoice.id} sent successfully.")

            except Exception as e:
                print(f"[{now()}] Error processing invoice {invoice.id}: {str(e)}")

        print(f"[{now()}] Invoice processing completed.")
