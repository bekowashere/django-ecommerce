from django.core.management import BaseCommand, CommandError
from store.models import ProductAttribute
import json

class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = '_data/store/ProductAttribute.json'

        with open(file_path, 'r', encoding="UTF-8") as f:
            data = json.load(f)

        for attr in data:
            name = attr['name']
            description = attr['description']

            try:
                product_attr = ProductAttribute(
                    name=name,
                    description=description
                )

                product_attr.save()

                self.stdout.write(self.style.SUCCESS(f'Product Attribute "{name}" create successfully'))
            except Exception as e:
                raise CommandError(f'{e}')