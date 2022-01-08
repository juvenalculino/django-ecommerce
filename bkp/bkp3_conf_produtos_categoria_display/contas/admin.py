from django.contrib import admin
from .models import Contas
from django.contrib.auth.admin import UserAdmin
# Register your models her


class ContasAdmin(UserAdmin):   
    list_display = ('email', 'nome', 'sobrenome', 'username', 'ultimo_login', 'data_entrou', 'is_active')
    list_display_links = ('email', 'nome', 'sobrenome')
    readonly_fields = ('data_entrou', 'ultimo_login')
    ordering = ('-data_entrou',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Contas, ContasAdmin)