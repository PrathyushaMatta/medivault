from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from core.models.users import User
import hashlib

@csrf_exempt  # Disable CSRF for testing only
def test_login(request):
    if request.method == "POST":
        aadhaar_number = request.POST.get("aadhaar_number")
        otp = request.POST.get("otp")

        # Simple logic to accept predefined Aadhaar + OTP for testing
        if aadhaar_number == "844033362513" and otp == "123456":
            aadhaar_hash = hashlib.sha256(aadhaar_number.encode()).hexdigest()
            try:
                user = User.objects.get(aadhaar_hash=aadhaar_hash)
                request.session['user_id'] = user.id  # Manually set session
                return JsonResponse({"message": "Logged in successfully"})
            except User.DoesNotExist:
                return JsonResponse({"error": "User not found"}, status=404)
        else:
            return JsonResponse({"error": "Invalid Aadhaar or OTP"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
