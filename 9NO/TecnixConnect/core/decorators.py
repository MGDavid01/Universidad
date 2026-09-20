from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def role_required(*roles):
    """Restringe una vista a uno o más roles de usuario."""

    def decorator(view_func):
        @login_required
        def _wrapped(request, *args, **kwargs):
            if request.user.role not in roles:
                return redirect("dashboard")
            return view_func(request, *args, **kwargs)

        return _wrapped

    return decorator
