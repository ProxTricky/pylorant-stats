from django.conf import settings
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.http import HttpResponseForbidden

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """Vérifie que l'email est autorisé avant de permettre la connexion"""
        email = sociallogin.user.email
        if email != settings.ALLOWED_EMAIL:
            raise ImmediateHttpResponse(
                HttpResponseForbidden('Unauthorized email address')
            )
        return super().pre_social_login(request, sociallogin)
