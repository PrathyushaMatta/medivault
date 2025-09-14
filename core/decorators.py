from functools import wraps
from django.shortcuts import redirect, get_object_or_404
from core.models import User

def session_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get("user_id")
        if not user_id:
            return redirect("login")
        try:
            user = User.objects.get(id=user_id)
            request.user = user  # Attach user object for later use
        except User.DoesNotExist:
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapper
