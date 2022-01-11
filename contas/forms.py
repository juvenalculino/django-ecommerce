from django.forms import ModelForm

from .models import Contas

class ResgitrationForm(ModelForm):
    class Meta:
        model = Contas
        fields = ['nome', 'sobrenome', 'telefone', 'email', 'password']

'''
    nome
    sobrenome
    username
    email
    telefone

    # Required
    data_entrou
    ultimo_login
    is_admin
    is_staff
    is_active
    is_superadmin
'''