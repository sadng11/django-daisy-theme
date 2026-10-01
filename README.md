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

Customize your admin panel inside `settings.py`:

```python
DAISY_THEME_CONFIG = {
    "SITE_TITLE": "My Company Admin",
    "SITE_HEADER": "Company Management",
    "SITE_LOGO": "/static/images/logo.svg",
    "DEFAULT_THEME": "light",
    "DARK_THEME": "dark",
    "SHOW_THEME_SWITCHER": True,
    "AVAILABLE_THEMES": ["light", "dark", "emerald", "cupcake", "night"],
    "DIRECTION": "auto",
    "COLLAPSIBLE_SIDEBAR": True,
}
```

---

## License

This project is licensed under the [MIT License](LICENSE).
