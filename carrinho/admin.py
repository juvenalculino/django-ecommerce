from django.contrib import admin
from .models import Carrinho, CarrinhoItem

# Register your models here.


class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ('carro_id', 'data_add')


class CarrinhoItemAdmin(admin.ModelAdmin):
    list_display = ('produto', 'carrinho', 'quantidade', 'is_active')


admin.site.register(Carrinho, CarrinhoAdmin)
admin.site.register(CarrinhoItem, CarrinhoItemAdmin)
