from django.core.management import BaseCommand, CommandError
from store.models import ProductAttribute, ProductAttributeValue
import json

class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = '_data/store/ProductAttributeValue.json'

        with open(file_path, 'r', encoding="UTF-8") as f:
            data = json.load(f)

        for attr_value in data:
            product_attribute = attr_value['product_attribute']
            attribute_value = attr_value['attribute_value']

            try:
                prod_attr = ProductAttribute.objects.get(name=product_attribute)
            except ProductAttribute.DoesNotExist:
                prod_attr = ProductAttribute(name=product_attribute)
                prod_attr.save()

            try:
                product_attribute_value = ProductAttributeValue(
                    product_attribute=prod_attr,
                    attribute_value=attribute_value
                )

                product_attribute_value.save()
                self.stdout.write(self.style.SUCCESS(f'Product Attribute Value "{attribute_value}" create successfully'))
            except Exception as e:
                raise CommandError(f'{e}')