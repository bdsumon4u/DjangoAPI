from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.ProductListCreate.as_view()),
    path('products/<int:pk>/', views.ProductRetrieveUpdateDestroy.as_view()),
]
