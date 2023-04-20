from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from django.core.validators import FileExtensionValidator
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from account.models import User, SellerUser

"""
Review:

Media:
"""
class Category(MPTTModel):
    name = models.CharField(_('Name'), max_length=64)
    slug = models.SlugField(
        _('Slug'),
        unique=True
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        blank=True,
        verbose_name=_('Parent')
    )

    def __str__(self):
        return self.name
    
    def childrens(self):
        return Category.objects.filter(parent=self)
    
    @property
    def any_children(self):
        return Category.objects.filter(parent=self).exists()
    
    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ('name',)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class ProductAttribute(models.Model):
    name = models.CharField(
        _('Attribute Name'),
        max_length=128,
        unique=True
    )
    description = models.TextField(_('Description'), null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name =_('Product Attribute')
        verbose_name_plural = _('Product Attributes')
    
class ProductAttributeValue(models.Model):
    product_attribute = models.ForeignKey(
        ProductAttribute,
        related_name='product_attribute',
        on_delete=models.PROTECT,
        verbose_name=_('Product Attribute')
    )
    attribute_value = models.CharField(
        _('Attribute Value'),
        max_length=255
    )

    def __str__(self):
        value = f'{self.product_attribute.name} -> {self.attribute_value}'
        return value

    class Meta:
        verbose_name =_('Product Attribute Value')
        verbose_name_plural = _('Product Attribute Values')

# through -> ProductTypeAttribute model
class ProductType(models.Model):
    name = models.CharField(
        _('Product Type Name'),
        max_length=255,
        unique=True
    )
    product_type_attribute = models.ManyToManyField(
        ProductAttribute,
        related_name='product_type_attributes',
        through="ProductTypeAttribute",
        verbose_name=_('Attributes')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name =_('Product Type')
        verbose_name_plural = _('Product Types')

class ProductTypeAttribute(models.Model):
    product_attribute = models.ForeignKey(
        ProductAttribute,
        related_name='prod_attribute',
        on_delete=models.PROTECT,
        verbose_name=_('Product Attribute')
    )

    product_type = models.ForeignKey(
        ProductType,
        related_name='prod_type',
        on_delete=models.PROTECT,
        verbose_name=_('Product Type')
    )

    def __str__(self):
        value = f'{self.product_type.name} -> {self.product_attribute.name}'
        return value

    class Meta:
        unique_together = [("product_attribute", "product_type")]
        verbose_name =_('Product Type Attribute')
        verbose_name_plural = _('Product Type Attributes')

class Brand(models.Model):
    name = models.CharField(
        _('Brand Name'),
        max_length=64,
        unique=True
    )

    slug = models.SlugField(
        _('Slug'),
        max_length=128,
        unique=True
    )

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')

# PRODUCT
class Product(models.Model):
    seller = models.ForeignKey(
        SellerUser,
        on_delete=models.CASCADE,
        verbose_name=_('Seller'),
        related_name='seller_products'
    )

    web_id = models.CharField(
        _('Web ID'),
        max_length=64,
        unique=True
    )
    slug = models.SlugField(
        _('Product Slug'),
        max_length=255,
        # unique=True
    )
    name = models.CharField(
        _('Product Name'),
        max_length=255
    )
    category = models.ForeignKey(
        Category,
        related_name = 'category_products',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Category')
    )

    brand = models.ForeignKey(
        Brand,
        related_name = 'brand_products',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Brand')
    )

    description = models.TextField(
        _('Product Description'),
        blank=True
    )

    # FEATURES
    is_active = models.BooleanField(_('Active'), default=True)
    is_new = models.BooleanField(_('New'), default=False)

    # METADA
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.web_id
    
    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ('-created_date',)
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

"""
bir producta birden fazla product inventory bağlıysa detay sayfasında diğer product inventory
ürünlerini de göster
"""
class ProductInventory(models.Model):
    product_type = models.ForeignKey(
        ProductType,
        related_name='product_type',
        on_delete=models.PROTECT
    )
    product = models.ForeignKey(
        Product,
        related_name='product',
        on_delete=models.PROTECT,
        verbose_name=_('Product')
    )
    
    # INVENTORY INFORMATION
    # upc ürünün dünyadaki genel kodu, sku bizim envanterimizde tuttuğumuz kod
    sku = models.CharField(
        _('Stock Keeping Unit'),
        max_length=32,
        unique=True
    )
    upc = models.CharField(
        _('Universal Product Code'),
        max_length=12,
        unique=True
    )
    moq = models.IntegerField(
        _('Minumum Order Quantity'),
        null=True,
        blank=True
    )

    # Field?
    web_slug = models.TextField(
        _('Web Slug')
    )

    # PRICE
    retail_price = models.DecimalField(
        _('Retail Price'),
        max_digits=9,
        decimal_places=2
    )

    store_price = models.DecimalField(
        _('Store Price'),
        max_digits=9,
        decimal_places=2
    )

    # ATTRIBUTES
    attribute_values = models.ManyToManyField(
        ProductAttributeValue,
        related_name='product_attribute_values',
        through="ProductAttributeValues",
        verbose_name=_('Attribute Values')
    )

    # FEATURES
    is_active = models.BooleanField(
        _('Active'),
        default=False
    )
    is_default = models.BooleanField(
        _('Default'),
        default=False
    )
    is_digital = models.BooleanField(
        _('Digital Product'),
        default=False
    )


    weight = models.FloatField(_('Product Weight'), null=True, blank=True)

    # METADA
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sku
    
    def save(self, *args, **kwargs):
        # web_slug = product__slug + sku || product__slug + product__web_id + sku
        new_web_slug = f'{self.product.slug}-{self.product.web_id}-{self.sku}'
        self.web_slug = new_web_slug
        super(ProductInventory, self).save(*args, **kwargs)

    
    class Meta:
        verbose_name = _('Product Inventory')
        verbose_name_plural = _('Product Inventories')

# sonradan değişebiliriz şimdilik böyle basit bir yol
def upload_inventory_media(instance, filename):
    filebase, extension = filename.rsplit('.', 1)
    img_path = f'store/{instance.product_inventory.sku}.{extension}'
    return img_path


class ProductInventoryMedia(models.Model):
    product_inventory = models.ForeignKey(
        ProductInventory,
        related_name='media',
        on_delete=models.PROTECT,
        verbose_name=_('Product Inventory')
    )

    image = models.ImageField(
        _('Product Inventory Image'),
        upload_to=upload_inventory_media,
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])]
    )

    class Meta:
        verbose_name = _('Product Inventory Media')
        verbose_name_plural = _('Product Inventory Medias')


STOCK_STATUS = (
    ('in-stock', _('Available')),
    ('critical', _('Critical')),
    ('out-of-stock', _('Not available')),
)

class Stock(models.Model):
    product_inventory = models.OneToOneField(
        ProductInventory,
        related_name='stock',
        on_delete=models.PROTECT,
        verbose_name=_('Product Inventory')
    )

    units = models.IntegerField(_('Units'), default=0)
    units_sold = models.IntegerField(_('Units Sold'), default=0)

    last_checked_date = models.DateTimeField(
        _('Last Checked Date'),
        null=True,
        blank=True
    )

    status = models.CharField(
        _('Stock Status'),
        max_length=12,
        choices=STOCK_STATUS
    )

    class Meta:
        verbose_name = _('Stock')
        verbose_name_plural = _('Stocks')

class ProductAttributeValues(models.Model):
    attr_values = models.ForeignKey(
        ProductAttributeValue,
        related_name='attr_values',
        on_delete=models.PROTECT,
        verbose_name=_('Attribute Values')
    )
    prod_inventory = models.ForeignKey(
        ProductInventory,
        related_name='prod_attr_values',
        on_delete=models.PROTECT,
        verbose_name=_('Product Inventory')
    )

    def __str__(self):
        value = f'{self.prod_inventory.sku} -> {self.attr_values.attribute_value}'
        return value

    class Meta:
        unique_together = [("attr_values", "prod_inventory")]
        verbose_name =_('Product Inventory Attribute Value ')
        verbose_name_plural = _('Product Inventory Attribute Values')