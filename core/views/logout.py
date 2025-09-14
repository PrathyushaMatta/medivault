from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def logout(request):
    # Clear the session
    request.session.flush()
    # Optionally, you can add a message here or redirect to login
    return redirect('login')
