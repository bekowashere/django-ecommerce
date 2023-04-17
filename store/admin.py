from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from store.models import (
    Category,
    ProductAttribute,
    ProductAttributeValue,
    ProductType,
    ProductTypeAttribute,
    Product,
    ProductInventory,
    Stock,
    ProductAttributeValues
)

@admin.register(Category)
class CategoryMPTTAdmin(DraggableMPTTAdmin):
    mptt_indent_field = 'name'
    mptt_level_indent = 50
    list_display = ('tree_actions', 'indented_title', 'related_products_count', 'related_products_cumulative_count')

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
            qs,
            Product,
            'category',
            'products_cumulative_count',
            cumulative=True
        )

        # Add non cumulative product count
        qs = Category.objects.add_related_count(
            qs,
            Product,
            'category',
            'products_count',
            cumulative=False
        )

        return qs
    
    # ! Just main category products count
    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Main Category Products'

    # ! Main category and subcategories total products count
    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'All Products'


admin.site.register(ProductAttribute)
@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ('product_attribute', 'attribute_value')
    search_fields = ('product_attribute__name__icontains', 'attribute_value')

admin.site.register(ProductType)
@admin.register(ProductTypeAttribute)
class ProductTypeAttributeAdmin(admin.ModelAdmin):
    list_display = ('product_type', 'product_attribute')
    list_filter = ('product_type',)
    search_fields = ('product_type__name__icontains', 'product_attribute__name__icontains')

class ProductAttributeValuesInline(admin.TabularInline):
    model = ProductAttributeValues

@admin.register(ProductInventory)
class ProductInventoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Main Information'), {'fields': ('product_type', 'product')}),
        (_('Product Information'), {'fields': ('sku', 'upc', 'moq', 'weight')}),
        (_('Price'), {'fields': ('retail_price', 'store_price')}),
        (_('Features'), {'fields': ('is_active', 'is_default', 'is_digital')}),
        (_('Metadata'), {'fields': ('created_date', 'updated_date')}),
    )

    list_display = ('sku', 'upc')
    list_filter = ('is_active', 'is_default', 'is_digital')
    search_fields = (
        'product__web_id__icontains',
        'product__name__icontains',
        'product__slug__icontains',
        'sku',
        'upc'
    )
    readonly_fields = ('created_date', 'updated_date')
    filter_horizontal = ('attribute_values',)

    inlines = [
        ProductAttributeValuesInline
    ]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Main Information'), {'fields': ('web_id', 'slug', 'name', 'category')}),
        (_('Features'), {'fields': ('is_active', 'is_new')}),
        (_('Description'), {'fields': ('description',)}),
        (_('Metadata'), {'fields': ('created_date', 'updated_date')}),
    )

    list_display = ('web_id', 'slug', 'name')
    list_filter = ('is_active', 'is_new')
    search_fields = ('web_id', 'slug', 'name')
    readonly_fields = ('created_date', 'updated_date')

admin.site.register(Stock)
admin.site.register(ProductAttributeValues)


