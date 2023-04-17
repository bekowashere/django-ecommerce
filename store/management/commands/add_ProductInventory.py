from django.core.management import BaseCommand, CommandError
from store.models import (
    Category,
    Product,
    ProductInventory,
    ProductType,
    ProductAttribute,
    ProductAttributeValue,
    ProductAttributeValues
)
import json

class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = '_data/store/ProductInventory.json'

        with open(file_path, 'r', encoding="UTF-8") as f:
            data = json.load(f)

        for prod_inventory in data:
            product_type_name = prod_inventory['product_type']
            product_web_id = prod_inventory['product']
            sku = prod_inventory['sku']
            upc = prod_inventory['upc']
            moq = prod_inventory['moq']
            retail_price = prod_inventory['retail_price']
            store_price = prod_inventory['store_price']
            is_active = prod_inventory['is_active']
            is_default = prod_inventory['is_default']
            is_digital = prod_inventory['is_digital']
            weight = prod_inventory['weight']

            inventory_attribute_values = prod_inventory['attribute_values']

            # GET PRODUCT TYPE
            try:
                product_type = ProductType.objects.get(name=product_type_name)
            except ProductType.DoesNotExist:
                product_type = ProductType(name=product_type_name)
                product_type.save()

            # GET PRODUCT
            try:
                product = Product.objects.get(web_id=product_web_id)
            except Product.DoesNotExist:
                raise CommandError("Product does not exist")
                
            try:
                product_inventory = ProductInventory(
                    product_type=product_type,
                    product=product,
                    sku=sku,
                    upc=upc,
                    moq=moq,
                    retail_price=retail_price,
                    store_price=store_price,
                    is_active=is_active,
                    is_default=is_default,
                    is_digital=is_digital,
                    weight=weight
                )

                product_inventory.save()

                for attr in inventory_attribute_values:
                    prod_attr = attr['product_attribute']
                    attr_value = attr['attribute_value']

                    # GET ProductAttribute
                    try:
                        product_attribute = ProductAttribute.objects.get(name=prod_attr)
                    except ProductAttribute.DoesNotExist:
                        product_attribute = ProductAttribute(name=prod_attr)
                        product_attribute.save()

                    # GET ProductAttributeValue
                    try:
                        product_attribute_value = ProductAttributeValue.objects.get(
                            product_attribute=product_attribute,
                            attribute_value=attr_value
                        )
                    except ProductAttributeValue.DoesNotExist:
                        raise CommandError("ProductAttributeValue does not exist")

                    # CREATE ProductAttributeValues -> Inventory Values
                    inventory_product_attribute_values = ProductAttributeValues(
                        attr_values=product_attribute_value,
                        prod_inventory=product_inventory
                    )
                    inventory_product_attribute_values.save()

                self.stdout.write(self.style.SUCCESS(f'ProductInventory "{sku}" create successfully'))
            except Exception as e:
                raise CommandError(f'{e}')