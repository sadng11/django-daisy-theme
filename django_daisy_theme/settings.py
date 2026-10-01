from copy import deepcopy
from django.conf import settings

DEFAULT_CONFIG = {
    "SITE_TITLE": "Django Administration",
    "SITE_HEADER": "Daisy Theme Admin",
    "SITE_LOGO": None,
    "SITE_LOGO_DARK": None,
    "FAVICON": None,
    "DEFAULT_THEME": "light",
    "DARK_THEME": "dark",
    "SHOW_THEME_SWITCHER": True,
    "AVAILABLE_THEMES": [
        "light",
        "dark",
        "emerald",
        "cupcake",
        "corporate",
        "synthwave",
        "night",
    ],
    "DIRECTION": "auto",
    "LOAD_DEFAULT_FONTS": True,
    "FONT_FAMILY": None,
    "COLLAPSIBLE_SIDEBAR": True,
    "SHOW_RECENT_ACTIONS": True,
    "CUSTOM_LINKS": [],
    "FOOTER_TEXT": "Powered by django-daisy-theme",
    "SHOW_VERSION": True,
    "ENABLE_SELECT2": True,
}


def get_theme_config(key=None):
    """
    Returns the active theme configuration dictionary merged with default settings.
    If a specific key is requested, returns its value.
    """
    user_config = getattr(settings, "DAISY_THEME_CONFIG", {})
    merged = deepcopy(DEFAULT_CONFIG)
    merged.update(user_config)
    if key:
        return merged.get(key)
    return merged
