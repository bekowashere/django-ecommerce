# REST FRAMEWORK
from rest_framework.response import Response
from rest_framework import status

# PERMISSIONS
from store.api.permissions import IsOwnerSeller

# REST FRAMEWORK VIEWS
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView

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

from store.api.serializers import (
    ProductCreateUpdateSerializer,
    ProductInventoryCreateUpdateSerializer 
)

# PRODUCT
class ProductCreateUpdateAPIView(APIView):
    permission_classes = [IsOwnerSeller]
    serializer_class = ProductCreateUpdateSerializer

    def post(self, request):
        data = request.data

        serializer = self.serializer_class(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            response = {
                'status': 'success',
                'code': status.HTTP_201_CREATED,
                'message': 'Product has been successfully created',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response({'status': 'error', 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# PRODUCT INVENTORY
class ProductInventoryCreateUpdateAPIView(APIView):
    permission_classes = [IsOwnerSeller]
    serializer_class = ProductInventoryCreateUpdateSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            response = {
                'status': 'success',
                'code': status.HTTP_201_CREATED,
                'message': 'ProductInventory has been successfully created',
                'data': serializer.data
            }

            return Response(response, status=status.HTTP_201_CREATED)
        return Response({'status': 'error', 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)