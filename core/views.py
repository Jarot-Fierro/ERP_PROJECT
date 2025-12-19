from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy

from users.models import UserRole


@login_required
def dashboard_view(request):
    user_roles = UserRole.objects.filter(user_id=request.user)

    permissions = {
        'customers': 0,
        'suppliers': 0,
        'materials': 0,
        'purchases': 0,
        'sales': 0,
        'inventory': 0,
        'accounting': 0,
        'reporting': 0,
    }

    for user_role in user_roles:
        role = user_role.role_id
        for module in permissions.keys():
            current_permission = getattr(role, module)
            if current_permission > permissions[module]:
                permissions[module] = current_permission

    # Configuración visual del dashboard
    MODULES = {
        "customers": {
            "label": "Clientes",
            "color": "#2563EB",  # Azul corporativo
            "icon": "users",
            "url": "#",
        },
        "suppliers": {
            "label": "Proveedores",
            "color": "#0F766E",  # Verde petróleo
            "icon": "truck",
            "url": "#",
        },
        "materials": {
            "label": "Materiales",
            "color": "#64748B",  # Gris acero
            "icon": "cube",
            "url": reverse_lazy("materials_list"),
        },
        "purchases": {
            "label": "Compras",
            "color": "#D97706",  # Ámbar oscuro
            "icon": "cart",
            "url": "#",
        },
        "sales": {
            "label": "Ventas",
            "color": "#4F46E5",  # Índigo profesional
            "icon": "currency",
            "url": "#",
        },
        "inventory": {
            "label": "Inventario",
            "color": "#059669",  # Verde control
            "icon": "archive",
            "url": "#",
        },
        "accounting": {
            "label": "Contabilidad",
            "color": "#334155",  # Gris pizarra
            "icon": "calculator",
            "url": "#",
        },
        "reporting": {
            "label": "Reportes",
            "color": "#B91C1C",  # Rojo sobrio
            "icon": "chart",
            "url": "#",
        },
    }

    # Solo módulos con acceso
    dashboard_modules = []
    for key, level in permissions.items():
        if level > 0:
            module = MODULES[key].copy()
            module["permission"] = level
            dashboard_modules.append(module)

    context = {
        "dashboard_modules": dashboard_modules,
    }

    return render(request, "core/dashboard.html", context)
