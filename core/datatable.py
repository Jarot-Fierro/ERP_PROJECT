from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.views import View


class BaseDataTableView(LoginRequiredMixin, View):
    model = None  # Modelo Django
    columns = []  # Columnas DataTable
    search_fields = []  # Campos para búsqueda
    permission_module = None  # Ej: "customers"

    def has_permission(self, request, level):
        """
        level: 1 = view, 2 = edit
        """
        return request.user_permissions.get(self.permission_module, 0) >= level

    def get_queryset(self):
        return self.model.objects.all()

    def render_actions(self, obj, request):
        actions = []

        # Ver (permiso lectura)
        if self.has_permission(request, 1):
            actions.append(
                f'<a href="{obj.pk}/view/" class="btn btn-sm btn-primary">Ver</a>'
            )

        # Editar (permiso escritura)
        if self.has_permission(request, 2):
            actions.append(
                f'<a href="{obj.pk}/edit/" class="btn btn-sm btn-warning">Editar</a>'
            )

        # Cambiar estado
        if hasattr(obj, "is_active") and self.has_permission(request, 2):
            label = "Desactivar" if obj.is_active else "Activar"
            actions.append(
                f'<button class="btn btn-sm btn-secondary toggle-status" '
                f'data-id="{obj.pk}">{label}</button>'
            )

        return " ".join(actions)

    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", "")

        queryset = self.get_queryset()

        # 🔎 Búsqueda
        if search_value:
            q = Q()
            for field in self.search_fields:
                q |= Q(**{f"{field}__icontains": search_value})
            queryset = queryset.filter(q)

        total = queryset.count()

        # 📄 Paginación
        queryset = queryset[start:start + length]

        data = []
        for obj in queryset:
            row = []

            # 1️⃣ ID
            row.append(obj.pk)

            # 2️⃣ Acciones
            row.append(self.render_actions(obj, request))

            # 3️⃣ Columnas visibles
            for col in self.columns:
                value = getattr(obj, col)
                if col == "updated_at":
                    value = f"-{value.strftime('%d/%m/%Y %H:%M')}"
                row.append(value)

            data.append(row)

        return JsonResponse({
            "draw": draw,
            "recordsTotal": total,
            "recordsFiltered": total,
            "data": data,
        })
