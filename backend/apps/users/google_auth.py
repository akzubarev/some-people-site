"""Google Identity Services credentials are verified only on the backend."""
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from django.conf import settings
from rest_framework.exceptions import ValidationError
import secrets


def verify_identity(credential, nonce):
    try:
        transport = Request()
        claims = id_token.verify_oauth2_token(credential, lambda *args, **kwargs: transport(*args, timeout=5, **kwargs), settings.GOOGLE_OAUTH_CLIENT_ID)
    except Exception as error:
        # Neither credentials nor provider errors belong in responses or logs.
        raise ValidationError({'detail': 'Google credential could not be verified. Try again.'}) from error
    if (claims.get('iss') not in ('accounts.google.com', 'https://accounts.google.com')
            or claims.get('aud') != settings.GOOGLE_OAUTH_CLIENT_ID
            or claims.get('email_verified') is not True
            or not isinstance(claims.get('sub'), str) or not claims['sub'] or len(claims['sub']) > 255
            or not isinstance(claims.get('nonce'), str)
            or not secrets.compare_digest(claims['nonce'].encode(), nonce.encode())):
        raise ValidationError({'detail': 'Invalid Google identity or challenge.'})
    return claims
