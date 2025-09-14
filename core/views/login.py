from django.shortcuts import render, redirect
from django.contrib import messages
from core.models import User, OTP
from core.utils import send_otp_sms, hash_aadhaar  # import hash_aadhaar directly
import random


def login(request):
    context = {}

    if request.method == "POST":
        action = request.POST.get("action")
        aadhaar = request.POST.get("aadhaar_number")
        otp_input = request.POST.get("otp")

        context.update({
            "aadhaar_number": aadhaar,
            "show_otp_field": action in ["send_otp", "verify_otp", "resend_otp"],
            "resend_otp": False,
            "otp_sent": False
        })

        if not aadhaar or not aadhaar.isdigit() or len(aadhaar) != 12:
            messages.error(request, "Please enter a valid 12-digit Aadhaar number.")
            return render(request, "login.html", context)

        aadhaar_hash = hash_aadhaar(aadhaar)  # ✅ Use hash_aadhaar function here

        try:
            user = User.objects.get(aadhaar_hash=aadhaar_hash)
        except User.DoesNotExist:
            messages.error(request, "Aadhaar not registered. Please sign up first.")
            return render(request, "login.html", context)

        if action in ["send_otp", "resend_otp"]:
            otp_code = str(random.randint(100000, 999999))
            print(f"Generated OTP: {otp_code} for {user.phone_number}", flush=True)

            OTP.objects.create(phone_number=user.phone_number, otp_code=otp_code, purpose="login",user=user)
            send_otp_sms(user.phone_number, otp_code)

            messages.success(request, "📲 OTP sent successfully.")
            context["show_otp_field"] = True
            context["otp_sent"] = True

        elif action == "verify_otp":
            if not otp_input:
                messages.error(request, "Please enter the OTP.")
                context["show_otp_field"] = True
                return render(request, "login.html", context)

            try:
                otp_obj = OTP.objects.filter(phone_number=user.phone_number, purpose="login").latest("created_at")

                if otp_obj.has_expired():
                    messages.error(request, "💥 OTP expired. Please request a new one.")
                    context["show_otp_field"] = True
                    context["resend_otp"] = True

                elif otp_obj.otp_code != otp_input:
                    messages.error(request, "❌ Invalid OTP. Please request a new one.")
                    context["show_otp_field"] = True
                    context["resend_otp"] = True

                else:
                    otp_obj.is_verified = True
                    otp_obj.save()

                    request.session['user_id'] = user.id
                    
                    
                    return redirect("home")  # Change to your home page

            except OTP.DoesNotExist:
                messages.error(request, "No OTP found. Please request again.")
                context["show_otp_field"] = True
                context["resend_otp"] = True

    return render(request, "login.html", context)
