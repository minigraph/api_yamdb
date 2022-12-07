import os
from django.core.management.base import BaseCommand, CommandError
from reviews.models import Title, Genre, Category
from django.conf import settings

import api.serializers as api_serializers


class Command(BaseCommand):

    def handle(self, *args, **options):

        DATA_DIR = os.path.join(
            os.path.join(settings.BASE_DIR, "static"),
            "data"
        )

        files = os.listdir(DATA_DIR)

        print('files to load:')
        [print(file) for file in files]

        parameters = {
            'UserSerializer':
                {
                 'class': api_serializers.UserSerializer,
                 'file_name': 'users.csv',
                },
            'CategorySerializer':
                {
                 'class': api_serializers.CategorySerializer,
                 'file_name': 'category.csv',
                },
            'GenreSerializer':
                {
                 'class': api_serializers.GenreSerializer,
                 'file_name': 'genre.csv',
                },
            'TitleSerializer':
                {
                 'class': api_serializers.TitleSerializer,
                 'file_name': 'titles.csv',
                },
            'GenresOfTitlesSerializer':
                {
                 'class': api_serializers.GenresOfTitlesSerializer,
                 'file_name': 'genre_title.csv',
                },
            'ReviewSerializer':
                {
                 'class': api_serializers.ReviewSerializer,
                 'file_name': 'review.csv',
                },
        }

        for key, value in parameters.items():
            class_name = key
            file_path = os.path.join(DATA_DIR, value['file_name'])
            klass = value['class']
            print('-' * 50)
            print('loading file ... ', file_path)
            params = {
                class_name: {
                    'class': klass,
                    'file_path': file_path,
                }
            }
            parameters[class_name] = {
                'class': klass,
                'file_path': file_path,
            }
            self.err = False
            self.load_from_csv(**params)
            if not self.err:
                print('OK')

    def load_from_csv(self, **kvargs):

        import csv
        for key, val in kvargs.items():
            class_params = kvargs[key]
            klass = class_params['class']
            file_path = class_params['file_path']

            with open(file_path, encoding="utf-8") as csv_file:
                file_data = list(csv.DictReader(csv_file))
                serializer = klass(data=file_data, many=True)
                if serializer.is_valid():
                    try:
                        serializer.save()
                    except Exception as e:
                        self.err = True
                        print('error while data loading: ', e)
                else:
                    print('validated_data', serializer.validated_data)
