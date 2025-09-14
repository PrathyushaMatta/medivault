from django.shortcuts import render, redirect
from django.contrib import messages
from core.models import User

def home(request):
    user_id = request.session.get("user_id")

    if not user_id:
        messages.error(request, "Please login first.")
        return redirect("login")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "User not found. Please login again.")
        return redirect("login")

    return render(request, "home.html", {"user": user})
