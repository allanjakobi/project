import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = 'Backup selected tables or all tables to CSV, XLS, or XLSX files.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--tables', nargs='+', type=str,
            help='List of tables to backup (default is all tables).'
        )
        parser.add_argument(
            '--format', type=str, default='csv',
            choices=['csv', 'xls', 'xlsx'],
            help='Format of the backup files (csv, xls, or xlsx). Default is csv.'
        )

    def handle(self, *args, **kwargs):
        tables = kwargs['tables']
        file_format = kwargs['format']
        
        # Get all models if no tables are specified
        if not tables:
            models = apps.get_models()
        else:
            models = [apps.get_model('myapp', table) for table in tables]

        for model in models:
            self.export_model(model, file_format)

    def export_model(self, model, file_format):
        # Get model name and data
        table_name = model._meta.model_name  # Get the table name in lowercase
        data = model.objects.all().values()

        # Convert QuerySet to DataFrame
        df = pd.DataFrame(data)

        # Define file name
        file_name = f"{table_name}.{file_format}"
        
        # Export to CSV or XLS/XLSX
        if file_format == 'csv':
            df.to_csv(file_name, index=False)
        elif file_format == 'xls':
            # 'xlwt' is used for writing XLS files
            df.to_excel(file_name, index=False, engine='xlwt')
        elif file_format == 'xlsx':
            # 'openpyxl' is used for writing XLSX files
            df.to_excel(file_name, index=False, engine='openpyxl')

        self.stdout.write(self.style.SUCCESS(f'Successfully backed up {table_name} to {file_name}'))
