from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.core.exceptions import MultipleObjectsReturned


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_app(self, request, provider, client_id=None):
        """
        Override to handle MultipleObjectsReturned error
        """
        try:
            return super().get_app(request, provider, client_id)
        except (SocialApp.MultipleObjectsReturned, MultipleObjectsReturned):
            # If multiple apps exist, get the first one for the current site
            site = Site.objects.get_current(request)
            apps = SocialApp.objects.filter(
                provider=provider,
                sites=site
            )
            if client_id:
                apps = apps.filter(client_id=client_id)
            
            # Return the first app found
            app = apps.first()
            if app:
                return app
            
            # If no app found for current site, try without site filter
            apps = SocialApp.objects.filter(provider=provider)
            if client_id:
                apps = apps.filter(client_id=client_id)
            return apps.first()