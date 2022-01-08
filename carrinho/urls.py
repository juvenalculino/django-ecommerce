from django.urls import path
from . import views

urlpatterns = [
    path('', views.carrinho, name='carrinho'),
    path('add_cart/<int:produto_id>/', views.add_carrinho, name='add_cart'),
    path('remove_carrinho/<int:produto_id>/', views.remove_carrinho,  name='remove_carrinho'),
] 