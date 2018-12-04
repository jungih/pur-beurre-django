from django.core.management.base import BaseCommand, CommandError
# from foods.models import Foods
import csv
import os
import re
from itertools import islice


class Command(BaseCommand):

    help = 'filter products from france'

    def handle(self, *args, **kwargs):

        cwd = os.getcwd()
        file_path = os.path.join(cwd, 'csv/fr.openfoodfacts.org.products.csv')
        new_file = os.path.join(cwd, 'csv/fr.products.csv')
        with open(file_path, 'r', newline='', encoding='utf-8') as csv_file:

            csv_reader = csv.DictReader(csv_file, delimiter='\t')

            with open(new_file, 'w', newline='', encoding='utf-8') as new_csv:
                fieldnames = ['code', 'url', 'product_name', 'quantity', 'brands', 'categories_tags',
                              'nutrition_grade_fr', 'image_url', 'countries_fr']
                csv_writer = csv.DictWriter(
                    new_csv, delimiter='\t', fieldnames=fieldnames)
                csv_writer.writeheader()
                previous_code = '0'
                for line in csv_reader:
                    code = line['code']
                    url = line['url']
                    product_name = line['product_name']
                    brands = line['brands']
                    quantity = line['quantity']
                    categories_tags = line['categories_tags']
                    image_url = line['image_url']
                    nutrition_grade_fr = line['nutrition_grade_fr']
                    countries_fr = line['countries_fr']
                    if code != previous_code:
                        if re.match('France', str(countries_fr), re.I) is not None:
                            if categories_tags:
                                csv_writer.writerow(
                                    {'code': code,
                                     'url': url,
                                     'product_name': product_name,
                                     'brands': brands,
                                     'quantity': quantity,
                                     'categories_tags': categories_tags,
                                     'image_url': image_url,
                                     'nutrition_grade_fr': nutrition_grade_fr,
                                     'countries_fr': countries_fr}
                                )
                                previous_code = code
        self.stdout.write(self.style.SUCCESS('New CSV file created '))
