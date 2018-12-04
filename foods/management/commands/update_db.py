from django.core.management.base import BaseCommand, CommandError
from foods.models import Foods
import csv
import os
import sys
import re
from itertools import islice


class Command(BaseCommand):

    help = 'update database'

    def handle(self, *args, **kwargs):

        cwd = os.getcwd()
        file_path = os.path.join(cwd, 'csv/fr.openfoodfacts.org.products.csv')
        with open(file_path, 'r', newline='', encoding='utf-8') as csv_file:

            csv_reader = csv.DictReader(csv_file, delimiter='\t')
            previous_code = ''
            for line in csv_reader:
                code = line['code']
                url = line['url']
                product_name = line['product_name']
                brands = line['brands']
                quantity = line['quantity']
                categories_fr = line['categories_fr']
                image_url = line['image_url']
                nutrition_grade_fr = line['nutrition_grade_fr']
                countries_fr = line['countries_fr']
                if code != previous_code:
                    if re.match('France', str(countries_fr), re.I) is not None:
                        if categories_fr:
                            try:
                                Foods.objects.update_or_create(code=line['code'],
                                                               defaults={
                                    'url': url,
                                    'product_name': product_name,
                                    'quantity': quantity,
                                    'brands': brands,
                                    'categories_fr': categories_fr,
                                    'nutrition_grade_fr': nutrition_grade_fr,
                                    'image_url': image_url,
                                    'countries_fr': countries_fr
                                })
                                previous_code = code
                            except:
                                print("Unexpected error:",
                                      sys.exc_info()[0])
                                print('Last saved item code:',
                                      line['code'])
                                raise
        self.stdout.write(self.style.SUCCESS('Database updated'))
