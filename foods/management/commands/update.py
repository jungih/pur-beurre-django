from django.core.management.base import BaseCommand, CommandError
from foods.models import Food

import csv
import os
import sys
import re

class Command(BaseCommand):

    help = 'update database'

    def handle(self, *args, **kwargs):

        cwd = os.getcwd()
        file_path = os.path.join(cwd, 'csv/fr.openfoodfacts.org.products.csv')
        with open(file_path, 'r', newline='', encoding='utf-8') as csv_file:

            csv_reader = csv.DictReader(csv_file, delimiter='\t')
            previous_code = ''
             self.stdout.write(self.style.SUCCESS('updating...'))
            for line in csv_reader:
                product = {'url': line['url'],
                           'product_name': line['product_name'],
                           'brands': line['brands'],
                           'quantity': line['quantity'],
                           'categories_fr': line['categories_fr'],
                           'image_url': line['image_url'],
                           'nutrition_grade_fr': line['nutrition_grade_fr'],
                           'countries_fr': line['countries_fr']}
                # Current product code
                code = line['code']
                categories_fr = line['categories_fr']
                countries_fr = line['countries_fr']
                # Filter out doubled product
                if code != previous_code:
                    # Select only products from France
                    if re.match('France', str(countries_fr), re.I) is not None:
                        # Select only products that has categories
                        if categories_fr:
                            try:
                                obj, created = Food.objects.update_or_create(
                                            code=line['code'],
                                            defaults=product,)
                                # Set current product code as previous code
                                previous_code = code
                            except:
                                print("Unexpected error:",
                                      sys.exc_info()[0])
                                print('Last saved item code:',
                                      line['code'])
                                raise
        self.stdout.write(self.style.SUCCESS('Database updated'))