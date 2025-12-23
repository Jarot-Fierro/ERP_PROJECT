from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from core.datatable import BaseDataTableView
from materials.models import Material


class MaterialListView(LoginRequiredMixin, TemplateView):
    template_name = "materials/material_list.html"


class MaterialDataTableView(BaseDataTableView):
    model = Material
    permission_module = "materials"

    # Columnas que se mostrarán en la tabla (en orden)
    columns = ["name", "status", "updated_at"]

    # Campos por los que se puede buscar
    search_fields = ["name", "updated_at"]

    # Configuración de ordenamiento
    default_order_column = 'name'
    default_order_direction = 'asc'
    order_columns_map = {
        0: 'id',  # ID
        2: 'name',  # Nombre
        3: 'status',  # Estado
        4: 'updated_at'  # Actualizado
    }
