from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.http import FileResponse, HttpResponse
from core.models import MedicalFile, User
from core.decorators import session_login_required  # ✅ Correct

@session_login_required
def upload_bloodtests(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # handle unauthorized access
    user = get_object_or_404(User, id=user_id)
    context = {}

    if request.method == "POST":
        if "upload" in request.POST and request.FILES.get("file"):
            file = request.FILES["file"]
            if file.content_type in ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                medical_file = MedicalFile(user=user, category="blood_test")
                medical_file.set_file(file)
                medical_file.save()
                context["success_message"] = "Blood Test file uploaded successfully."
            else:
                context["error_message"] = "Only PDF or document files are allowed."

        if "search" in request.POST:
            search_query = request.POST.get("search_query", "")
            files = MedicalFile.objects.filter(user=user, category="blood_test", file_name__icontains=search_query).order_by('-uploaded_at')
            if not files.exists():
                context["search_error"] = "No files found."
            context["search_results"] = files

    # Recent files from last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_files = MedicalFile.objects.filter(user=user, category="blood_test", uploaded_at__gte=thirty_days_ago).order_by('-uploaded_at')

    context["recent_files"] = recent_files
    return render(request, "upload_bloodtests.html", context)

@session_login_required
def bloodtest_preview(request, file_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = get_object_or_404(User, id=user_id)
    medical_file = get_object_or_404(MedicalFile, id=file_id, user=user, category="blood_test")
    file_content = medical_file.get_file()
    if file_content:
        return FileResponse(file_content, content_type='application/pdf')  # Adjust if other formats are used
    else:
        return HttpResponse("Unable to load file.", status=404)

@session_login_required
def bloodtest_download(request, file_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = get_object_or_404(User, id=user_id)
    medical_file = get_object_or_404(MedicalFile, id=file_id, user=user, category="blood_test")
    file_content = medical_file.get_file()
    if file_content:
        response = FileResponse(file_content, as_attachment=True, filename=medical_file.file_name)
        return response
    else:
        return HttpResponse("Unable to download file.", status=404)
