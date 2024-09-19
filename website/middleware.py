# middleware.py

from django.utils import timezone
from django.conf import settings
from django.shortcuts import redirect
from datetime import timedelta

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            if last_activity:
                # Convert timestamp from session to datetime
                last_activity = timezone.datetime.fromisoformat(last_activity)
                now = timezone.now()
                if now - last_activity > timedelta(seconds=settings.SESSION_COOKIE_AGE):
                    # Session has expired
                    request.session.flush()  # Clear the session
                    return redirect('login')

            # Update last activity timestamp
            request.session['last_activity'] = timezone.now().isoformat()

        response = self.get_response(request)
        return response
