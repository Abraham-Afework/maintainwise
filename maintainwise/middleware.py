from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
import re

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.login_url = reverse('login')
        self.exempt_urls = [
            re.compile('^' + reverse('login').lstrip('/')),
            re.compile('^' + reverse('register').lstrip('/')),
            re.compile('^' + settings.STATIC_URL.lstrip('/')),
            re.compile('^' + settings.MEDIA_URL.lstrip('/')),
        ]

    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path_info.lstrip('/')
            if not any(url.match(path) for url in self.exempt_urls):
                print(f'Redirecting to login: {path}')
                return redirect(self.login_url)
        response = self.get_response(request)
        return response
