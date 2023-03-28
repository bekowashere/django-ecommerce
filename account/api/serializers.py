from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.utils.crypto import get_random_string
from django.utils.text import slugify

# MODELS
from account.models import User, CustomerUser, SellerUser, Address

from world.models import Country

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'is_active', 'is_customer', 'is_seller'
        )

class  UserSerializerWithToken(UserSerializer):
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
    
    class Meta:
        model = CustomerUser
        fields = (
            'user',
            'email',
            'username',
            'first_name',
            'last_name',
            'phone_number',
            'is_active',
            'is_customer',
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