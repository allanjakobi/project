import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
from django.conf import settings
from myapp.models import Agreements, Users
from django.db.models import Q

class Command(BaseCommand):
    help = 'Extend agreements automatically if they are overdue and set to EndingSoon.'

    def handle(self, *args, **kwargs):
        today = now().date()
        agreements = Agreements.objects.filter(
            Q(status='Test')
        )

        for agreement in agreements:
            agreement_end_date = agreement.startDate + relativedelta(months=agreement.months)
            extend_cutoff_date = agreement_end_date + relativedelta(days=7)
            print(agreement_end_date, extend_cutoff_date )
            if today > extend_cutoff_date:
                try:
                    user_profile = agreement.userId
                    language = user_profile.language

                    # Extend agreement
                    agreement.extended += 1
                    aug= int(agreement.months / (agreement.extended))  # Adjust logic as needed
                    agreement.months = agreement.months + aug
                    agreement.status = 'Active'
                    agreement.save()

                    # Notify the user
                    self.send_email(user_profile, agreement, language)

                    self.stdout.write(
                        self.style.SUCCESS(f"[{now()}] Agreement {agreement.agreementId} extended successfully.")
                    )
                except Exception as e:
                    self.stderr.write(f"Error processing agreement {agreement.agreementId}: {e}")

    def send_email(self, user_profile, agreement, language):
        smtp_server = settings.EMAIL_HOST
        smtp_port = settings.EMAIL_PORT
        context = ssl.create_default_context()

        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = user_profile.email

        name = f"{user_profile.firstName} {user_profile.lastName}"
        end_date = agreement.startDate + relativedelta(months=agreement.months)
        formatted_end_date = end_date.strftime("%d.%m.%Y")

        if language in ['Eesti', 'Estonian']:
            msg['Subject'] = 'Akordioni rendilepingut on automaatselt pikendatud'
            body = (
                f"Lp. {name},\n\n"
                f"Akordioni rendilepingut nr. {agreement.agreementId} on automaatselt pikendatud kuni {formatted_end_date}.\n"
                f"Jätkake makseid püsikorraldusega endise viitenumbri {agreement.referenceNr} alusel.\n"
                f"Vajadusel kontakteeruge täpsustamiseks.\n\n"
                f"Accordion Rent"
            )
        else:
            msg['Subject'] = 'Your accordion rental period is automatically extended'
            body = (
                f"Dear {name},\n\n"
                f"Your accordion rental period (Agreement {agreement.agreementId}) is automatically extended to {formatted_end_date}.\n"
                f"Please continue payments using your reference number {agreement.referenceNr}.\n\n"
                f"Accordion Rent"
            )

        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls(context=context)
                server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                server.sendmail(msg['From'], msg['To'], msg.as_string())
                self.stdout.write(self.style.SUCCESS(f"Email sent to {user_profile.email}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Failed to send email to {user_profile.email}: {e}"))


    def send_email(self, user_profile, agreement, language):
        today = now().date()
        smtp_server = settings.EMAIL_HOST
        smtp_port = settings.EMAIL_PORT

        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        

        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = user_profile.email
        
        name = f"{user_profile.firstName} {user_profile.lastName}"
        endDate = agreement.startDate + relativedelta(months=agreement.months)
        formatted_end_date = endDate.strftime("%d.%m.%Y")

        if language in ['Eesti', 'Estonian']:
            msg['Subject'] = 'Akordioni rendilepingut on automaatselt pikendatud'
            body = (
                f"Lp. {name}.\n\n\n"
                f"Akordioni rendilepingut nr. {agreement.agreementId} on automaatselt pikendatud kuni {formatted_end_date}.\n\n"
                f"Jätkake makseid püsikorraldusega endise viitenumbri {agreement.referenceNr} alusel\n"
                f"Vajadusel kontakteeruge täpsustamiseks.\n\n"
                f"Andke teada kui soovite pilli tuua hooldamiseks. \n\n"
                f"Head pilli kasutamist uuel perioodil,\n\n\n"
                f"Accordion Rent,\n"
            )
        else:
            msg['Subject'] = 'Your accordion rental period is automatically extended '
            
            body = (
                f"Dear {name}.\n\n\n"
                f"Your  accordion rental period is automatically extended to {endDate}.\n"
                f"(Agreement {agreement.agreementId})\n\n"
                f"Please continue payments using your reference number {agreement.referenceNr}\n"
                f"If needed, please don't hesitate to contact us for more information.\n\n"
                f"Feel free to reach out if you'd like to bring the instrument in for maintenance. \n\n"
                f"Wishing you an enjoyable experience with the instrument during the new rental period.,\n\n\n"
                f"Accordion Rent,\n"

            )

        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls(context=context)
                server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                server.sendmail(msg['From'], msg['To'], msg.as_string())
                self.stdout.write(self.style.SUCCESS(f"Email sent to {user_profile.email}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to send email to {user_profile.email}: {e}"))
