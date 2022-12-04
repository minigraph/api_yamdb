# Модуль еще не реализован!!! 2022-12-02 16-56 МСК


import os

from api.serializers import CategorySerializer
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """
    Класс для выполнения из командной строки
    типа python manage.py import_data
    """
    
    # класс еще не реализован!!! 
    
    def handle(self, *args, **options):

        self.load_from_csv()

        # DATA_DIR = os.path.join(os.path.join(settings.BASE_DIR, "static"), "data")
        
        # files = os.listdir(DATA_DIR)

        # import csv
        # for file in files:
        #     full_name = os.path.join(DATA_DIR, file)
        #     print(full_name)
        #     with open(full_name, newline='', encoding='utf8') as csvfile:
        #         spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        #         for row in spamreader:
        #             print(' '.join(row))

    def load_from_csv(self):
        categories_list = self.csv_to_json(r"./static/data/category.csv")

        serializer = CategorySerializer(data=categories_list, many=True)

        print(serializer.is_valid())
        # False

        print(serializer.validated_data)

    def csv_to_json(self, csv_file_path):
        import csv

        with open(csv_file_path, encoding="utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file)

        return csv_reader
