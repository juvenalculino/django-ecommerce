from .models import Carrinho, CarrinhoItem
from carrinho.views import _carrinho_id

def contar(request):
    contar_carrinho = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            carrinho = Carrinho.objects.filter(carro_id=_carrinho_id(request))
            carrinho_items = CarrinhoItem.objects.all().filter(carrinho=carrinho[:1])
            for carrinho_item in carrinho_items:
                contar_carrinho += carrinho_item.quantidade
        except Carrinho.DoesNotExist:
            contar_carrinho = 0
    return dict(contar_carrinho=contar_carrinho)