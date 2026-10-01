from django_daisy_theme.settings import get_theme_config


def daisy_theme_context(request):
    """
    Injects daisy_theme configuration into the template context.
    """
    return {
        "daisy_theme": get_theme_config(),
    }
