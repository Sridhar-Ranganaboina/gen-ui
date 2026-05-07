import hmac
import os
from hashlib import sha256

API_TOKEN = os.getenv('GENUI_API_TOKEN', 'dev-token')
SIGNING_KEY = os.getenv('GENUI_SIGNING_KEY', 'dev-signing-key')

def is_authorized(headers, body: bytes = b'') -> bool:
    auth = headers.get('Authorization', '')
    if auth == f'Bearer {API_TOKEN}':
        return True
    signature = headers.get('X-GenUI-Signature', '')
    if signature:
        expected = hmac.new(SIGNING_KEY.encode(), body, sha256).hexdigest()
        return hmac.compare_digest(signature, expected)
    return False
