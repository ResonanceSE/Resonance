from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from ..models.auth_model import Token

class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        
        try:
            token_obj = Token.objects.get(key=token)
            return (token_obj.user, token)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token')