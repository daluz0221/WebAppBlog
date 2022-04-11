from django.db import models
from django.contrib.auth.models import AbstractBaseUser,  PermissionsMixin


from .managers import UserManager

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    """Modelo de usuario personalizado."""

    username =  models.CharField('Nombre de usuario', max_length=50, unique=True)
    email = models.EmailField('Correo electrónico', unique=True)
    nombres = models.CharField('Nombres', max_length=50)
    apellidos = models.CharField('Apellidos', max_length=50)
    role = models.CharField('Rol', max_length=50, choices=[('admin', 'Administrador'), ('estandar', 'Estandar')])
    is_staff = models.BooleanField('¿Es miembro del staff?', default=False)
    is_active = models.BooleanField(default=False)
    coderegistro = models.CharField('Código de registro', max_length=10,blank=True, null=True)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email',]

    objects = UserManager()

    class Meta:
        """Meta definition for User."""

        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_short_name(self):
        return self.username

   

    def get_full_name(self):
        """Unicode representation of User."""
        return self.nombres + ' ' + self.apellidos

    def __str__(self):
        
        return self.username

