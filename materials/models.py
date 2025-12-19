from django.db import models

from config.abstract import StandardModel


class Material(StandardModel):
    id_material = models.CharField(max_length=50, null=True, blank=True, verbose_name='Material ID')
    name = models.CharField(max_length=100, verbose_name='Nombre')
    description = models.TextField(max_length=250, blank=True, verbose_name='Descripción')
    unit = models.CharField(max_length=50, verbose_name='Unidad')
    material_type = models.CharField(max_length=50, verbose_name='Tipo de Material')

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiales'

    def __str__(self):
        return self.name
