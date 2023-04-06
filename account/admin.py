from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from account.models import User, CustomerUser, SellerUser, SellerUserImage, Address
from account.forms import CustomUserCreationForm

@admin.register(User)
class MyUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    fieldsets = (
        (_('Login Information'), {'fields': ('email', 'username', 'password')}),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'is_customer', 'is_seller', 'groups', 'user_permissions'
            )
        }),
        (_('Dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # ADD USER FIELD
    add_fieldsets = (
        (_('Login Information'), {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

    list_display = ('email', 'username', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('date_joined',)
    filter_horizontal = (
        'groups',
        'user_permissions',
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('User'), {'fields': ('user',)}),
        (_('Address Personal Information'),
         {'fields': ('address_name', 'first_name', 'last_name', 'company_name', 'phone_number')}),
        (_('Address'), {
            'fields': ('street_address_1', 'street_address_2', 'postal_code', 'city', 'city_area', 'country')
        })
    )

    list_display = ('address_name', 'user', 'city', 'city_area', 'country')
    search_fields = ('address_name', 'user__email__icontains', 'city', 'city_area', 'country__name__icontains')


@admin.register(CustomerUser)
class CustomerUserAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('User'), {'fields': ('user',)}),
        (_('Personal Information'), {'fields': ('first_name', 'last_name', 'phone_number')}),
        (_('Default Addresses'), {'fields': ('default_shipping_address',)}),
        (_('Note'), {'fields': ('note',)}),
    )

    list_display = ('user', 'first_name', 'last_name', 'phone_number')
    search_fields = ('user__email__icontains', 'first_name', 'last_name')

@admin.register(SellerUser)
class SellerUserAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('User'), {'fields': ('user',)}),
        (_('Supplier Information'), {'fields': ('company_name', 'seller_slug', 'code', 'phone_number', 'company_image',)}),
        (_('Contact Information'), {'fields': ('website_url', 'public_phone_number', 'fax_number', 'public_email')}),
        (_('Location Information'), {'fields': ('street_address_1', 'street_address_2', 'postal_code', 'city', 'city_area', 'country', 'latitude', 'longitude')}),
        (_('Verify'), {'fields': ('is_verified',)}),
        (_('Description'), {'fields': ('description',)}),
        (_('Languages'), {'fields': ('languages',)}),
    )

    list_display = ('user', 'company_name', 'website_url')
    list_filter = ('is_verified',)
    search_fields = ('user__email__icontains', 'company_name','website_url', 'seller_slug')

@admin.register(SellerUserImage)
class SellerUserImageAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('User'), {'fields': ('seller',)}),
        (_('Image'), {'fields': ('image_id', 'image')})
    )

    list_display = ('seller', 'image_id', 'image')
    search_fields = ('seller__user__email__icontains' ,'seller__company_name')
    readonly_fields = ('image_id',)