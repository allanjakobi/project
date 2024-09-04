from django.core.management.base import BaseCommand
from myapp.models import Agreements, Invoices, Rates
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Q

class Command(BaseCommand):
    help = 'Automatically create invoices for all active agreements up to a specified date.'

    def add_arguments(self, parser):
        parser.add_argument('up_to_date', type=str, help='Date in format dd.mm.yyyy to generate invoices up to.')

    def handle(self, *args, **options):
        up_to_date_str = options['up_to_date']
        self.stdout.write(f"Creating invoices up to {up_to_date_str}...")
        
        # Implement the auto-create invoices logic
        up_to_date = datetime.strptime(up_to_date_str, '%d.%m.%Y').date()

        agreements = Agreements.objects.filter(~Q(status="Closed"))

        for agreement in agreements:
            current_invoice_date = agreement.startDate

            while current_invoice_date <= up_to_date:
                if not Invoices.objects.filter(
                    agreementId=agreement,
                    date__year=current_invoice_date.year,
                    date__month=current_invoice_date.month
                ).exists():
                    quantity = agreement.invoice_interval
                    price = agreement.rate * quantity

                    Invoices.objects.create(
                        date=current_invoice_date,
                        agreementId=agreement,
                        quantity=quantity,
                        price=price,
                        status="Issued"
                    )

                current_invoice_date += relativedelta(months=+agreement.invoice_interval)

        self.stdout.write("Invoices created successfully.")
