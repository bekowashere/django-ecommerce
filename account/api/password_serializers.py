# PASSWORD - EMAIL
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

# MODELS
from account.models import User, CustomerUser, SellerUser

# CHANGE PASSWORD
class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    model = User

    # def validate_old_password(self, value):
    #     request = self.context.get("request")
    #     user = request.user
    #     valid = user.check_password(value)

    #     if not valid:
    #         raise serializers.ValidationError({"old_password": "Old password is not correct"})
    #     return value
        
    def validate_new_password(self, value):
        validate_password(value)
        return value
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs
    
#  FORGOT PASSWORD - SEND EMAIL
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    model = User

    # böyle bir mail var mı exist mi
    # girilen değerin email olup olmadığını kontrol etme?

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email address does not exist"})
        return value
    
# NEW PASSWORD [new_password - uidb64 - token]
class NewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    uidb64 = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    model = User

    def validate_new_password(self, value):
        validate_password(value)
        return value
    
