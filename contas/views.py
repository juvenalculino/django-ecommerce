from django.shortcuts import render, redirect
from .forms import ResgitrationForm
from .models import Contas
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

# 12/01/22 14:49 - User Activation imports
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


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
            # 12/01/22 14:21 - User Activation
            current_site = get_current_site(request)
            mail_subject = 'Please activate account'
            message = render_to_string('contas/verificacao_conta.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_tokes(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to[to_email])
            send_email.send()
            messages.success(request, 'Registro feito com sucesso!')
            return redirect('register')
    else:
        form = ResgitrationForm()
    context = {
        'form': form,
    }
    return render(request, 'contas/register.html', context)
    

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            #messages.success(request, 'Agora você está logado!')
            return redirect('home')
        else:
            messages.error(request, 'Erro ao fazer login')
            return redirect('login')
    return render(request, 'contas/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Você saiu do sistema!')
    return redirect('login')



def activate(request):
    return 