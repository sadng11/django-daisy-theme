from pathlib import Path


def test_static_assets_exist():
    base_static = (
        Path(__file__).resolve().parent.parent
        / "django_daisy_theme"
        / "static"
        / "django_daisy_theme"
    )
    assert (base_static / "css" / "daisy-theme.min.css").is_file()
    assert (base_static / "css" / "fonts.css").is_file()
    assert (base_static / "js" / "alpine.min.js").is_file()
    assert (base_static / "js" / "daisy-theme.js").is_file()
    assert (base_static / "js" / "select2-init.js").is_file()
    assert (base_static / "fonts" / "vazirmatn").is_dir()
    assert (base_static / "fonts" / "inter").is_dir()

    # Verify font files exist
    assert any((base_static / "fonts" / "vazirmatn").glob("*.woff2"))
    assert any((base_static / "fonts" / "inter").glob("*.woff2"))

    # Verify daisy-theme.min.css has non-trivial size
    css_size = (base_static / "css" / "daisy-theme.min.css").stat().st_size
    assert css_size > 5000, f"CSS file too small: {css_size} bytes"
