# REST FRAMEWORK
from rest_framework.response import Response
from rest_framework import status

# REST FRAMEWORK VIEWS
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView

# REST FRAMEWORK - JWT
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# PERMISSIONS
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

# OUR PERMISSIONS
from account.api.permissions import IsSuperUser, IsOwnerCustomer

# MODELS
from account.models import User, CustomerUser, SellerUser, Address

# SERIALIZERS
from account.api.serializers import (
    UserSerializerWithToken,
    CustomerSerializerWithToken,
    CustomerRegisterSerializer,
    AddressSerializer
    
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
            return Response({'status': 'success', 'user': serializer.data}, status=status.HTTP_201_CREATED)
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
    
class AddressCreateUpdateDeleteAPIView(APIView):
    permission_classes = [IsOwnerCustomer]
    serializer_class = AddressSerializer

    def post(self, request):
        data = request.data

        serializer = self.serializer_class(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'address': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': 'error', 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        data = request.data

        address_id = data.get('id')
        address = Address.objects.get(id=address_id)

        serializer = self.serializer_class(address, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'address': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': 'error', 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        data = request.data
        address_id = data.get('id')

        try:
            address = Address.objects.get(id=address_id)
            address.delete()
        except Exception as e:
            print(e)
            return Response({'status':'error', 'detail': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status':'success', 'detail': 'Address deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            