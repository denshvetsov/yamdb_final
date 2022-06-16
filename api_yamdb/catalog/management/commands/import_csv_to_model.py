import csv

from django.apps import apps
from django.core.management.base import BaseCommand

from catalog.models import Category, Title
from reviews.models import Review
from users.models import User


class Command(BaseCommand):
    """
    пример команды os x, в одну строчку:
    python3 manage.py import_csv_to_model
    --path static/data/genre.csv --app_name catalog --model_name genre
    протестировано при четком соответствии полей
    """
    help = 'Creating model objects according the file path specified'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help="file path")
        parser.add_argument('--model_name', type=str, help="model name")
        parser.add_argument(
            '--app_name',
            type=str,
            help="django app name that the model is connected to"
        )

    def handle(self, *args, **options):
        file_path = options['path']
        _model = apps.get_model(options['app_name'], options['model_name'])
        with open(file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
            for row in reader:
                try:
                    if row.get('category'):
                        category = Category.objects.get(id=row.get('category'))
                        row.update({'category': category})
                    if row.get('title_id'):
                        title = Title.objects.get(id=row.get('title_id'))
                        row.update({'title': title})
                    if row.get('author'):
                        title = User.objects.get(id=row.get('author'))
                        row.update({'author': title})
                    if row.get('review_id'):
                        review = Review.objects.get(id=row.get('review_id'))
                        row.update({'review': review})
                    obj, created = _model.objects.get_or_create(**row)
                except Exception as ex:
                    print('Ошибка импорта')
                    print(ex)
                    print(row)
