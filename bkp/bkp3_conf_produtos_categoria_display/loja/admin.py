from django.contrib import admin
from .models import Produto
# Register your models here.


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome_produto', 'preco', 'estoque', 'categoria', 'data_criacao', 'data_modificacao', 'e_disponivel')
    prepopulated_fields = {'slug': ('nome_produto',)}

admin.site.register(Produto, ProdutoAdmin)

"""
    nome_produto
    slug
    descricao
    preco
    imagem 
    estoque 
    e_disponivel 
    categoria
    data_criacao 
    data_modificacao
"""