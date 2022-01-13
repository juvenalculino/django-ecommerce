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

from django.http import HttpResponse
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
            current_site = get_current_site(request=request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('contas/email_ativo.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            #messages.success(
            #    request=request,
            #    message="Please confirm your email address to complete the registration"
            #)
            return redirect('contas/login/?command=verification&email='+email)
        else:
            messages.error(request=request, message='Register failes!')
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
            messages.success(request, 'Agora você está logado!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Erro ao fazer login')
            return redirect('login')
    return render(request, 'contas/login.html')

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
def forgotpassword(request):
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



def resetpassword(request):
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
    return render(request, 'contas/resetpassword.html')