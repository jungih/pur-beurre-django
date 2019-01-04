from django.core.management.base import BaseCommand, CommandError
from foods.models import Food

import os
import csv

class Command(BaseCommand):
    help = 'Update database table from csv file'

    def handle(self, *args, **options):
        print('Updating food_food talbe')
        cwd = os.getcwd()
        csv_file =
        with open()
        products = Food.objects.all()
        for product in products:
            obj, created = product.update_or_create()

             poll.save()

            self.stdout.write(self.style.SUCCESS('food_food tablesuccessfully updated')