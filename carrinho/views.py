from django.shortcuts import redirect, render
from loja.models import Produto
from .models import Carrinho, CarrinhoItem
# Create your views here.

#3
def _carrinho_id(request):
    carrinho = request.session.session_key
    if not carrinho:
        carrinho = request.session.create()
    return carrinho



#2
def add_carrinho(request, produto_id):
    produto = Produto.objects.get(id=produto_id) # busca o produto
    try:
        carrinho = Carrinho.objects.get(carro_id=_carrinho_id(request)) # busca o carrinho usando o carro_id presente na sessão
    except Carrinho.DoesNotExist:
        carrinho = Carrinho.objects.create(
            carro_id = _carrinho_id(request)
        )
    carrinho.save()
    try:
        carrinho_item = CarrinhoItem.objects.get(produto=produto, carrinho=carrinho)
        carrinho_item.quantidade += 1
        carrinho_item.save()
    except CarrinhoItem.DoesNotExist:
        carrinho_item = CarrinhoItem.objects.create(
            produto = produto,
            quantidadde = 1,
            carrinho = carrinho,
        )
        carrinho_item.save()
    #return HttpResponse(carrinho_item.produto)
    #exit()
    return redirect('carrinho')



#1
def carrinho(request, total=0, quantidade=0, carrinho_items=None):
    try:
        carrinho = Carrinho.objects.get(carro_id=_carrinho_id(request))
        carrinho_items = CarrinhoItem.objects.filter(carrinho=carrinho, is_active=True)
        for carrinho_item in carrinho_items:
            total += (carrinho_item.produto.preco * carrinho_item.quantidade)
            quantidade += carrinho_item.quantidade
        taxa = (2 * total) / 100
        total_geral = total + taxa
    except Exception as e:
        raise e
    context = {
        'total': total,
        'quantidade': quantidade,
        'carrinho_items': carrinho_items,
        'taxa': taxa,
        'total_geral': total_geral,
    }
    return render(request, 'loja/carrinho.html', context)