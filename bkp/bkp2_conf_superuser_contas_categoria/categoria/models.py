from django.db import models

# Create your models here.
class Categoria(models.Model):
    categoria_nome = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    descricao = models.TextField(max_length=255, blank=True)
    cat_imagem = models.ImageField(upload_to='fotos/categoria', blank=True)


    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'


    def __str__(self):
        return self.categoria_nome