from django.core.management.base import BaseCommand
from myapp.models import Agreements, Invoices
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from datetime import datetime

class Command(BaseCommand):
    print("Invoice creation started")
    print("schedulder: auto_create_invoices", datetime.now().strftime("%d.%m.%Y") )

    help = 'Automatically create invoices for all active agreements up to a specified date.'

    def add_arguments(self, parser):
        parser.add_argument('up_to_date', type=str, help='Date in format dd.mm.yyyy to generate invoices up to.')

    def handle(self, *args, **options):
        up_to_date_str = options['up_to_date']
        self.stdout.write(f"Creating invoices up to {up_to_date_str}...")
        
        # Convert the string date to a date object
        up_to_date = datetime.strptime(up_to_date_str, '%d.%m.%Y').date()

        # Fetch all active agreements (excluding closed ones)
        agreements = Agreements.objects.filter(~Q(status="Closed"))

        for agreement in agreements:
            current_invoice_date = agreement.startDate
            last_invoice_date = min(current_invoice_date + relativedelta(months=agreement.months), up_to_date)

            # Loop through the agreement's billing periods until we reach the specified date
            while current_invoice_date < last_invoice_date:
                # Check if an invoice for this period already exists
                if not Invoices.objects.filter(
                    agreement=agreement,
                    date__year=current_invoice_date.year,
                    date__month=current_invoice_date.month
                ).exists():
                    # Calculate quantity and price based on the agreement's data
                    quantity = agreement.invoice_interval
                    price = agreement.rate  # the rate

                    # Create the invoice for the current billing period
                    Invoices.objects.create(
                        date=current_invoice_date,
                        agreement=agreement,
                        quantity=quantity,
                        price=price,
                        status="Issued"
                    )

                # Move to the next billing period based on invoice_interval (months)
                current_invoice_date += relativedelta(months=agreement.invoice_interval)

        self.stdout.write("Invoices created successfully.")
