# Generated by Django 4.0.1 on 2022-01-13 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carrinho', '0005_rename_variacoes_carrinhoitem_variations'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carrinhoitem',
            old_name='variations',
            new_name='variacoes',
        ),
    ]
