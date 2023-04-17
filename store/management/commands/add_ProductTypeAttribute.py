from django.core.management import BaseCommand, CommandError
from store.models import ProductAttribute, ProductType, ProductTypeAttribute
import json

class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = '_data/store/ProductTypeAttribute.json'

        with open(file_path, 'r', encoding="UTF-8") as f:
            data = json.load(f)

        for type_attr in data:
            product_attribute = type_attr['product_attribute']
            product_type = type_attr['product_type']

            # Get Product Attribute
            try:
                prod_attr = ProductAttribute.objects.get(name=product_attribute)
            except ProductAttribute.DoesNotExist:
                prod_attr = ProductAttribute(name=product_attribute)
                prod_attr.save()

            # Get Product Attribute
            try:
                prod_type = ProductType.objects.get(name=product_type)
            except ProductType.DoesNotExist:
                prod_type = ProductType(name=product_type)
                prod_type.save()

            

            try:
                product_type_attribute = ProductTypeAttribute(
                    product_attribute=prod_attr,
                    product_type=prod_type
                )

                product_type_attribute.save()
                self.stdout.write(self.style.SUCCESS(f'Product Type Attribute "{product_type} > {product_attribute}" create successfully'))
            except Exception as e:
                raise CommandError(f'{e}')