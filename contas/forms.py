from django.forms import ModelForm, CharField
from django.forms.widgets import PasswordInput

from .models import Contas

class ResgitrationForm(ModelForm):
    password = CharField(widget=PasswordInput(attrs={
        'placeholder': 'Digite a Senha',
        'class': 'form-control',
    }))
    confirm_password = CharField(widget=PasswordInput(attrs={
        'placeholder': 'Confirmar Senha',
        'class': 'form-control',
    }))
    class Meta:
        model = Contas
        fields = ['nome', 'sobrenome', 'telefone', 'email', 'password']
    
    def __init__(self, *args, **kwargs):
        super(ResgitrationForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs['placeholder'] = 'Seu Nome'
        self.fields['sobrenome'].widget.attrs['placeholder'] = 'Seu Sobrenome'
        self.fields['email'].widget.attrs['placeholder'] = 'Seu Email'
        self.fields['telefone'].widget.attrs['placeholder'] = 'Seu Telefone'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


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