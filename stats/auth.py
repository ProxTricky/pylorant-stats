import os
from functools import wraps
from typing import Optional

from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.core.exceptions import PermissionDenied
from jose import jwt
from auth0.authentication import GetToken
from auth0.management import Auth0

# Auth0 configuration
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
AUTH0_AUDIENCE = os.getenv('AUTH0_AUDIENCE')
ALGORITHMS = ['RS256']
ALLOWED_EMAIL = os.getenv('AUTH0_ALLOWED_EMAIL')

def get_auth0_token():
    """Obtenir un token de gestion Auth0"""
    get_token = GetToken(AUTH0_DOMAIN, AUTH0_CLIENT_ID, client_secret=AUTH0_CLIENT_SECRET)
    token = get_token.client_credentials(AUTH0_AUDIENCE)
    return token['access_token']

def verify_token(token: str) -> Optional[dict]:
    """Vérifier et décoder le JWT token"""
    try:
        # Récupérer la clé publique depuis Auth0
        jwks_url = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'
        jwks_client = jwt.PyJWKClient(jwks_url)
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        # Vérifier et décoder le token
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=ALGORITHMS,
            audience=AUTH0_AUDIENCE,
            issuer=f'https://{AUTH0_DOMAIN}/'
        )
        
        return payload
    except Exception as e:
        print(f"Token verification failed: {str(e)}")
        return None

def require_auth(f):
    """Décorateur pour protéger les routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = args[0].META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            raise PermissionDenied("No token provided")

        token = auth_header.split(' ')[1]
        payload = verify_token(token)
        
        if not payload:
            raise PermissionDenied("Invalid token")

        # Vérifier l'email de l'utilisateur
        email = payload.get('email')
        if email != ALLOWED_EMAIL:
            raise PermissionDenied("Unauthorized email")

        return f(*args, **kwargs)
    return decorated

def get_auth0_user_info(access_token: str) -> dict:
    """Récupérer les informations de l'utilisateur depuis Auth0"""
    auth0_mgmt = Auth0(AUTH0_DOMAIN, get_auth0_token())
    user_info = auth0_mgmt.users.get(access_token)
    return user_info
