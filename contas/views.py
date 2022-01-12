from django.shortcuts import render, redirect
from .forms import ResgitrationForm
from .models import Contas
from django.contrib import messages


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = ResgitrationForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            sobrenome = form.cleaned_data['sobrenome']
            email = form.cleaned_data['email']
            telefone = form.cleaned_data['telefone']
            username = email.split('@')[0]
            password = form.cleaned_data['password']
            # Vamos pasar aqui os dados que tem na nossa função do smodels def create_user(self, nome, sobrenome, username, email, password=None):
            user = Contas.objects.create_user(nome=nome, sobrenome=sobrenome, email=email, username=username, password=password)
            user.telefone = telefone
            user.save()
            messages.success(request, 'Registro feito com sucesso!')
            return redirect('register')
    else:
        form = ResgitrationForm()
    context = {
        'form': form,
    }
    return render(request, 'contas/register.html', context)
    

def login(request):
    return render(request, 'contas/login.html')

def logout(request):
    return render(request, 'contas/logout.html')