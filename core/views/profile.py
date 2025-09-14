from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import User, MedicalFile
from django.contrib import messages
from core.decorators import session_login_required  # ✅ Correct

@session_login_required
def profile(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "upload_image":
            profile_picture = request.FILES.get("profile_picture")
            if profile_picture:
                user.profile_picture = profile_picture
                user.save()
                messages.success(request, "Profile picture updated successfully.")
            else:
                messages.error(request, "No image selected.")

        elif action == "update_bio":
            name = request.POST.get("name", "").strip()
            phone_number = request.POST.get("phone_number", "").strip()
            address = request.POST.get("address", "").strip()

            if not name:
                messages.error(request, "Name is required.")
            else:
                user.name = name
                user.phone_number = phone_number
                user.address = address
                user.save()
                messages.success(request, "Bio updated successfully.")

    prescription_count = MedicalFile.objects.filter(user=user, category="prescription").count()
    xray_count = MedicalFile.objects.filter(user=user, category="xray").count()
    bloodtest_count = MedicalFile.objects.filter(user=user, category="blood_test").count()

    context = {
        "user": user,
        "prescription_count": prescription_count,
        "xray_count": xray_count,
        "bloodtest_count": bloodtest_count,
    }
    return render(request, "profile.html", context)