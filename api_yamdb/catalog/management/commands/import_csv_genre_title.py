import csv

from django.core.management.base import BaseCommand

from catalog.models import Genre, Title


class Command(BaseCommand):
    """
    импорт свзи ManyToMany
    пример команды os x:
    python3 manage.py import_csv_genre_title --path static/data/genre_title.csv
    """
    help = 'Creating model objects according the file path specified'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help="file path")

    def handle(self, *args, **options):
        file_path = options['path']
        with open(file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',', quotechar='|')
            for row in reader:
                try:
                    title_obj_exist = Title.objects.filter(
                        id=row.get('title_id')
                    ).exists()
                    genre_obj_exist = Genre.objects.filter(
                        id=row.get('genre_id')
                    ).exists()
                    if title_obj_exist and genre_obj_exist:
                        title = Title.objects.get(id=row.get('title_id'))
                        genre = Genre.objects.get(id=row.get('genre_id'))
                        title.genre.add(genre)
                        title.save()
                except Exception as error:
                    print(f'Импортируйте все зависимые таблицы {error}')
                    print(row)
