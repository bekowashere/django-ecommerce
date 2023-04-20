from rest_framework import serializers
from django.utils.text import slugify

from store.models import (
    Category,
    ProductAttribute,
    ProductAttributeValue,
    ProductType,
    ProductTypeAttribute,
    Product,
    ProductInventory,
    ProductInventoryMedia,
    Stock,
    ProductAttributeValues
)

from account.models import User, SellerUser

# PRODUCT
class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'web_id',
            'name',
            'slug',
            'category',
            'brand',
            'description'
        )
        extra_kwargs = {
            'slug': {'required':False},
        }

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user

        sellerUser = SellerUser.objects.get(user=user)
        
        product = Product.objects.create(
            seller=sellerUser,
            web_id=validated_data['web_id'],
            name=validated_data['name'],
            slug=slugify(validated_data['name']),
            category=validated_data['category'],
            brand=validated_data['brand'],
            description=validated_data['description']
        )

        return product
    
    def update(self, instance, validated_data):
        instance.web_id = validated_data.get('web_id', instance.web_id)
        instance.name = validated_data.get('name', instance.name)
        instance.category = validated_data.get('category', instance.category)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.description = validated_data.get('description', instance.description)

        instance.save()

        return instance
    
# PRODUCT INVENTORY
class ProductInventoryMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInventoryMedia
        fields = ('image',)

class ProductInventoryCreateUpdateSerializer(serializers.ModelSerializer):
    images = ProductInventoryMediaSerializer(source='media', many=True, read_only=True)
    
    class Meta:
        model = ProductInventory
        fields = (
            'product_type',
            'product',
            'sku',
            'upc',
            'moq',
            'web_slug',
            'retail_price',
            'store_price',
            'is_active',
            'is_default',
            'is_digital',
            'weight',
            'attribute_values',
            'images'
        )
        extra_kwargs = {
            'web_slug': {'read_only': True}
        }

    def create(self, validated_data):
        request = self.context.get("request")

        product_inventory = ProductInventory.objects.create(
            product_type=validated_data['product_type'],
            product=validated_data['product'],
            sku=validated_data['sku'],
            upc=validated_data['upc'],
            moq=validated_data['moq'],
            retail_price=validated_data['retail_price'],
            store_price=validated_data['store_price'],
            is_default=validated_data['is_default'],
            is_digital=validated_data['is_digital']
        )

        # IMAGES
        images_data = request.FILES
        if len(images_data) > 0:
            for image_data in images_data.values():
                ProductInventoryMedia.objects.create(
                    product_inventory=product_inventory,
                    image=image_data
                )

        """
        ProductAttributeValues
        prod_inventory = FK(ProductInventory, related_name='prod_attr_values')
        attr_values = FK(ProductAttributeValue, related_name='attr_values')
        
        product_type seçtik Televizyon
        ptype="Televizyon"
        qs = ProductTypeAttribute.objects.filter(product_type=ptype)
        """

        return product_inventory

class ProductTypeAttributeSerializer(serializers.ModelSerializer):
    pass