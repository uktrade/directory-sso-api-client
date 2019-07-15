from django.utils.deprecation import MiddlewareMixin
from django.contrib import auth


class AuthenticationMiddleware(MiddlewareMixin):

    def process_request(self, request):
        user = auth.authenticate(request)
        if user:
            request.user = user
            auth.login(request, user)
        else:
            request.user = None
