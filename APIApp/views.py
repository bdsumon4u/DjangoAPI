from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Product
from .serializers import ProductSerializer
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from .permissions import IsOwnerOrReadOnly

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the APIApp index.")


class ProductListCreate(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProductRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
