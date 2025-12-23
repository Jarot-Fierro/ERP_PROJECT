from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.views import View


class BaseDataTableView(LoginRequiredMixin, View):
    model = None  # Modelo Django
    columns = []  # Columnas DataTable
    search_fields = []  # Campos para búsqueda
    permission_module = None  # Ej: "materials"

    # Configuración de ordenamiento
    default_order_column = 'id'  # Columna por defecto
    default_order_direction = 'desc'  # Dirección por defecto

    # Mapeo de índices DataTable a campos del modelo
    # Formato: {índice_dataTable: 'nombre_campo_modelo'}
    order_columns_map = {}

    # Diccionario para mapear nombres de campo a funciones de renderizado personalizadas
    column_renderers = {}

    def has_permission(self, request, level):
        """
        level: 1 = view, 2 = edit
        """
        return request.user_permissions.get(self.permission_module, 0) >= level

    def get_queryset(self):
        return self.model.objects.all()

    def get_column_renderer(self, column_name):
        """Obtiene la función de renderizado para una columna específica"""
        return self.column_renderers.get(column_name)

    def render_column(self, obj, column):
        """Renderiza una columna con su formato personalizado si existe"""
        renderer = self.get_column_renderer(column)
        if renderer:
            return renderer(obj)

        # Intentar obtener el valor del objeto
        value = getattr(obj, column, '')

        # Si es un méthod callable, llamarlo
        if callable(value):
            value = value()

        return value

    def render_status(self, obj):
        """Renderizador para el campo status"""
        if hasattr(obj, 'status'):
            if obj.status:
                return '<span class="badge bg-success">Activo</span>'
            else:
                return '<span class="badge bg-danger">Inactivo</span>'
        return ''

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
        if hasattr(obj, "status") and self.has_permission(request, 2):
            label = "Desactivar" if obj.status else "Activar"
            btn_class = "btn-danger" if obj.status else "btn-success"
            actions.append(
                f'<button class="btn btn-sm {btn_class} toggle-status" '
                f'data-id="{obj.pk}">{label}</button>'
            )

        return " ".join(actions)

    def get_order_field(self, request):
        """Obtiene el campo de ordenamiento basado en los parámetros de la petición"""
        order_column_index = int(request.GET.get('order[0][column]', 0))
        order_direction = request.GET.get('order[0][dir]', 'asc')

        # Usar el mapeo personalizado o un mapeo por defecto
        if self.order_columns_map:
            order_field = self.order_columns_map.get(order_column_index)
        else:
            # Mapeo por defecto: asume que las columnas están en el mismo orden
            # 0=ID, 1=Acciones, luego siguen las columnas definidas en self.columns
            if order_column_index == 0:
                order_field = 'id'
            elif order_column_index == 1:
                order_field = None  # Acciones no se puede ordenar
            else:
                # Índices 2+ corresponden a self.columns
                col_index = order_column_index - 2
                if 0 <= col_index < len(self.columns):
                    order_field = self.columns[col_index]
                else:
                    order_field = None

        if order_field:
            # Aplicar dirección
            if order_direction == 'desc':
                order_field = f'-{order_field}'

        return order_field

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

        # 📊 Ordenamiento
        order_field = self.get_order_field(request)

        if order_field:
            queryset = queryset.order_by(order_field)
        else:
            # Orden por defecto
            default_order = f'-{self.default_order_column}' if self.default_order_direction == 'desc' else self.default_order_column
            queryset = queryset.order_by(default_order)

        # 📄 Paginación
        queryset = queryset[start:start + length]

        data = []
        for obj in queryset:
            row = []

            # 1️⃣ ID
            row.append(obj.pk)

            # 2️⃣ Acciones
            row.append(self.render_actions(obj, request))

            # 3️⃣ Columnas visibles con renderizado personalizado
            for col in self.columns:
                # Verificar si es el campo 'status' para renderizado especial
                if col == 'status':
                    row.append(self.render_status(obj))
                else:
                    value = self.render_column(obj, col)

                    # Formato para fechas
                    if col in ['created_at', 'updated_at'] and hasattr(value, 'strftime'):
                        value = f"{value.strftime('%d/%m/%Y %H:%M')}"
                    elif col in ['status'] and isinstance(value, bool):
                        value = "Activo" if value else "Inactivo"

                    row.append(value)

            data.append(row)

        return JsonResponse({
            "draw": draw,
            "recordsTotal": total,
            "recordsFiltered": total,
            "data": data,
        })
