from django.db import models
import uuid
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from account.utils import generate_seller_code, generate_random_seller_code

# WORLD
from world.models import Language, Country

class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with given email and password (required fields)
        extra_fields --> first_name, last_name..
        """

        if not email:
            raise ValueError(_('You must provide an email address'))
        
        if not password:
            raise ValueError(_('User must have a password'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a 'Normal' user. For this reason is_staff and is_superuser fields are False
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user = self._create_user(email, password=password, **extra_fields)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        """
        Create and save a 'Super' user. For this reason is_staff and is_superuser fields are True
        """

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))
        
        user = self._create_user(email, password=password, **extra_fields)
        return user
    

class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('Username'),
        max_length=64,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        }
    )

    email = models.EmailField(
        _('Email Address'),
        unique=True,
        help_text=_('Required. 50 characters or fewer. Example: john.doe@gmail.com'),
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )

    is_active = models.BooleanField(_('Active'), default=True)
    is_staff = models.BooleanField(_('Staff User'), default=False)
    is_superuser = models.BooleanField(_('Superuser'), default=False)

    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    last_login = models.DateTimeField(auto_now=True)

    is_customer = models.BooleanField(_('Customer'), default=False)
    is_seller = models.BooleanField(_('Seller'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.get_username()
    
    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        'account.CustomerUser',
        on_delete=models.CASCADE,
        related_name='customer_addresses',
        verbose_name=_('Customer')
    )
    address_name = models.CharField(_('Address Name'), max_length=64, help_text="Ex: Home")
    first_name = models.CharField(_('First Name'), max_length=64)
    last_name = models.CharField(_('Last Name'), max_length=64)
    company_name = models.CharField(_('Company Name'), max_length=64, null=True, blank=True)
    
    # Phone number validator process --> frontend 
    phone_number = models.CharField(
        _('Phone'),
        max_length=32,
        null=True,
        blank=True,
    )

    # Address Information
    street_address_1 = models.CharField(_('Street Address 1'), max_length=256)
    street_address_2 = models.CharField(_('Street Address 2'), max_length=256, null=True, blank=True)
    postal_code = models.CharField(_('Postal Code'), max_length=32)
    city = models.CharField(_('City'), max_length=64, help_text="Ex: Los Angeles")
    city_area = models.CharField(_('City Area'), max_length=64, help_text="Ex: California")

    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        related_name='adddress_country',
        verbose_name=_('Country'),
        null=True
    )

    def __str__(self):
        return self.address_name
    
    @property
    def full_name(self):
        """
        Return the first_name + last_name
        """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name
    
    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

class CustomerUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name=_('User')
    )

    first_name = models.CharField(_('First Name'), max_length=64, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=64, blank=True)

    phone_number = models.CharField(
        _('Phone'),
        max_length=32,
        null=True,
        blank=True,
    )

    default_shipping_address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        related_name='shipping_address',
        null=True,
        blank=True,
        verbose_name=_('Default Shipping Address')
    )

    note = models.TextField(_('Admin Note'), null=True, blank=True)

    def __str__(self):
        return self.user.email
    
    def get_full_name(self):
        """
        Return the first_name + last_name
        """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name
    
    @property
    def get_all_addresses(self):
        return self.customer_addresses.all()

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

def default_seller_image_path():
    return f'account/sellers/default.png'

def upload_seller_image(instance, filename):
    filebase, extension = filename.rsplit('.', 1)
    return f'account/sellers/{instance.user}/main_image.{extension}'

class SellerUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name=_('User')
    )

    company_image = models.ImageField(
        _('Company Image'),
        upload_to=upload_seller_image,
        default=default_seller_image_path,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])]
    )

    company_name = models.CharField(_('Company Name'), max_length=128)
    seller_slug = models.SlugField(_('Slug'))
    code = models.CharField(_('Company Code'), max_length=4, unique=True)
    description = models.TextField(_('Description'), null=True, blank=True)
    website_url = models.URLField(_('Website'), null=True, blank=True, help_text='www.my-site.com')

    # Contact Fields
    # phone_number for account management (reset password, send sms..)
    # public_phone_number for everyone
    phone_number = models.CharField(_('Hidden Phone'), max_length=32, null=True, blank=True)
    public_phone_number = models.CharField(_('Public Phone'), max_length=32, null=True, blank=True)
    public_email = models.EmailField(_('Email Address'), null=True, blank=True)
    fax_number = models.CharField(_('Fax'), max_length=32, null=True, blank=True)

    # Location
    street_address_1 = models.CharField(_('Street Address 1'), max_length=256, null=True, blank=True)
    street_address_2 = models.CharField(_('Street Address 2'), max_length=256, null=True, blank=True)
    postal_code = models.CharField(_('Postal Code'), max_length=32, null=True, blank=True)
    city = models.CharField(_('City'), max_length=64, null=True, blank=True, help_text="Ex: Los Angeles")
    city_area = models.CharField(_('City Area'), max_length=64, null=True, blank=True, help_text="Ex: California")

    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        related_name='s_addresses',
        verbose_name=_('Country'),
        null=True,
        blank=True
    )

    latitude = models.DecimalField(_('Latitude'), max_digits=11, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(_('Longitude'), max_digits=11, decimal_places=8, null=True, blank=True)

    is_verified = models.BooleanField(_('Verified'), default=False)

    languages = models.ManyToManyField(
        Language,
        verbose_name=_('Languages'),
        help_text=_('Select spoken languages'),
        blank=True
    )

    # TO-DO
    # rating
    # get_products
    # get_products_count
    # get_comments

    @property
    def get_all_images(self):
        return self.seller_multiple_images.all()

    def __str__(self):
        return self.company_name
    
    # def save(self, *args, **kwargs):
    #     # seller_slug
    #     seller_slug = slugify(self.company_name)
    #     exs_slug = False
    #     exs_slug = self.__class__.objects.filter(seller_slug=seller_slug)
    #     while exs_slug:
    #         seller_slug = f'{seller_slug}-{get_random_string(9, "0123456789")}'
    #         exs_slug = self.__class__.objects.filter(seller_slug=seller_slug)
    #     self.seller_slug = seller_slug
        
    #     # code
    #     seller_code = generate_seller_code(self.company_name)
    #     exs_code = False
    #     # exs_code = SellerUser.objects.filter(code=seller_code).exists()
    #     exs_code = self.__class__.objects.filter(code=seller_code).exists()
    #     while exs_code:
    #         seller_code = generate_random_seller_code()
    #         exs_code = self.__class__.objects.filter(code=seller_code).exists()
    #     self.code = seller_code
        
    #     super(SellerUser, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if (self.street_address_1 and self.postal_code and self.city and self.city_area and self.country):
            self.is_verified = True
        
        super(SellerUser, self).save(*args, **kwargs)
    
    class Meta:
        # ordering rating
        ordering = ('company_name',)
        verbose_name = _('Seller')
        verbose_name_plural = _('Sellers')

def upload_seller_multiple_image(instance, filename):
    filebase ,extension = filename.split('.', 1)
    return f'account/sellers/{instance.seller.user}/{instance.image_id}.{extension}'

class SellerUserImage(models.Model):
    seller = models.ForeignKey(
        SellerUser,
        on_delete=models.CASCADE,
        verbose_name=_('Seller'),
        related_name='seller_multiple_images'
    )

    image_id = models.UUIDField(
        _('Image ID'),
        default=uuid.uuid4,
        editable=False
    )

    image = models.ImageField(
        _('Image'),
        upload_to=upload_seller_multiple_image,
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])]
    )

    def __str__(self):
        return str(self.image_id)
    
    # property image url
    
    class Meta:
        verbose_name = _('Seller Image')
        verbose_name_plural = _('Seller Images')