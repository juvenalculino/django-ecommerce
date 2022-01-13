from re import split
from carrinho.models import Carrinho, CarrinhoItem
from django.shortcuts import render, redirect
from django.contrib import messages, auth
# 12/01/22 14:49 - User Activation imports
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator

from .forms import ResgitrationForm
from .models import Contas

from carrinho.views import _carrinho_id

import requests


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = ResgitrationForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            sobrenome = form.cleaned_data['sobrenome']
            email = form.cleaned_data['email']
            telefone = form.cleaned_data['telefone']
            password = form.cleaned_data['password']
            username = email.split('@')[0]

            # Vamos pasar aqui os dados que tem na nossa função do smodels def create_user(self, nome, sobrenome, username, email, password=None):
            user = Contas.objects.create_user(nome=nome, sobrenome=sobrenome, email=email, username=username, password=password)
            user.telefone = telefone
            user.save()
            
            # 12/01/22 14:21 - User Activation
            current_site = get_current_site(request=request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('contas/active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(
                request=request,
                message="Please confirm your email address to complete the registration"
            )
            return redirect('register')
        else:
            messages.error(request=request, message='Register failed!')
    else:
        form = ResgitrationForm()
    context = {
        'form': form,
    }
    return render(request, 'contas/register.html', context)
    

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                carrinho = Carrinho.objects.get(cart_id=_carrinho_id(request))
                carrinho_items = CarrinhoItem.objects.filter(carrinho=carrinho)
                if carrinho_items.exists():
                    variacao_produto = []
                    for carrihno_item in carrinho_items:
                        variacoes = carrihno_item.variacoes.all()
                        variacao_produto.append(list(variacoes))
                        # cart_item.user = user
                        # cart_item.save()
                    carrinho_items = CarrinhoItem.objects.filter(user=user)
                    existe_lista_variacoes = [list(item.variacoes.all()) for item in carrinho_items]
                    id = [item.id for item in carrinho_items]

                    for product in variacao_produto:
                        if product in existe_lista_variacoes:
                            index = existe_lista_variacoes.index(product)
                            item_id = id[index]
                            item = CarrinhoItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_items = CarrinhoItem.objects.filter(cart=cart)
                            for item in cart_items:
                                item.user = user
                                item.save()
            except Exception:
                pass
            auth.login(request=request, user=user)
            messages.success(request=request, message="Login successful!")

            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split("=") for x in query.split("&"))
                if "next" in params:
                    next_page = params["next"]
                    return redirect(next_page)
            except Exception:
                return redirect('dashboard')
        else:
            messages.error(request=request, message="Login failed!")
    context = {
        'email': email if 'email' in locals() else '',
        'password': password if 'password' in locals() else '',
    }
    return render(request, 'contas/login.html', context=context)



@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.info(request, 'Você saiu do sistema!')
    return redirect('login')



def activate(request, uidb64, token):#uidb64, token
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Contas.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request=request, message="Your account is activated, please login!")
        return render(request, 'contas/login.html')
    else:
        messages.error(request=request, message="Activation link is invalid!")
        return redirect('home')


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'contas/dashboard.html')



# 13/01/22 09:20
def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        # Verificando se email existe
        if Contas.objects.filter(email=email).exists():
            # Verificando se o email é exato
            user = Contas.objects.get(email__iexact=email)

            # 13/01/22 09:27 - Reset password email
            current_site = get_current_site(request=request)
            mail_subject = 'Reset Your Password!.'
            message = render_to_string('contas/reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Email enviado para sua conta. Verifique o link de alteração de senha!')
            return redirect('login')

        else:
            messages.error(request, 'Conta não existe!')
            return redirect('forgotpassword')
    return render(request, 'contas/forgotpassword.html')



# 13/01/22 09:20 - Função para validar o envio de email
def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Contas.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request=request, message='Please reset your password')
        return redirect('login')
    else:
        messages.error(request=request, message="This link has been expired!")
        return redirect('home')



def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Contas.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, message="Password reset successful!")
            return redirect('login')
        else:
            messages.error(request, message="Password do not match!")
    return render(request, 'contas/reset_password.html')