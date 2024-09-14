"""Auth utils."""
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


def encode_uuid(uuid: str) -> str:
    """Encode uuid for authorization."""
    return force_str(urlsafe_base64_encode(force_bytes(uuid)))


def decode_uuid(encoded: str) -> str:
    """Decode uuid for authorization."""
    return force_str(urlsafe_base64_decode(encoded))
