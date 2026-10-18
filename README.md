# django-daisy-theme 🌼

A modern, responsive, and customizable theme for the Django Admin interface built with **Tailwind CSS v3.4**, **daisyUI v4**, and **Alpine.js**.

---

## Features

- ⚡ **Zero-Configuration Plug-and-Play:** Install and add to `INSTALLED_APPS` — that's it!
- 🌐 **Native RTL & LTR Bi-Directional Support:** Automatic direction detection via `get_current_language_bidi()` with tailored typography (Vazirmatn for Persian/Arabic, Inter for Latin).
- 📱 **Mobile-First Responsive Layout:** Fluid DaisyUI Drawer for mobile touch navigation and collapsible sidebar on desktop.
- 🎨 **Theme Switcher:** Seamless switching between DaisyUI themes (`light`, `dark`, `emerald`, `cupcake`, `synthwave`, `night`, etc.) synced to `localStorage`.
- 📊 **Modern Dashboard:** Card-based app & model groupings, quick action buttons, metric stats, and styled activity feeds.
- 🔍 **Enhanced Data Tables:** Slide-over filter drawer, floating action bar, and zebra-striped tables.
- 📦 **No Node.js Required:** Production CSS, JS, and font assets are pre-compiled and bundled directly within the Python package.

---

## Installation

```bash
pip install django-daisy-theme
```

Add `django_daisy_theme` to your `INSTALLED_APPS` in `settings.py` **before** `django.contrib.admin`:

```python
INSTALLED_APPS = [
    "django_daisy_theme",       # Must be before django.contrib.admin
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # ...
]
```

---

## Configuration (Optional)

Customize your admin panel inside `settings.py` by defining `DAISY_THEME_CONFIG`:

```python
DAISY_THEME_CONFIG = {
    # Site Branding
    "SITE_TITLE": "Django Administration",                   # Browser tab title
    "SITE_HEADER": "Daisy Theme Admin",                      # Brand text in navbar & login
    "SITE_LOGO": "/static/images/logo.svg",                  # Light mode logo URL (or None)
    "SITE_LOGO_DARK": "/static/images/logo-dark.svg",        # Dark mode logo URL (or None)
    "FAVICON": "/static/images/favicon.ico",                 # Favicon URL (or None)

    # Themes & Color Palettes
    "DEFAULT_THEME": "light",                                # Default DaisyUI theme
    "DARK_THEME": "dark",                                    # Target theme for quick dark toggle
    "SHOW_THEME_SWITCHER": True,                             # Show/hide theme dropdown in navbar
    "AVAILABLE_THEMES": [                                    # Themes displayed in the dropdown
        "light",
        "dark",
        "emerald",
        "cupcake",
        "corporate",
        "synthwave",
        "night",
    ],

    # Layout, Direction & Fonts
    "DIRECTION": "auto",                                     # "auto", "rtl", or "ltr"
    "LOAD_DEFAULT_FONTS": True,                              # Load bundled Vazirmatn & Inter fonts
    "FONT_FAMILY": None,                                     # Custom font-family override (or None)
    "COLLAPSIBLE_SIDEBAR": True,                             # Collapsible sidebar with drawer mode
    "SHOW_BREADCRUMBS": True,                                # Show/hide navigation breadcrumbs
    "ENABLE_SELECT2": True,                                  # Enhance select boxes with Select2

    # Dashboard & Navigation
    "SHOW_RECENT_ACTIONS": True,                             # Show recent activity feed on dashboard
    "CUSTOM_LINKS": [                                        # Custom links in navbar & sidebar
        {
            "title": "Website",
            "url": "https://example.com",
            "icon": "globe",
            "target": "_blank",
        },
        {
            "title": "Documentation",
            "url": "/docs/",
            "icon": "file-text",
            "target": "_self",
        },
    ],

    # Footer
    "FOOTER_TEXT": "Powered by django-daisy-theme",          # Custom footer text
    "SHOW_VERSION": True,                                    # Show package version in footer/sidebar
}
```

---

## Configuration Reference

| Option | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `SITE_TITLE` | `str` | `"Django Administration"` | Browser page title suffix (`<title>`). |
| `SITE_HEADER` | `str` | `"Daisy Theme Admin"` | Brand title displayed in the navbar and login page. |
| `SITE_LOGO` | `str \| None` | `None` | Path or URL to the brand logo image. |
| `SITE_LOGO_DARK` | `str \| None` | `None` | Path or URL to the dark mode brand logo image. |
| `FAVICON` | `str \| None` | `None` | Path or URL to the browser favicon. |
| `DEFAULT_THEME` | `str` | `"light"` | Initial DaisyUI theme applied on first visit. |
| `DARK_THEME` | `str` | `"dark"` | Target theme when using the quick Dark/Light toggle button. |
| `SHOW_THEME_SWITCHER` | `bool` | `True` | Display the theme selector dropdown and dark/light toggle. |
| `AVAILABLE_THEMES` | `list[str]` | `["light", "dark", "emerald", "cupcake", "corporate", "synthwave", "night"]` | List of DaisyUI themes to show in the theme dropdown. |
| `DIRECTION` | `str` | `"auto"` | `"auto"` (detects RTL/LTR from active language), `"rtl"`, or `"ltr"`. |
| `LOAD_DEFAULT_FONTS` | `bool` | `True` | Automatically load bundled Vazirmatn (RTL) and Inter (LTR) fonts. |
| `FONT_FAMILY` | `str \| None` | `None` | Custom CSS font-family string (e.g. `'Roboto', sans-serif`). |
| `COLLAPSIBLE_SIDEBAR` | `bool` | `True` | Enable collapsible sidebar on desktop and drawer on mobile. |
| `SHOW_BREADCRUMBS` | `bool` | `True` | Show navigation breadcrumb trail on admin pages. |
| `ENABLE_SELECT2` | `bool` | `True` | Automatically enhance select inputs with Select2 search. |
| `SHOW_RECENT_ACTIONS` | `bool` | `True` | Show the recent activity / history cards on the main dashboard. |
| `CUSTOM_LINKS` | `list[dict]` | `[]` | List of custom external or internal navigation links. |
| `FOOTER_TEXT` | `str` | `"Powered by django-daisy-theme"` | Custom text displayed at the bottom of admin pages. |
| `SHOW_VERSION` | `bool` | `True` | Show the package version badge in the footer / sidebar. |

---

### Custom Links Icons
You can use any of the built-in Lucide icons for `CUSTOM_LINKS`:
`home`, `dashboard`, `users`, `user`, `folder`, `file-text`, `edit`, `trash`, `plus`, `search`, `sun`, `moon`, `palette`, `globe`, `check`, `alert-circle`, `log-out`, `key`, `shopping-cart`, `tag`, `layers`, `settings`, `help-circle`, `external-link`, `filter`, `clock`, `history`, `arrow-left`, `arrow-right`, `lock`, `shield-check`.

### Supported DaisyUI Themes
`light`, `dark`, `cupcake`, `bumblebee`, `emerald`, `corporate`, `synthwave`, `retro`, `cyberpunk`, `valentine`, `halloween`, `garden`, `forest`, `aqua`, `lofi`, `pastel`, `fantasy`, `wireframe`, `black`, `luxury`, `dracula`, `cmyk`, `autumn`, `business`, `acid`, `lemonade`, `night`, `coffee`, `winter`, `dim`, `nord`, `sunset`.

---

## License

This project is licensed under the [MIT License](LICENSE).
