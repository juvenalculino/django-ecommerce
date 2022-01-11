from django.contrib import admin
from .models import Produto, Variacao
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
class VariacaoAdmin(admin.ModelAdmin):
    list_display = ('produto', 'variacao_categoria', 'variacao_valor', 'is_active', 'data_criacao')
    list_editable = ('is_active',)   # Cho phép chỉnh sửa trên list hiển thị
    list_filter = ('produto', 'variacao_categoria', 'variacao_valor')

admin.site.register(Variacao, VariacaoAdmin)


'''
    produto
    variacao_categoria
    variacao_valor
    is_active
    data_criacao
'''