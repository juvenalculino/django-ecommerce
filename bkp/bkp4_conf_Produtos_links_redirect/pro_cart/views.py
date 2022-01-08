from django.shortcuts import render
from loja.models import Produto

def home(request):
    produtos = Produto.objects.all().filter(e_disponivel=True)
    context = {
        'produtos': produtos,
    }
    return render(request, 'home.html', context)