from django.shortcuts import render
from .forms import ResgitrationForm


# Create your views here.
def register(request):
    form = ResgitrationForm
    context = {
        'form': form,
    }
    return render(request, 'contas/register.html', context)
    

def login(request):
    return render(request, 'contas/login.html')

def logout(request):
    return render(request, 'contas/logout.html')