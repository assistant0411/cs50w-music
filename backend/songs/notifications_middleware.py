"""Middleware authenticating user via knox token when calling django-notifications APIs"""

from knox import crypto
from knox.models import AuthToken


class NotificationsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/notifications/"):
            # get the token from the http header
            auth_header = request.headers.get("Authorization", "")
            if auth_header.startswith("Token "):
                raw_token = auth_header.split(" ")[1]
                
                # check if the token is valid
                token_obj = AuthToken.objects.filter(digest=crypto.hash_token(raw_token)).first()
                if token_obj:
                    request.user = token_obj.user

        return self.get_response(request)
