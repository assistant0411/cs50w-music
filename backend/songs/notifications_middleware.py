from knox.models import AuthToken
from knox import crypto


class NotificationsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/notifications/'):
            auth_header = request.headers.get('Authorization', '')
            if auth_header.startswith('Token '):
                raw_token = auth_header.split(' ')[1]
                token_obj = AuthToken.objects.filter(digest=crypto.hash_token(raw_token)).first()
                if token_obj:
                    request.user = token_obj.user

        return self.get_response(request)
