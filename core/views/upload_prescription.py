from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from core.models import MedicalFile
from core.models.users import User
from django.http import HttpResponse
import datetime
from core.decorators import session_login_required  # ✅ Correct

@session_login_required
def upload_prescription(request):
    user_id = request.session.get("user_id")
    if not user_id:
        messages.error(request, "Please login to continue.")
        return redirect("login")

    user = get_object_or_404(User, id=user_id)

    context = {"recent_files": [], "search_results": None, "query": ""}

    if request.method == "POST":
        uploaded_file = request.FILES.get("file")
        if uploaded_file and uploaded_file.name.endswith(".pdf"):
            medical_file = MedicalFile(user=user, category="prescription")
            medical_file.set_file(uploaded_file)
            medical_file.save()
            messages.success(request, "✅ Prescription file uploaded successfully.")
            return redirect("upload_prescription")
        else:
            messages.error(request, "❌ Please upload a valid PDF file.")

    # Recent files (last 30 days)
    thirty_days_ago = timezone.now() - datetime.timedelta(days=30)
    context["recent_files"] = MedicalFile.objects.filter(
        user=user,
        category="prescription",
        uploaded_at__gte=thirty_days_ago
    ).order_by('-uploaded_at')

    # Handle search query
    query = request.GET.get("query", "")
    context["query"] = query
    if query:
        context["search_results"] = MedicalFile.objects.filter(
            user=user,
            category="prescription",
            file_name__icontains=query
        ).order_by('-uploaded_at')

    return render(request, "upload_prescription.html", context)


def download_prescription(request, file_id):
    user_id = request.session.get("user_id")
    if not user_id:
        messages.error(request, "Please login to continue.")
        return redirect("login")

    medical_file = get_object_or_404(MedicalFile, id=file_id, user_id=user_id, category="prescription")
    file_content = medical_file.get_file()
    if file_content is None:
        messages.error(request, "Unable to retrieve file.")
        return redirect("upload_prescription")

    response = HttpResponse(file_content.read(), content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="{medical_file.file_name}"'
    return response


def preview_prescription(request, file_id):
    user_id = request.session.get("user_id")
    if not user_id:
        messages.error(request, "Please login to continue.")
        return redirect("login")

    medical_file = get_object_or_404(MedicalFile, id=file_id, user_id=user_id, category="prescription")
    file_content = medical_file.get_file()
    if file_content is None:
        messages.error(request, "Unable to retrieve file.")
        return redirect("upload_prescription")

    response = HttpResponse(file_content.read(), content_type="application/pdf")
    response['Content-Disposition'] = f'inline; filename="{medical_file.file_name}"'
    return response
