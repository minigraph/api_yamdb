import sqlite3

from django.core.management.base import BaseCommand
from reviews import models as review_models
from users import models as user_models


class Command(BaseCommand):
    """
    Use: 
        python manage.py clear_table tablename <table name>
    For delete all tables use:
        python manage.py clear_table tablename all
    For help:
        python manage.py clear_table help
    """

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('arguments', nargs='+', type=str)

    def handle(self, *args, **options):


        if not options['arguments']:
            return
        if options['arguments'][0] == 'help':
            print(__class__.__doc__)
            return

        # tables = [('reviews_' + item).casefold() for item in dir(review_models) 
        # if not item.startswith('__') and not item.startswith('_') and callable(getattr(review_models, item))]
        # tables2 = [('users_' + item).casefold() for item in dir(user_models) 
        #             if not item.startswith('__') and not item.startswith('_') and callable(getattr(user_models, item))]
        # tables += tables2
        # print(tables)
        # return

        if options['arguments'][0] == 'tablename':
            if options['arguments'][1] == 'all':
                tables = [
                    'reviews_category',
                    'reviews_comment',
                    'reviews_genre',
                    'reviews_genresoftitles',
                    'reviews_review',
                    'reviews_title',
                    'users_customuser',
                ]
            else:
                table = [options['arguments'][1],]

            for table in tables:
                self.tablename = table
                self.clear_table()
                print(f'table {self.tablename} is cleared')
            return
        else:
            print(__class__.__doc__)

    def clear_table(self):
        table = self.tablename

        cn = sqlite3.connect('db.sqlite3')

        cur = cn.cursor()

        cur.execute(
            f'''
            DELETE FROM {table}
            '''
        )
        cn.commit()
        cur.close()
        cn.close()