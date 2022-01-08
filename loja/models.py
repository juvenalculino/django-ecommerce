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
