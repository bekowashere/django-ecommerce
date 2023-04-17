from django.core.management import BaseCommand, CommandError
from store.models import Category, Product
import json

class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = '_data/store/Product.json'

        with open(file_path, 'r', encoding="UTF-8") as f:
            data = json.load(f)

        for prod in data:
            web_id = prod['web_id']
            slug = prod['slug']
            name = prod['name']
            category_name = prod['category_name']
            category_slug = prod['category_slug']
            description = prod['description']

            # GET CATEGORY
            try:
                category = Category.objects.get(slug=category_slug)
            except Category.DoesNotExist:
                category = Category(name=category_name, slug=category_slug)
                category.save()
                
            try:
                product = Product(
                    web_id=web_id,
                    slug=slug,
                    name=name,
                    category=category,
                    description=description
                )

                product.save()

                self.stdout.write(self.style.SUCCESS(f'Product "{web_id}" create successfully'))
            except Exception as e:
                raise CommandError(f'{e}')