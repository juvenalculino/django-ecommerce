# Generated by Django 4.0.1 on 2022-01-11 14:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carrinho', '0002_carrinhoitem_variacoes'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrinhoitem',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
