from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from core.datatable import BaseDataTableView
from materials.models import Material


class MaterialListView(LoginRequiredMixin, TemplateView):
    template_name = "materials/material_list.html"


class MaterialDataTableView(BaseDataTableView):
    model = Material
    permission_module = "materials"
    columns = ["name", "updated_at"]
    search_fields = ["name"]
