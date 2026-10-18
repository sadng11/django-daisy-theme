import pytest

def test_default_theme_config():
    from django_daisy_theme.settings import get_theme_config
    
    config = get_theme_config()
    assert config["DEFAULT_THEME"] == "light"
    assert config["DARK_THEME"] == "dark"
    assert config["DIRECTION"] == "auto"
    assert config["LOAD_DEFAULT_FONTS"] is True
    assert config["ENABLE_SELECT2"] is True
    assert config["SHOW_GREETING_BANNER"] is True
    assert config["SHOW_STATS_CARDS"] is True
    assert "light" in config["AVAILABLE_THEMES"]
    assert "dark" in config["AVAILABLE_THEMES"]

def test_override_theme_config(settings):
    settings.DAISY_THEME_CONFIG = {
        "DEFAULT_THEME": "emerald",
        "SITE_TITLE": "Custom Admin Panel",
    }
    from django_daisy_theme.settings import get_theme_config
    
    config = get_theme_config()
    assert config["DEFAULT_THEME"] == "emerald"
    assert config["SITE_TITLE"] == "Custom Admin Panel"
    # Fallback to default
    assert config["DARK_THEME"] == "dark"
