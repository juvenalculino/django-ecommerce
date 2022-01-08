from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

# 2
class MinhaConta(BaseUserManager):
    # Criando usuário normal
    def create_user(self, nome, sobrenome, username, email, password=None):
        if not email:
            raise ValueError('Usuário não tem endereço de email')
        if not username:
            raise ValueError('Usuário não passou o username')
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            nome = nome,
            sobrenome = sobrenome,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    # Criando superusuário
    def create_superuser(self, nome, sobrenome, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            nome = nome,
            sobrenome = sobrenome,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user



# 1
class Contas(AbstractBaseUser):

    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    telefone = models.CharField(max_length=50)
    # Vamos dizer que queremos alguns filtros
    # Required
    data_entrou = models.DateTimeField(auto_now_add=True)
    ultimo_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nome', 'sobrenome']

    # 3 - Inicio
    objects = MinhaConta()
    # 3 - Fim


    def __str__(self):
        return self.email

    # Definindo os métodos
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

