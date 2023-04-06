from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password, check_password
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from account.utils import generate_seller_code, generate_random_seller_code
# MODELS
from account.models import User, CustomerUser, SellerUser, SellerUserImage, Address

from world.models import Country

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'is_active', 'is_customer', 'is_seller'
        )

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        # return str(token)
        return str(token.access_token)
    
    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'is_active', 'is_customer', 'is_seller', 'token'
        )

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = (
            'first_name', 'last_name', 'phone_number'
        )
        # extra_kwargs = {
        #     'default_shipping_address': {'read_only': True},
        #     'note': {'read_only': True}
        # }

# CUSTOMER LOGIN
class DefaultShippingAddressSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField()

    def get_country(self, obj):
        return obj.country.name
    
    class Meta:
        model = Address
        fields = (
            'id', 'address_name', 'country'
        )

class CustomerSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    email = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()
    is_customer = serializers.SerializerMethodField()
    is_seller = serializers.SerializerMethodField()
    default_shipping_address = DefaultShippingAddressSerializer()


    def get_token(self, obj):
        token = RefreshToken.for_user(obj.user)
        return str(token.access_token)
    
    def get_email(self, obj):
        return obj.user.email

    def get_username(self, obj):
        return obj.user.username
    
    def get_is_active(self, obj):
        return obj.user.is_active

    def get_is_customer(self, obj):
        return obj.user.is_customer
    
    def get_is_seller(self, obj):
        return obj.user.is_seller
    
    class Meta:
        model = CustomerUser
        fields = (
            'user',
            'email',
            'username',
            'is_active',
            'is_customer',
            'is_seller',
            'first_name',
            'last_name',
            'phone_number',
            'token',
            'default_shipping_address'
        )

# CUSTOMER REGISTER
class CustomerRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    token = serializers.SerializerMethodField(read_only=True)

    customeruser = CustomerSerializer(required=True)

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'password',
            'password2',
            'is_active',
            'is_customer',
            'is_seller',
            'customeruser',
            'token',
        )
        extra_kwargs = {
            'username': {'read_only': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        email = validated_data['email']
        _username = email.split('@')[0]

        ex = False
        ex = User.objects.filter(username=_username).exists()
        while ex:
            _username = f'{_username}-{get_random_string(9, "0123456789")}'
            ex = User.objects.filter(username=_username).exists()

        # User
        user = User.objects.create(
            username=_username,
            email=email,
            is_active=True,
            is_customer=True,
        )
        
        user.set_password(validated_data['password'])
        user.save()

        # Customer
        customer_data = validated_data.pop('customeruser')
        first_name = customer_data['first_name']
        last_name = customer_data['last_name']
        phone_number = customer_data['phone_number']

        CustomerUser.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number
        )
        return user
    
# ADRESS
class DefaultAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ('default_shipping_address',)

    def update(self, instance, validated_data):
        instance.default_shipping_address = validated_data.get('default_shipping_address', instance.default_shipping_address)

        instance.save()

        return instance

# CUSTOMER PROFILE INFORMATION
class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = (
            'first_name',
            'last_name',
            'phone_number'
        )
        extra_kwargs = {
            'first_name': {'required':True},
            'last_name': {'required':True}
        }

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)

        instance.save()
        
        return instance

    
class AddressSerializer(serializers.ModelSerializer):
    # country = serializers.SerializerMethodField()

    # def get_country(self, obj):
    #     return obj.country.name
    
    class Meta:
        model = Address
        exclude = ['user']

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user

        customerUser = CustomerUser.objects.get(user=user)
        address = Address.objects.create(
            user=customerUser,
            address_name=validated_data['address_name'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            company_name=validated_data['company_name'],
            phone_number=validated_data['phone_number'],
            street_address_1=validated_data['street_address_1'],
            street_address_2=validated_data['street_address_2'],
            postal_code=validated_data['postal_code'],
            city=validated_data['city'],
            city_area=validated_data['city_area'],
            country=validated_data['country']
        )

        if customerUser.default_shipping_address is None:
            customerUser.default_shipping_address = address

        customerUser.save()

        return address
    
    def update(self, instance, validated_data):
        instance.address_name = validated_data.get('address_name', instance.address_name)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.street_address_1 = validated_data.get('street_address_1', instance.street_address_1)
        instance.street_address_2 = validated_data.get('street_address_2', instance.street_address_2)
        instance.postal_code = validated_data.get('postal_code', instance.postal_code)
        instance.city = validated_data.get('city', instance.city)
        instance.city_area = validated_data.get('city_area', instance.city_area)
        instance.country = validated_data.get('country', instance.country)

        instance.save()

        return instance
# SELLER LOGIN
class SellerSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    email = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()
    is_customer = serializers.SerializerMethodField()
    is_seller = serializers.SerializerMethodField()

    def get_token(self, obj):
        token = RefreshToken.for_user(obj.user)
        return str(token.access_token)
    
    def get_email(self, obj):
        return obj.user.email

    def get_username(self, obj):
        return obj.user.username
    
    def get_is_active(self, obj):
        return obj.user.is_active

    def get_is_customer(self, obj):
        return obj.user.is_customer
    
    def get_is_seller(self, obj):
        return obj.user.is_seller
    
    class Meta:
        model = SellerUser
        fields = (
            'user',
            'email',
            'username',
            'is_active',
            'is_customer',
            'is_seller',
            'company_name',
            'company_image',
            'seller_slug',
            'code',
            'phone_number',
            'description',
            'website_url',
            'public_email',
            'public_phone_number',
            'fax_number',
            # location
            'street_address_1',
            'street_address_2',
            'postal_code',
            'city',
            'city_area',
            'country',
            'latitude',
            'longitude',
            'token'
        )

# SELLER REGISTER
class SellerSerializer(serializers.ModelSerializer):
    # required = False to auto create seller_slug & code
    class Meta:
        model = SellerUser
        fields = (
            'company_name', 'seller_slug', 'code', 'phone_number'
        )
        extra_kwargs = {
            'seller_slug': {'required':False},
            'code': {'required':False}
        }

class SellerRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    token = serializers.SerializerMethodField(read_only=True)

    selleruser = SellerSerializer(required=True)

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'password',
            'password2',
            'is_active',
            'is_customer',
            'is_seller',
            'selleruser',
            'token'
        )
        extra_kwargs = {
            'username': {'read_only': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        email = validated_data['email']
        _username = email.split('@')[0]

        ex = False
        ex = User.objects.filter(username=_username).exists()
        while ex:
            _username = f'{_username}-{get_random_string(9, "0123456789")}'
            ex = User.objects.filter(username=_username).exists()

        # User
        user = User.objects.create(
            username=_username,
            email=email,
            is_active=True,
            is_seller=True,
        )
        
        user.set_password(validated_data['password'])
        user.save()

        # Seller
        seller_data = validated_data.pop('selleruser')
        company_name = seller_data['company_name']
        phone_number = seller_data['phone_number']

        # seller_slug
        seller_slug = slugify(company_name)
        exs_slug = False
        exs_slug = SellerUser.objects.filter(seller_slug=seller_slug).exists()
        while exs_slug:
            seller_slug = f'{seller_slug}-{get_random_string(9, "0123456789")}'
            exs_slug = SellerUser.objects.filter(seller_slug=seller_slug).exists()
        
        # code
        seller_code = generate_seller_code(company_name)
        exs_code = False
        exs_code = SellerUser.objects.filter(code=seller_code).exists()
        while exs_code:
            seller_code = generate_random_seller_code()
            exs_code = SellerUser.objects.filter(code=seller_code).exists()

        SellerUser.objects.create(
            user=user,
            company_name=company_name,
            seller_slug=seller_slug,
            code=seller_code,
            phone_number=phone_number
        )
        return user
# SELLER COMPANY IMAGE
class SellerCompanyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerUser
        fields = (
            'company_image'
        )

    def update(self, instance, validated_data):
        instance.company_image = validated_data.get('company_image', instance.company_image)
        instance.save()

        return instance
# SELLER USER IMAGE
class SellerUserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerUserImage
        fields = ('image_id', 'image')

# SELLER MULTIPLE IMAGES
# V1
class SellerCreateMultipleImageSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        return SellerUserImageSerializer(obj.get_all_images, many=True).data
    
    class Meta:
        model = SellerUser
        fields = ('user', 'company_name', 'images')
        extra_kwargs = {
            'user': {'read_only': True},
            'company_name': {'read_only': True}
        }
        
    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        images_data = request.FILES

        sellerUser = SellerUser.objects.get(user=user)

        for image_data in images_data.values():
            SellerUserImage.objects.create(seller=sellerUser, image=image_data)

        return sellerUser

# V2
class SellerCreateMultipleImageSerializerV2(serializers.ModelSerializer):
    class Meta:
        model = SellerUserImage
        fields = ('image_id', 'image')


# SELLER COMPANY IMAGE
class SellerCompanyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerUser
        fields = (
            'user', 'company_name', 'company_image'
        )
        extra_kwargs = {
            'user': {'read_only': True},
            'company_name': {'read_only': True}
        }

    def update(self, instance, validated_data):
        # request = self.context.get("request")
        # imgs = request.FILES
        # img = request.FILES.get('company_image')

        instance.company_image = validated_data.get('company_image', instance.company_image)
        instance.save()

        return instance

# SELLER PROFILE
class SellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerUser
        fields = (
            'company_name',
            'description'
        )

    def update(self, instance, validated_data):
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.description = validated_data.get('description', instance.description)

        instance.save()

        return instance
    
# SELLER SLUG
class SellerSlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerUser
        fields = ('seller_slug',)
        validators = [
            UniqueTogetherValidator(
                queryset=SellerUser.objects.all(),
                fields=['seller_slug']
            )
        ]
    
    def update(self, instance, validated_data):
        instance.seller_slug = validated_data.get('seller_slug', instance.seller_slug)
        instance.save()

        return instance
    
# SELLER CODE
class SellerCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerUser
        fields = ('code',)
        validators = [
            UniqueTogetherValidator(
                queryset=SellerUser.objects.all(),
                fields=['code']
            )
        ]
    
    def update(self, instance, validated_data):
        instance.code = validated_data.get('code', instance.code)
        instance.save()

        return instance


# SELLER CONTACT 
class SellerContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerUser
        fields = (
            'website_url',
            'public_email',
            'public_phone_number',
            'fax_number'
        )
        # User email & SellerUser public_email control !
        validators = [
            UniqueTogetherValidator(
                queryset=SellerUser.objects.all(),
                fields=['public_email']
            )
        ]

    def validate_public_email(self, value):
        if User.objects.filter(email=value).exists():
            print("böyle bi email var")
            raise serializers.ValidationError("Account already exists with this email")
        return value
        
    def update(self, instance, validated_data):
        instance.website_url = validated_data.get('website_url', instance.website_url)
        instance.public_email = validated_data.get('public_email', instance.public_email)
        instance.public_phone_number = validated_data.get('public_phone_number', instance.public_phone_number)
        instance.fax_number = validated_data.get('fax_number', instance.fax_number)
        
        instance.save()

        return instance

# SELLER LOCATION
class SellerLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerUser
        fields = (
            'street_address_1',
            'street_address_2',
            'postal_code',
            'city',
            'city_area',
            'country'
        )
        extra_kwargs = {
            'postal_code': {'required':True},
            'city': {'required':True},
            'city_area': {'required':True},
            'country': {'required':True}
        }
        

    def validate_street_address_1(self, value):
        if len(value)<16:
            raise serializers.ValidationError("Street Address 1 must be a minimum of 16 characters!")
        return value
    
    def update(self, instance, validated_data):
        instance.street_address_1 = validated_data.get('street_address_1', instance.street_address_1)
        instance.street_address_2 = validated_data.get('street_address_2', instance.street_address_2)
        instance.postal_code = validated_data.get('postal_code', instance.postal_code)
        instance.city = validated_data.get('city', instance.city)
        instance.city_area = validated_data.get('city_area', instance.city_area)
        instance.country = validated_data.get('country', instance.country)

        instance.save()
        
        return instance
    

##########################################################
class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    model = User
