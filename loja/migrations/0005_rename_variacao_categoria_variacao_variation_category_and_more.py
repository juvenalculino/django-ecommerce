# Generated by Django 4.0.1 on 2022-01-13 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0004_variacao_delete_variation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variacao',
            old_name='variacao_categoria',
            new_name='variation_category',
        ),
        migrations.RenameField(
            model_name='variacao',
            old_name='variacao_valor',
            new_name='variation_value',
        ),
    ]
