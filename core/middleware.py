from users.models import UserRole


class UserPermissionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        permissions = {}

        if request.user.is_authenticated:
            roles = UserRole.objects.filter(user_id=request.user)

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

            for user_role in roles:
                role = user_role.role_id
                for module in permissions.keys():
                    value = getattr(role, module, 0)
                    if value > permissions[module]:
                        permissions[module] = value

        request.user_permissions = permissions
        return self.get_response(request)
