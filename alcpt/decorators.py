from django.contrib.auth.decorators import login_required

from django.core.exceptions import PermissionDenied


def permission_check(required_privilege):
    def decorator(view):
        @login_required
        def check(request, *args, **kwargs):
            if not required_privilege:
                raise ValueError("Loss argument 'required_privilege'")

            if not request.user.has_permission(required_privilege):
                raise PermissionDenied

            return view(request, *args, **kwargs)
        return check
    return decorator
