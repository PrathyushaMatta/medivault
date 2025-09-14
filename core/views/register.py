from django.shortcuts import render, redirect
from django.contrib import messages
from core.models import User, OTP
from core.utils import send_otp_sms, encrypt_aadhaar, hash_aadhaar
import random

def register(request):
    context = {}

    if request.method == "POST":
        action = request.POST.get("action")
        name = request.POST.get("name")
        phone = request.POST.get("phone_number")
        aadhaar = request.POST.get("aadhaar_number")
        otp_input = request.POST.get("otp")

        context.update({
            "name": name,
            "phone_number": phone,
            "aadhaar_number": aadhaar,
            "show_otp_field": False,
            "resend_otp": False,
            "otp_sent": False
        })

        # Generate Aadhaar hash if aadhaar is provided
        aadhaar_hash = hash_aadhaar(aadhaar) if aadhaar else None

        # Check if Aadhaar already registered
        if aadhaar_hash and User.objects.filter(aadhaar_hash=aadhaar_hash).exists():
            messages.error(request, "Aadhaar already registered. Please login.")
            return render(request, "register.html", context)

        # ---- SEND / RESEND OTP ----
        if action in ["send_otp", "resend_otp"]:
            if not phone:
                messages.error(request, "Phone number is required.")
            else:
                otp_code = str(random.randint(100000, 999999))
                print(f"Generated OTP: {otp_code} for {phone}", flush=True)

                OTP.objects.create(phone_number=phone, otp_code=otp_code, purpose="register")
                send_otp_sms(phone, otp_code)

                messages.success(request, "📲 OTP sent successfully.")
                context["show_otp_field"] = True
                context["otp_sent"] = True

        # ---- VERIFY OTP ----
        elif action == "verify_otp":
            if not (name and phone and aadhaar and otp_input):
                messages.error(request, "All fields are required.")
                return render(request, "register.html", context)

            if not aadhaar.isdigit() or len(aadhaar) != 12:
                messages.error(request, "❌ Invalid Aadhaar number.")
                return render(request, "register.html", context)

            try:
                otp_obj = OTP.objects.filter(phone_number=phone, purpose="register").latest("created_at")

                if otp_obj.has_expired():
                    messages.error(request, "💥OTP expired. Please request a new one.")
                    context["show_otp_field"] = True
                    context["resend_otp"] = True

                elif otp_obj.otp_code != otp_input:
                    messages.error(request, "❌ Invalid OTP. Please request a new one.")
                    context["show_otp_field"] = True
                    context["resend_otp"] = True

                else:
                    # ✅ Create the user
                    user = User.objects.create(
                        name=name,
                        phone_number=phone,
                        aadhaar_encrypted=encrypt_aadhaar(aadhaar),
                        aadhaar_hash=aadhaar_hash
                    )

                    otp_obj.is_verified = True
                    otp_obj.user = user
                    otp_obj.save()

                    messages.success(request, "Registration successful 🎉.Please Login.")
                    return redirect("login")

            except OTP.DoesNotExist:
                messages.error(request, "No OTP found. Please request again.")
                context["show_otp_field"] = True
                context["resend_otp"] = True

    return render(request, "register.html", context)
