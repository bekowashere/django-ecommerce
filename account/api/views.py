# REST FRAMEWORK
from rest_framework.response import Response
from rest_framework import status

# REST FRAMEWORK VIEWS
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView

# REST FRAMEWORK - JWT
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# PERMISSIONS
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

# OUR PERMISSIONS
from account.api.permissions import IsSuperUser, IsOwnerCustomer, IsOwnerSeller

# MODELS
from account.models import User, CustomerUser, SellerUser, Address, SellerUserImage

# PASSWORD - EMAIL
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status

# SERIALIZERS
from account.api.serializers import (
    UserSerializerWithToken,
    
    # CUSTOMER
    CustomerSerializerWithToken,
    CustomerRegisterSerializer,
    CustomerProfileSerializer,
    DefaultAddressSerializer,
    AddressSerializer,
    
    # SELLER
    SellerSerializerWithToken,
    SellerRegisterSerializer,
    SellerCreateMultipleImageSerializer,
    SellerCompanyImageSerializer,
    SellerProfileSerializer,
    SellerSlugSerializer,
    SellerCodeSerializer,
    SellerContactSerializer,
    SellerLocationSerializer,
    SellerUserImageSerializer,

    # PASSWORD
    ChangePasswordSerializer
)

class MyTokenObtainPairSerializer(TokenObtainSerializer):
    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# CUSTOMER LOGIN
class CustomerMyTokenObtainPairSerializer(TokenObtainSerializer):
    def validate(self, attrs):
        data = super(CustomerMyTokenObtainPairSerializer, self).validate(attrs)
        customer = CustomerUser.objects.get(user=self.user)

        serializer = CustomerSerializerWithToken(customer).data
        for k, v in serializer.items():
            data[k] = v
        return data
    
class CustomerMyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomerMyTokenObtainPairSerializer

# CUSTOMER REGISTER
class CustomerRegisterAPIView(APIView):
    serializer_class = CustomerRegisterSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            response = {
                'status': 'success',
                'code': status.HTTP_201_CREATED,
                'message': 'Your account has been successfully created',
                'data': serializer.data
            }

            return Response(response, status=status.HTTP_201_CREATED)
        return Response({'status': 'error', 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# CUSTOMER PROFILE
class CustomerProfileUpdateAPIView(APIView):
    permission_classes = [IsOwnerCustomer]
    serializer_class = CustomerProfileSerializer

    def put(self, request):
        data = request.data
        user = request.user

        customer = CustomerUser.objects.get(user=user)

        serializer = self.serializer_class(customer, data=data)
        if serializer.is_valid():
            serializer.save()

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Your profile information has been successfully updated',
                'data': serializer.data
            }
            
            return Response(response, status=status.HTTP_200_OK)
        return Response({'status': 'error', 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# SELLER LOGIN
class SellerMyTokenObtainPairSerializer(TokenObtainSerializer):
    def validate(self, attrs):
        data = super(SellerMyTokenObtainPairSerializer, self).validate(attrs)
        customer = SellerUser.objects.get(user=self.user)

        serializer = SellerSerializerWithToken(customer).data
        for k, v in serializer.items():
            data[k] = v
        return data
    
class SellerMyTokenObtainPairView(TokenObtainPairView):
    serializer_class = SellerMyTokenObtainPairSerializer
    
# SELLER REGISTER
class SellerRegisterAPIView(APIView):
    serializer_class = SellerRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            response = {
                'status': 'success',
                'code': status.HTTP_201_CREATED,
                'message': 'Your account has been successfully created',
                'data': serializer.data
            }

            return Response(response, status=status.HTTP_201_CREATED)
        return Response({'status': 'error', 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# SELLER MULTIPLE IMAGES
class SellerMultipleImagesCreateAPIView(APIView):
    permission_classes = [IsOwnerSeller]
    serializer_class = SellerCreateMultipleImageSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            response = {
                'status': 'success',
                'code': status.HTTP_201_CREATED,
                'message': 'Your images has been successfully created',
                'data': serializer.data
            }

            return Response(response, status=status.HTTP_201_CREATED)
        return Response({'status': 'error', 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        data = request.data
        
        try:
            for image_id in data.values():
                img_obj = SellerUserImage.objects.get(image_id=image_id)
                img_obj.delete()

                response = {
                'status': 'success',
                'code': status.HTTP_204_NO_CONTENT,
                'message': 'Your images removes successfully',
                'data': []
                }
                
                return Response(response, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            return Response({'status': 'error', 'detail': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
        
# V2
class SellerMultipleImagesCreateAPIViewV2(APIView):
    permission_classes = [IsOwnerSeller]
    serializer_class = SellerUserImageSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'images': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': 'error', 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

#  SELLER COMPANY IMAGE
class SellerCompanyImageUpdateAPIView(APIView):
    permission_classes = [IsOwnerSeller]
    serializer_class = SellerCompanyImageSerializer

    def put(self, request):
        data = request.data
        user = request.user

        seller = SellerUser.objects.get(user=user)
        # photo = self.get_object(pk)

        serializer = self.serializer_class(seller, data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Your company image has been successfully updated',
                'data': serializer.data
            }

            return Response(response, status=status.HTTP_200_OK)
        return Response({'status': 'error', 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# SELLER PROFILE
class SellerProfileUpdateAPIView(APIView):
    permission_classes = [IsOwnerSeller]
    serializer_class = SellerProfileSerializer

    def put(self, request):
        data = request.data
        user = request.user

        seller = SellerUser.objects.get(user=user)

        serializer = self.serializer_class(seller, data=data)
        if serializer.is_valid():
            serializer.save()

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Your profile information has been successfully updated',
                'data': serializer.data
            }

            return Response(response, status=status.HTTP_200_OK)
        return Response({'status': 'error', 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
# SELLER SLUG
class SellerSlugUpdateAPIView(APIView):
    permission_classes = [IsOwnerSeller]
    serializer_class = SellerSlugSerializer

    def put(self, request):
        data = request.data
        user = request.user

        seller = SellerUser.objects.get(user=user)

        serializer = self.serializer_class(seller, data=data)
        if serializer.is_valid():
            serializer.save()

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Your slug has been successfully updated',
                'data': serializer.data
            }

            return Response(response, status=status.HTTP_200_OK)
        return Response({'status': 'error', 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
# SELLER CODE
class SellerCodeUpdateAPIView(APIView):
    permission_classes = [IsOwnerSeller]
    serializer_class = SellerCodeSerializer

    def put(self, request):
        data = request.data
        user = request.user

        seller = SellerUser.objects.get(user=user)

        serializer = self.serializer_class(seller, data=data)
        if serializer.is_valid():
            serializer.save()

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Your company code has been successfully updated',
                'data': serializer.data
            }

            return Response(response, status=status.HTTP_200_OK)
        return Response({'status': 'error', 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# SELLER CONTACT
class SellerContactUpdateAPIView(APIView):
    permission_classes = [IsOwnerSeller]
    serializer_class = SellerContactSerializer

    def put(self, request):
        data = request.data
        user = request.user

        seller = SellerUser.objects.get(user=user)

        serializer = self.serializer_class(seller, data=data)
        if serializer.is_valid():
            serializer.save()

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Your contact informations has been successfully updated',
                'data': serializer.data
            }

            return Response(response, status=status.HTTP_200_OK)
        return Response({'status': 'error', 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
# SELLER LOCATION
class SellerLocationUpdateAPIView(APIView):
    permission_classes = [IsOwnerSeller]
    serializer_class = SellerLocationSerializer

    def put(self, request):
        data = request.data
        user = request.user

        seller = SellerUser.objects.get(user=user)

        serializer = self.serializer_class(seller, data=data)
        if serializer.is_valid():
            serializer.save()

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Your location informations has been successfully updated',
                'data': serializer.data
            }

            return Response(response, status=status.HTTP_200_OK)
        return Response({'status': 'error', 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
# ADDRESS
class ListAddressAPIView(ListAPIView):
    permission_classes = [IsOwnerCustomer]
    serializer_class = AddressSerializer

    def get_queryset(self):
        user = self.request.user
        customer = CustomerUser.objects.get(user=user)
        queryset = Address.objects.filter(user=customer)
        return queryset

class DefaultAddressUpdateAPIView(APIView):
    permission_classes = [IsOwnerCustomer]
    serializer_class = DefaultAddressSerializer

    def put(self, request):
        data = request.data
        user = request.user

        customer = CustomerUser.objects.get(user=user)

        serializer = self.serializer_class(customer, data=data)
        if serializer.is_valid():
            serializer.save()

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Your default address has been successfully updated',
                'data': serializer.data
            }

            return Response(response, status=status.HTTP_200_OK)
        return Response({'status': 'error', 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class AddressCreateUpdateDeleteAPIView(APIView):
    permission_classes = [IsOwnerCustomer]
    serializer_class = AddressSerializer

    def post(self, request):
        data = request.data

        serializer = self.serializer_class(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            response = {
                'status': 'success',
                'code': status.HTTP_201_CREATED,
                'message': 'Your new address has been successfully created',
                'data': serializer.data
            }

            return Response(response, status=status.HTTP_201_CREATED)
        return Response({'status': 'error', 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        data = request.data

        address_id = data.get('id')
        address = Address.objects.get(id=address_id)

        serializer = self.serializer_class(address, data=data)
        if serializer.is_valid():
            serializer.save()

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Your address has been successfully updated',
                'data': serializer.data
            }

            return Response({'status': 'success', 'address': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': 'error', 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        data = request.data
        address_id = data.get('id')

        try:
            address = Address.objects.get(id=address_id)
            address.delete()

            response = {
                'status': 'success',
                'code': status.HTTP_204_NO_CONTENT,
                'message': 'Your address deleted successfully',
                'data': []
                }

            return Response(response, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            return Response({'status':'error', 'detail': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)


##########################################################
class ChangePasswordView(UpdateAPIView):
    """
    A endpoint for changing password
    """
    # queryset = User.object.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    model = User

    def get_object(self):
        obj = self.request.user
        return obj
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        # serializer = self.get_serializer(data=request.data)
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            # Check old_password
            # self.object -> user
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({"old_password": "Old password is not correct"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check new passwords match
            new_password = serializer.data.get('new_password')
            new_password_confirm = serializer.data.get('new_password_confirm')
            if new_password != new_password_confirm:
                return Response({"new_password": "Password fields didn't match."}, status=status.HTTP_400_BAD_REQUEST)
                
            # set_password
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully'
            }

            # serializer.save()

            return Response(response, status=status.HTTP_200_OK)
        return Response({'status': 'error', 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)