import logging
import os
import sys

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.management.base import BaseCommand

import api.serializers as api_serializers


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        initialize_logger()

        DATA_DIR = os.path.join(
            os.path.join(settings.BASE_DIR, "static"),
            "data"
        )

        files = os.listdir(DATA_DIR)

        logger.info(
            'files to load:'
            f'[{[file for file in files]}]'
        )

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
            logger.info(
                '----------------------------\n'
                f'loading file ... {file_path}'
            )
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
                logger.info('OK')

    def load_from_csv(self, **kvargs):

        import csv
        for key, val in kvargs.items():
            class_params = kvargs[key]
            klass = class_params['class']
            file_path = class_params['file_path']

            with open(file_path, encoding="utf-8") as csv_file:
                try:
                    file_data = list(csv.DictReader(csv_file))
                    serializer = klass(data=file_data, many=True)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        pass
                except Exception as e:
                    self.err = True
                    logger.error(
                        f'error while data loading, see below:\n {e}'
                    )
                    raise


def initialize_logger():
    """
    Инициализурует логгер модуля приложения.
    """

    file_dir = os.path.dirname(os.path.abspath(__file__))
    file_handler = logging.FileHandler(
        filename=os.path.join(file_dir, 'main.log'),
        encoding='utf-8',
    )
    message_format = (
        '%(asctime)s : %(levelname)s'
        ' : %(name)s : LN=%(lineno)d'
        ' : pathname=%(pathname)s : %(message)s'
    )
    stdout_handler = logging.StreamHandler(stream=sys.stdout,)
    handlers = [file_handler, stdout_handler]
    formatter = logging.Formatter(
        message_format,
        '%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    stdout_handler.setFormatter(formatter)
    logging.basicConfig(
        level=logging.INFO,
        handlers=handlers,
        format=message_format,
    )
