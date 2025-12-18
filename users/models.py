from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=128)

    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'users'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.username


class Role(models.Model):
    rol_id = models.AutoField(primary_key=True)
    PERMISSION_CHOICES = [
        (0, 'Sin acceso'),
        (1, 'Solo lectura'),
        (2, 'Lectura y escritura'),
    ]

    role_name = models.CharField(max_length=50, unique=True)
    customers = models.IntegerField(choices=PERMISSION_CHOICES, default=0)
    suppliers = models.IntegerField(choices=PERMISSION_CHOICES, default=0)
    materials = models.IntegerField(choices=PERMISSION_CHOICES, default=0)
    purchases = models.IntegerField(choices=PERMISSION_CHOICES, default=0)
    sales = models.IntegerField(choices=PERMISSION_CHOICES, default=0)
    inventory = models.IntegerField(choices=PERMISSION_CHOICES, default=0)
    accounting = models.IntegerField(choices=PERMISSION_CHOICES, default=0)
    reporting = models.IntegerField(choices=PERMISSION_CHOICES, default=0)

    class Meta:
        db_table = 'roles'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.role_name


class UserRole(models.Model):
    user_role_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_roles'
        verbose_name = 'Rol del Usuario'
        verbose_name_plural = 'Roles del Usuario'
        unique_together = ('user_id', 'role_id')

    def __str__(self):
        return self.user_id.username
