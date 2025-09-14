import requests

API_KEY = "38284aa2-833e-11f0-a562-0200cd936042"  # 🔐 Replace with your actual key from 2factor.in

def send_otp_sms(phone_number: str, otp_code: str) -> dict:
    """
    Sends an OTP SMS using 2Factor API.

    Args:
        phone_number (str): 10-digit Indian mobile number (no +91 prefix).
        otp_code (str): The OTP to send.

    Returns:
        dict: Parsed JSON response from 2Factor API.
    """
    url = f"https://2factor.in/API/V1/{API_KEY}/SMS/{phone_number}/{otp_code}"

    try:
        response = requests.get(url)
        print(f"2Factor response: {response.status_code} - {response.text}", flush=True)
        return response.json()
    except Exception as e:
        print(f"Error sending OTP via 2Factor: {e}", flush=True)
        return {
            "status": "failed",
            "message": "Could not connect to SMS service"
        }