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
from datetime import date

class Command(BaseCommand):
    help = 'Check agreements ending in one month or less and update their status to "EndingSoon".'

    def handle(self, *args, **kwargs):
        
        today = now().date()
        #one_month_from_now = today + relativedelta(months=agreement.months-1)

        agreements = Agreements.objects.filter(
            Q(status__in=['Created'])
        )
        
        nextMonthDate=today+relativedelta(months=1)

        for agreement in agreements:
            agreementEnd = agreement.startDate + relativedelta(months=agreement.months)            
            
            if nextMonthDate > agreementEnd:

                print("run endsoon")
                user_profile = agreement.userId
                language = user_profile.language

                # Update agreement status to "EndingSoon"
                agreement.status = "EndingSoon"
                agreement.save()

                # Send notification email to the user
                self.send_email(user_profile, agreement, language)

                self.stdout.write(
                    self.style.SUCCESS(f"[{now()}] Agreement {agreement.agreementId} is ending soon.")
                )

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
        formatted_end_date_eng = endDate.strftime("%d-%M-%Y")

        if language in ['Eesti', 'Estonian']:
            msg['Subject'] = 'Akordioni rendileping on peatselt lõppemas'
            body = (
                f"Lp. {name}.\n\n\n"
                f"Akordioni rendileping nr. {agreement.agreementId} on lõppemas {formatted_end_date}.\n\n"
                f"Lepingu pikendamiseks ja info täpsustamiseks kontakteeruge.\n"
                f"Kui akordioni tagastamine ei ole lõpule viidud {formatted_end_date}, pikendatakse lepingut automaatselt {agreement.months} kuu võrra.\n\n"
                f"Soovides pikendada rendilepingut muu pikkusega perioodi võrra, küsige juhiseid uue lepingu sõlmimiseks (Muu pikkusega perioodi puhul võib kuu renditasu sõltuvalt perioodi pikkusest erineda varasemast tasust. Uue lepingu puhul on vajalik sõlmida uus püsikorraldus uue ref. numbri alusel). \n\n"
                f"Lepingu lõpetamiseks peab rendiakordion olema tagasatatud - üle antud enne {formatted_end_date}.\n"
                f"Sobiliku aja ning parima toimetusviisi kokku leppimiseks kontakteeruge ...\n\n"
                f"Veenduge, et tagastamisel on pill komplektne, selle korpus ja pillikast puhastatud ning kõik lepingujärgsed kohustused on täidetud.\n"
                f"Vajades lisainformatsiooni, küsige julgesti ...\n\n"
                f"Täname tähtaegse tegutsemise eest,\n"
                f"Accordion Rent,\n"
            )
        else:
            msg['Subject'] = 'Rental period is ending soon'
            s = ""
            if agreement.months > 1:
                s="s"
            body = (
                f"Dear {name}.\n\n\n"
                f"Your  accordion rental period is about to end on {endDate}.\n"
                f"(Agreement {agreement.agreementId})\n\n"
                f"Contact ... to extend the agreement.\n"
                f"If the instrument is not returned by the deadline {endDate}, the agreement will be automatically extended by {agreement.months} month{s}.\n"
                f"In the case of need to extend rental by different period, ask for instructions setting up a new arragement. (In the case of different period the payent rate can differ. You will provided with a new reference number). \n\n"
                f"Otherwise, please return the instrument to ... before {endDate}.\n"
                f"Contact ... to arrange the time and best delivery method.\n\n"
                f"Ensure all contractual obligations are fulfilled upon termination.\n"
                f"If you need more information, don't hesitate to contact us.\n\n"
                f"With best regards,\n"
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
