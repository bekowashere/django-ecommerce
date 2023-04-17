from django.core.management import BaseCommand, CommandError
from store.models import ProductType
import json

class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = '_data/store/ProductType.json'

        with open(file_path, 'r', encoding="UTF-8") as f:
            data = json.load(f)

        for type in data:
            name = type['name']

            try:
                product_type = ProductType(
                    name=name
                )

                product_type.save()

                self.stdout.write(self.style.SUCCESS(f'Product Type "{name}" create successfully'))
            except Exception as e:
                raise CommandError(f'{e}')