from django.shortcuts import get_object_or_404, render
from .models import Produto
from categoria.models import Categoria
# Create your views here.

def loja(request, categoria_slug=None):
    categorias = None
    produtos = None

    if categoria_slug != None:
        categorias = get_object_or_404(Categoria, slug=categoria_slug)
        produtos = Produto.objects.filter(categoria=categorias, e_disponivel=True)
        contar_produto = produtos.count()
    else:

        produtos = Produto.objects.all().filter(e_disponivel=True)
        contar_produto = produtos.count()
    context = {
        'produtos': produtos,
        'contar_produto': contar_produto,
    }
    return render(request, 'loja/loja.html', context)


def detalhe_produto(request, categoria_slug, produto_slug):
    try:
        unico_produto = Produto.objects.get(categoria__slug=categoria_slug, slug=produto_slug)
    except Exception as e:
        raise e
    context = {
        'unico_produto': unico_produto,
    }
    return render(request, 'loja/detalhe_produto.html', context)