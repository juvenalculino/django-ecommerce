from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from loja.models import Produto, Variacao
from .models import Carrinho, CarrinhoItem
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

#3
def _carrinho_id(request):
    carrinho_id = request.session.session_key
    if not carrinho_id:
        carrinho_id = request.session.create()
    return carrinho_id



#2
def add_carrinho(request, produto_id):
    #4
    usuario_atual = request.user
    produto = Produto.objects.get(id=produto_id) # busca o produto
    if usuario_atual.is_authenticated:
        variacao_produto = list()
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST.get(key)
                try:
                    variacao = Variacao.objects.get(produto=produto, variacao_categoria__iexact=key, variacao_valor__iexact=value)
                    variacao_produto.append(variacao)
                except ObjectDoesNotExist:
                    pass
        """try:
            carrinho = Carrinho.objects.get(carro_id=_carrinho_id(request)) # busca o carrinho usando o carro_id presente na sessão
        except Carrinho.DoesNotExist:
            carrinho = Carrinho.objects.create(
                carro_id = _carrinho_id(request)
            )
        carrinho.save()"""
        #7
        se_carrinho_item_existe = CarrinhoItem.objects.filter(produto=produto, user=usuario_atual).exists()
        if se_carrinho_item_existe:
            carrinho_item = CarrinhoItem.objects.filter(produto=produto, user=usuario_atual)
        #8 existing_variations -> database
        # current variation -> product_variation
        # Item_id -> database
            existe_lista_variacoes = [list(item.variacoes.all()) for item in carrinho_item]
            id = [item.id for item in carrinho_item]
            if variacao_produto in existe_lista_variacoes:
                idex = existe_lista_variacoes.index(variacao_produto)
                carrinho_item = CarrinhoItem.objects.get(id=id[idex])
                carrinho_item.quantidade += 1
        #10
            else:
                carrinho_item = CarrinhoItem.objects.create(produto=produto, user=usuario_atual, quantidade=1)           


        else:
            # Create new cart item
            #12
            carrinho_item = CarrinhoItem.objects.create(produto=produto, user=usuario_atual, quantidade=1)

        #5
        if len(variacao_produto) > 0:
            carrinho_item.variacoes.clear()
            for item in variacao_produto:
                carrinho_item.variacoes.add(item)
        carrinho_item.save()
        return redirect('carrinho')
    else:
        variacao_produto = list()
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST.get(key)
                try:
                    variacao = Variacao.objects.get(produto=produto, variacao_categoria__iexact=key, variacao_valor__iexact=value)
                    variacao_produto.append(variacao)
                except ObjectDoesNotExist:
                    pass
        try:
                
            carrinho = Carrinho.objects.get(carro_id=_carrinho_id(request=request))
        except Carrinho.DoesNotExist:
            carrinho = Carrinho.objects.create(carro_id=_carrinho_id(request))
        carrinho.save()

        se_carrinho_item_existe = CarrinhoItem.objects.filter(produto=produto, carrinho=carrinho).exists()
        if se_carrinho_item_existe:
            carrinho_item = CarrinhoItem.objects.filter(produto=produto, carrinho=carrinho)
            existe_lista_variacoes = [list(item.variacoes.all()) for item in carrinho_item]
            id = [item.id for item in carrinho_item]
            if variacao_produto in existe_lista_variacoes:
                idex = existe_lista_variacoes.index(variacao_produto)
                carrinho_item = CarrinhoItem.objects.get(id=id[idex])
                carrinho_item.quantidade += 1
        #10
            else:
                carrinho_item = CarrinhoItem.objects.create(produto=produto, carrinho=carrinho, quantidade=1)           
        else:
            # Create new cart item
            #12
            carrinho_item = CarrinhoItem.objects.create(produto=produto, carrinho=carrinho, quantidade=1)

        #5
        if len(variacao_produto) > 0:
            carrinho_item.variacoes.clear()
            for item in variacao_produto:
                carrinho_item.variacoes.add(item)
        carrinho_item.save()
        return redirect('carrinho')



#2
def remove_carrinho(request, produto_id, carrinho_item_id):
    produto = get_object_or_404(Produto, id=produto_id)
    try:
        if request.user.is_authenticated:
            carrinho_item = CarrinhoItem.objects.get(id=carrinho_item_id, produto=produto, user=request.user)
        else:
            carrinho = Carrinho.objects.get(carro_id=_carrinho_id(request))
            carrinho_item = CarrinhoItem.objects.get(id=carrinho_item_id, produto=produto, carrinho=carrinho)
        if carrinho_item.quantidade > 1:
            carrinho_item.quantidade -= 1
            carrinho_item.save()
        else:
            carrinho_item.delete()
    except Exception:
        pass
    return redirect('carrinho')

#3 
def remove_carrinho_item(request, produto_id, carrinho_item_id):
    produto = get_object_or_404(Produto, id=produto_id)
    try:
        if request.user.is_authenticated:
            carrinho_item = CarrinhoItem.objects.get(id=carrinho_item_id, produto=produto, user=request.user)
        else:
            carrinho = Carrinho.objects.get(carro_id=_carrinho_id(request))
            carrinho_item = CarrinhoItem.objects.get(id=carrinho_item_id, produto=produto, carrinho=carrinho)
        carrinho_item.delete()
    except Exception:
        pass
    return redirect('carrinho')



#1
def carrinho(request, total=0, quantidade=0, carrinho_items=None):
    try:
        if request.user.is_authenticated:
            carrinho_items = CarrinhoItem.objects.filter(user=request.user, is_active=True)
        else:
            carrinho = Carrinho.objects.get(carro_id=_carrinho_id(request=request))
            carrinho_items = CarrinhoItem.objects.filter(carrinho=carrinho, is_active=True)

        
        for carrinho_item in carrinho_items:
            total += (carrinho_item.produto.preco * carrinho_item.quantidade)
            quantidade += carrinho_item.quantidade
        taxa = (total * 2) / 100
        total_geral = total + taxa
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantidade': quantidade,
        'carrinho_items': carrinho_items,
        'taxa': taxa if 'taxa' in locals() else "",
        'total_geral': total_geral if 'taxa' in locals() else 0,
    }
    return render(request, 'loja/carrinho.html', context)