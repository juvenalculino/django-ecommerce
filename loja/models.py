from django.db import models
from categoria.models import Categoria
from django.urls import reverse

# Create your models here.
class Produto(models.Model):
    nome_produto = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    descricao = models.TextField(max_length=500, blank=True)
    preco = models.IntegerField()
    imagem = models.ImageField(upload_to='fotos/produtos')
    estoque = models.IntegerField()
    e_disponivel = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_modificacao = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('detalhe_produto', args=[self.categoria.slug, self.slug])

    def __str__(self):
        return self.nome_produto




class VariationGerenciador(models.Manager):
    def colors(self):
        return super(VariationGerenciador, self).filter(variacao_categoria='color', is_active=True)

    def sizes(self):
        return super(VariationGerenciador, self).filter(variacao_categoria='size', is_active=True)


variacao_categoria_choice = (
    ('color', 'color'),
    ('size', 'size'),
)

class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    variacao_categoria = models.CharField(max_length=100, choices=variacao_categoria_choice)
    variacao_valor = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    objects = VariationGerenciador()

    def __str__(self):
        return self.variacao_valor
