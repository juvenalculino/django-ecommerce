from django.db.models.query import Prefetch
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