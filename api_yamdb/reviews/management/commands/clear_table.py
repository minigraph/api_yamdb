import sqlite3

from django.core.management.base import BaseCommand


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
                tables = [options['arguments'][1], ]

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
