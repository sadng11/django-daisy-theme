# Design Specification: django-daisy-theme

- **Date:** 2026-10-01
- **Status:** Approved
- **Target Package Name:** `django-daisy-theme`
- **Module Name:** `django_daisy_theme`
- **License:** MIT License

---

## 1. Executive Summary & Objectives

`django-daisy-theme` is a modern, responsive, open-source plug-and-play theme for the Django Admin interface, built with Tailwind CSS v3.4, daisyUI v4, and Alpine.js.

### Key Goals:
1. **Zero-Configuration Plug-and-Play:** Works immediately upon adding `'django_daisy_theme'` to `INSTALLED_APPS` (before `'django.contrib.admin'`).
2. **First-Class RTL & LTR Support:** Automatic direction detection via Django's `get_current_language_bidi()`, paired with bundled web fonts (Vazirmatn for Persian/Arabic and Inter for Latin scripts).
3. **Responsive Mobile-First UI/UX:** DaisyUI Drawer for fluid mobile navigation and collapsible sidebar on desktop, card-based dashboards, floating action bars, and sticky save controls.
4. **Rich Customization:** Clean configuration via `DAISY_THEME_CONFIG` in `settings.py` (custom logos, titles, DaisyUI themes, custom sidebar links, dark/light theme switching).
5. **No Runtime Node.js Dependency:** Production CSS, JS, and font assets are pre-compiled and bundled directly within the Python package.
6. **Open Source & Extensible:** Distributed under the MIT license, preserving 100% of Django's native `ModelAdmin` APIs and template block hierarchies.

---

## 2. System Architecture & Directory Structure

The repository is organized into three distinct parts: the distributable Python package, an interactive sandbox/demo Django project, and the frontend asset build pipeline.

```text
django-theme/
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml
│
├── django_daisy_theme/               # Core Python Package
│   ├── __init__.py
│   ├── apps.py                       # AppConfig with metadata
│   ├── settings.py                   # Default configuration dictionary
│   ├── context_processors.py         # Injects theme configuration into admin contexts
│   ├── templatetags/
│   │   ├── __init__.py
│   │   └── daisy_theme.py            # Custom tags (direction, theme attributes, icons)
│   ├── static/django_daisy_theme/
│   │   ├── css/
│   │   │   ├── daisy-theme.min.css   # Compiled Tailwind + DaisyUI
│   │   │   └── fonts.css             # Font face definitions
│   │   ├── js/
│   │   │   ├── alpine.min.js         # Alpine.js runtime
│   │   │   └── daisy-theme.js        # Drawer, theme toggle, and search logic
│   │   ├── fonts/
│   │   │   ├── vazirmatn/            # WOFF2 files (Regular, Medium, Bold)
│   │   │   └── inter/                # WOFF2 files (Regular, Medium, Bold)
│   │   └── img/
│   │       ├── default-logo.svg
│   │       └── favicon.ico
│   └── templates/
│       └── admin/
│           ├── base.html             # Main skeleton (Drawer, Navbar, Sidebar, Footer)
│           ├── base_site.html        # Branding header
│           ├── index.html            # Dashboard (Metrics, App cards, Recent actions)
│           ├── login.html            # Glassmorphic centered login card
│           ├── change_list.html      # Responsive data table, filter drawer, search
│           ├── change_list_results.html # Styled table rows and headers
│           ├── change_form.html      # Fieldsets as cards, inline accordions, sticky save
│           ├── delete_confirmation.html # Confirmation modal/card
│           ├── delete_selected_confirmation.html
│           ├── object_history.html   # Timeline format for object revisions
│           └── includes/
│               ├── navbar.html       # Top navigation, breadcrumbs, search, theme switcher
│               ├── sidebar.html      # App/Model tree with Lucide icons
│               ├── theme_toggle.html # DaisyUI theme selector dropdown
│               ├── pagination.html   # DaisyUI join button pagination
│               └── stats_cards.html  # Quick metric summary cards
│
├── demo/                             # Live Sandbox Django Project
│   ├── manage.py
│   ├── demo/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── shop/                         # Test models for full widget validation
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       └── models.py                 # Category, Product, Order, OrderItem
│
└── frontend/                         # Asset compilation pipeline
    ├── package.json
    ├── tailwind.config.js
    └── src/
        └── styles.css
```

---

## 3. Package Configuration & Customization (`settings.py`)

### 3.1 Zero-Configuration Setup
```python
# settings.py
INSTALLED_APPS = [
    "django_daisy_theme",  # Place before django.contrib.admin
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # ... other apps
]
```

### 3.2 Optional Configuration Specification (`DAISY_THEME_CONFIG`)
```python
DAISY_THEME_CONFIG = {
    # 1. Brand Identity
    "SITE_TITLE": "Django Administration",
    "SITE_HEADER": "Daisy Theme Admin",
    "SITE_LOGO": None,               # Static path e.g. "/static/images/logo.svg"
    "SITE_LOGO_DARK": None,          # Static path for dark theme logo
    "FAVICON": None,

    # 2. DaisyUI Themes & Color Modes
    "DEFAULT_THEME": "light",        # Default data-theme attribute
    "DARK_THEME": "dark",            # Target theme when toggling dark mode
    "SHOW_THEME_SWITCHER": True,     # Enable dropdown in navbar
    "AVAILABLE_THEMES": [            # Allowed themes in selector
        "light", "dark", "emerald", "cupcake", "corporate", "synthwave", "night"
    ],

    # 3. Direction & Typography
    "DIRECTION": "auto",             # 'auto', 'rtl', or 'ltr'
    "LOAD_DEFAULT_FONTS": True,      # Load bundled Vazirmatn & Inter
    "FONT_FAMILY": None,             # Custom font-family override

    # 4. Navigation & Layout
    "COLLAPSIBLE_SIDEBAR": True,     # Enable desktop sidebar minimization
    "SHOW_RECENT_ACTIONS": True,     # Render recent actions in dashboard
    "CUSTOM_LINKS": [
        {
            "title": "Main Website",
            "url": "/",
            "icon": "globe",
            "target": "_blank",
        },
    ],

    # 5. Footer & Information
    "FOOTER_TEXT": "Powered by django-daisy-theme",
    "SHOW_VERSION": True,
}
```

---

## 4. Frontend & Design Architecture

### 4.1 Technology Stack
* **Tailwind CSS v3.4:** Utility-first CSS engine configured with logical properties for bi-directional layout.
* **daisyUI v4:** Semantic component classes (`btn`, `card`, `drawer`, `table`, `join`, `badge`, `input`).
* **Alpine.js v3.x:** Lightweight reactive UI controller for:
  * Mobile drawer open/close state.
  * Theme switching synced to `localStorage`.
  * Search palette and dropdown filters.
* **Lucide Icons:** Clean, modern SVG icons with automated fallbacks.
* **Fonts:**
  * **Vazirmatn (v33+):** Clean, accessible Persian/Arabic typography.
  * **Inter (v4+):** Highly readable Latin typography.

### 4.2 Bi-Directional Layout (RTL & LTR)
1. In `base.html`, the root element dynamically receives direction:
   ```html
   <html lang="{{ LANGUAGE_CODE }}" dir="{% if LANGUAGE_BIDI %}rtl{% else %}ltr{% endif %}" data-theme="light">
   ```
2. Direction-aware styling utilizes Tailwind's `rtl:` and `ltr:` modifiers, along with logical properties (`ps-`, `pe-`, `ms-`, `me-`).
3. Layout components automatically adjust:
   * LTR: Sidebar on left, profile/actions on right.
   * RTL: Sidebar on right, profile/actions on left.

---

## 5. Screen Specifications

### 5.1 Authentication (`admin/login.html`)
* Centered card with subtle backdrop gradient and glassmorphism effect.
* Brand logo, system title, clear error alerts (`alert alert-error`).
* Clean inputs with animated focus states and button loading feedback.

### 5.2 Dashboard (`admin/index.html`)
* **Header Greeting:** Welcome message with current user role and date.
* **Summary Metrics:** Stat cards displaying registered models and system activity.
* **App Cards Grid:** Organized into responsive grid (1 col mobile, 2 col tablet, 3 col desktop).
* **Recent Actions:** Timeline list displaying user modifications with action-specific badge colors (Green for addition, Blue for change, Red for deletion).

### 5.3 Data Tables (`admin/change_list.html`)
* **Search & Filter Bar:** Top search input with immediate clear button.
* **Filter Drawer/Modal:** Off-canvas or dropdown filter panel, freeing table horizontal space.
* **Table UI:** `table table-zebra table-hover` inside a rounded card with horizontal scroll indicator for overflow.
* **Multi-Action Bar:** Sticky bottom toolbar appearing only when records are selected.
* **Pagination:** DaisyUI `join` grouping with current page indicator.

### 5.4 Form View (`admin/change_form.html`)
* **Card-Based Fieldsets:** Clean visual separation between field groups.
* **Input Elements:** `input-bordered`, `select-bordered`, `textarea-bordered`.
* **Inlines:** Tabular and stacked inlines styled with card headers and discrete delete actions.
* **Sticky Action Bar:** Fixed bottom bar providing quick access to Save and Delete buttons regardless of scroll depth.

---

## 6. Testing & Quality Assurance Plan

### 6.1 Automated Unit Tests
* **Config Loader Tests:** Verify that default values are returned when `DAISY_THEME_CONFIG` is missing or partially populated.
* **Template Tags Tests:** Verify direction helpers, theme attribute helpers, and icon resolvers.
* **Static Assets Tests:** Verify that all required CSS, JS, and font files exist in `static/django_daisy_theme/` and return HTTP 200.

### 6.2 Sandbox Demo Project Validation
* Launch `demo/manage.py runserver` with SQLite.
* Populate sample data (Users, Categories, Products, Orders).
* Verify:
  1. Desktop and mobile viewports (Responsive Drawer).
  2. Language switching between Persian (`fa`) and English (`en`).
  3. DaisyUI theme switcher toggling themes and persisting in `localStorage`.
  4. Standard ModelAdmin features: filters, search, inline forms, bulk actions.

---

## 7. Distribution & Packaging

* **Build Tool:** `hatchling` (or `setuptools`) configured via `pyproject.toml`.
* **Package Data:** All templates and static assets included in sdist and wheel distributions.
* **License:** MIT License.
