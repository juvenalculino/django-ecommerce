from django.shortcuts import render

# Create your views here.
def carrinho(request):
    return render(request, 'loja/carrinho.html')