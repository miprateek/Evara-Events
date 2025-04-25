from django.conf import settings
from .models import MapSettings

def map_url(request):
    """
    Provides the Google Maps embed URL to all templates.
    First tries to get the default map URL from the database,
    falls back to settings if none exists.
    """
    try:
        map_settings = MapSettings.objects.filter(is_default=True).first()
        if map_settings:
            return {'google_maps_url': map_settings.map_url}
    except:
        pass
    
    return {'google_maps_url': settings.GOOGLE_MAPS_EMBED_URL}