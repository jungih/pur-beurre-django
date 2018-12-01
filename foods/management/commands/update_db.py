from django.core.management.base import BaseCommand, CommandError
from foods.models import Foods
import csv
import os, sys
import re
from itertools import islice


class Command(BaseCommand):

    help = 'update database'

    def handle(self, *args, **kwargs):

        cwd = os.getcwd()
        file_path = os.path.join(cwd, 'csv/fr.openfoodfacts.org.products.csv')
        new_file = os.path.join(cwd, 'csv/fr.products.csv')
        with open(new_file, 'r', newline='', encoding='utf-8') as csv_file:

            csv_reader = csv.DictReader(csv_file, delimiter='\t')
            print('Updating database table')
            for line in csv_reader:
                try:
                    Foods.objects.get_or_create(code=line['code'],
                                                defaults={
                                                'url':line['url'],
                                                'product_name':line['product_name'],
                                                'quantity':line['quantity'],
                                                'brands':line['brands'],
                                                'categories_fr':line['categories_fr'],
                                                'nutrition_grade_fr':line['nutrition_grade_fr'],
                                                'image_url':line['image_url'],
                                                'countries_fr':line['countries_fr']
                                                })

                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    print('Last saved item code:', line['code'])
                    raise
        self.stdout.write(self.style.SUCCESS('Database updated'))
