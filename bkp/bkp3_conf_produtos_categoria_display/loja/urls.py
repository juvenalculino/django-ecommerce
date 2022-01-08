from django.urls import path
from . import views


urlpatterns = [
    path('', views.loja, name='loja'),
    path('<slug:categoria_slug>/', views.loja, name='produtos_por_categoria'),
] 


