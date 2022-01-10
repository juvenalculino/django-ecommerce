from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Produto
from categoria.models import Categoria
from carrinho.models import CarrinhoItem
from carrinho.views import _carrinho_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# Create your views here.

def loja(request, categoria_slug=None):
    categorias = None
    produtos = None

    if categoria_slug != None:
        categorias = get_object_or_404(Categoria, slug=categoria_slug)
        produtos = Produto.objects.filter(categoria=categorias, e_disponivel=True)
        contar_produto = produtos.count()
        paginator = Paginator(produtos, 3)
        page = request.GET.get('page')
        page_produto = paginator.get_page(page)
        
    else:

        produtos = Produto.objects.all().filter(e_disponivel=True).order_by('id')
        #5
        paginator = Paginator(produtos, 3)
        page = request.GET.get('page')
        page_produto = paginator.get_page(page)
        contar_produto = produtos.count()
    context = {
        'produtos': page_produto,
        'contar_produto': contar_produto,
    }
    return render(request, 'loja/loja.html', context)


def detalhe_produto(request, categoria_slug, produto_slug):
    try:
        unico_produto = Produto.objects.get(categoria__slug=categoria_slug, slug=produto_slug)
        #4
        no_carro = CarrinhoItem.objects.filter(carrinho__carro_id=_carrinho_id(request), produto=unico_produto).exists()
        """return HttpResponse(no_carro)
        exit()"""
    except Exception as e:
        raise e
    context = {
        'unico_produto': unico_produto,
        'no_carro': no_carro,
    }
    return render(request, 'loja/detalhe_produto.html', context)