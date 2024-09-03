import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import transaction

class Command(BaseCommand):
    help = 'Restore data to the database from CSV, XLS, or XLSX backups.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--files', nargs='+', type=str, required=True,
            help='List of backup files to restore.'
        )
        parser.add_argument(
            '--format', type=str, default='csv',
            choices=['csv', 'xls', 'xlsx'],
            help='Format of the backup files (csv, xls, or xlsx). Default is csv.'
        )
        parser.add_argument(
            '--mode', type=str, default='append',
            choices=['append', 'overwrite'],
            help='Mode to restore data: append (default) or overwrite.'
        )

    def handle(self, *args, **kwargs):
        files = kwargs['files']
        file_format = kwargs['format']
        mode = kwargs['mode']

        for file in files:
            model_name = os.path.splitext(os.path.basename(file))[0]
            try:
                model = apps.get_model('myapp', model_name)
                self.import_model(model, file, file_format, mode)
            except LookupError:
                self.stdout.write(self.style.ERROR(f'Model "{model_name}" not found.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing file "{file}": {str(e)}'))

    def import_model(self, model, file, file_format, mode):
        # Read the data from the file
        if file_format == 'csv':
            df = pd.read_csv(file)
        elif file_format == 'xls':
            df = pd.read_excel(file, engine='xlrd')  # Specify engine for XLS
        elif file_format == 'xlsx':
            df = pd.read_excel(file, engine='openpyxl')  # Specify engine for XLSX

        # Convert DataFrame to list of dictionaries
        data = df.to_dict('records')

        with transaction.atomic():
            if mode == 'overwrite':
                model.objects.all().delete()
                self.stdout.write(self.style.SUCCESS(f'Existing data in "{model._meta.verbose_name_plural}" cleared.'))

            # Bulk create
            instances = [model(**record) for record in data]
            model.objects.bulk_create(instances)

            self.stdout.write(self.style.SUCCESS(f'Successfully restored data to "{model._meta.verbose_name_plural}" from {file}.'))
