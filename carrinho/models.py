from django.db import models
from loja.models import Produto

# Create your models here.
class Carrinho(models.Model):
    carro_id = models.CharField(max_length=250, blank=True)
    data_add = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.carro_id

class CarrinhoItem(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    is_active = models.BooleanField(default=True)


    def sub_total(self):
        return self.produto.preco * self.quantidade


    def __str__(self):
        return self.produto
