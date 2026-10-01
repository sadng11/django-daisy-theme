# django-daisy-theme Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and package `django-daisy-theme`, a modern, responsive, zero-configuration DaisyUI v4 + Tailwind CSS v3.4 theme for Django Admin with native bi-directional RTL/LTR support and rich customization.

**Architecture:** The project overrides standard Django admin templates using modular DaisyUI components and Alpine.js interactivity. Dynamic styling and direction are injected via a lightweight context processor and custom template tags that read `DAISY_THEME_CONFIG` with zero-config fallbacks. CSS, JS, and web fonts (Vazirmatn & Inter) are bundled inside the Python wheel package with no runtime Node.js dependency.

**Tech Stack:** Python 3.11+, Django 4.2+/5.x, Tailwind CSS v3.4, daisyUI v4, Alpine.js v3, Lucide Icons, Vazirmatn & Inter fonts, hatchling/setuptools.

**Spec:** [docs/superpowers/specs/2026-10-01-django-daisy-theme-design.md](file:///data/python/django-theme/docs/superpowers/specs/2026-10-01-django-daisy-theme-design.md)

## Global Constraints

- Package name on PyPI: `django-daisy-theme`, Python import name: `django_daisy_theme`.
- License: MIT License.
- Zero mandatory Node.js runtime for the end-user (all static files are pre-compiled and included in package distributions).
- Standard ModelAdmin compatibility: Never break or alter standard Django ModelAdmin APIs (`list_display`, `list_filter`, `inlines`, `actions`, `search_fields`).
- Bi-directional support: Fully responsive in both LTR and RTL with automatic direction detection via `get_current_language_bidi()`.
- Bundled fonts: Vazirmatn for Persian/Arabic RTL, Inter for Latin LTR.

---

### Task 1: Python Project Packaging, Config & App Setup

**Files:**
- Create: `.gitignore`
- Create: `LICENSE`
- Create: `README.md`
- Create: `pyproject.toml`
- Create: `django_daisy_theme/__init__.py`
- Create: `django_daisy_theme/apps.py`
- Create: `django_daisy_theme/settings.py`
- Test: `tests/test_config.py`

**Interfaces:**
- Produces: `django_daisy_theme.settings.get_theme_config(key=None)` returning the active configuration merged with defaults.
- Produces: `django_daisy_theme.apps.DjangoDaisyThemeConfig` app config.

- [ ] **Step 1: Create virtual environment and install test requirements**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install "django>=4.2,<5.2" pytest pytest-django
```

- [ ] **Step 2: Write failing test for theme configuration defaults**

```python
# tests/test_config.py
import pytest
from django.conf import settings

def test_default_theme_config():
    from django_daisy_theme.settings import get_theme_config, DEFAULT_CONFIG
    
    config = get_theme_config()
    assert config["DEFAULT_THEME"] == "light"
    assert config["DARK_THEME"] == "dark"
    assert config["DIRECTION"] == "auto"
    assert config["LOAD_DEFAULT_FONTS"] is True
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
```

- [ ] **Step 3: Run test to verify failure**

```bash
source .venv/bin/activate
pytest tests/test_config.py -v
```
Expected: FAIL with `ModuleNotFoundError: No module named 'django_daisy_theme'`

- [ ] **Step 4: Implement minimal project setup and configuration module**

```python
# django_daisy_theme/__init__.py
__version__ = "0.1.0"
default_app_config = "django_daisy_theme.apps.DjangoDaisyThemeConfig"
```

```python
# django_daisy_theme/apps.py
from django.apps import AppConfig

class DjangoDaisyThemeConfig(AppConfig):
    name = "django_daisy_theme"
    verbose_name = "Daisy Theme for Django Admin"
```

```python
# django_daisy_theme/settings.py
from django.conf import settings
from copy import deepcopy

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
        "light", "dark", "emerald", "cupcake", "corporate", "synthwave", "night"
    ],
    "DIRECTION": "auto",
    "LOAD_DEFAULT_FONTS": True,
    "FONT_FAMILY": None,
    "COLLAPSIBLE_SIDEBAR": True,
    "SHOW_RECENT_ACTIONS": True,
    "CUSTOM_LINKS": [],
    "FOOTER_TEXT": "Powered by django-daisy-theme",
    "SHOW_VERSION": True,
}

def get_theme_config(key=None):
    user_config = getattr(settings, "DAISY_THEME_CONFIG", {})
    merged = deepcopy(DEFAULT_CONFIG)
    merged.update(user_config)
    if key:
        return merged.get(key)
    return merged
```

Create packaging files:
- `pyproject.toml` with `setuptools` build backend, package metadata, inclusion of templates and static assets.
- `LICENSE` with MIT text.
- `.gitignore` with Python, virtual environment, node_modules, and cache files ignored.

- [ ] **Step 5: Run tests to verify they pass**

```bash
source .venv/bin/activate
pytest tests/test_config.py -v
```
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add .gitignore LICENSE pyproject.toml README.md django_daisy_theme/ tests/
git commit -m "feat: initial package structure, configuration loader and tests"
```

---

### Task 2: Context Processors & Template Tags (Direction, Theme, Icons)

**Files:**
- Create: `django_daisy_theme/context_processors.py`
- Create: `django_daisy_theme/templatetags/__init__.py`
- Create: `django_daisy_theme/templatetags/daisy_theme.py`
- Test: `tests/test_templatetags.py`

**Interfaces:**
- Consumes: `django_daisy_theme.settings.get_theme_config`
- Produces: `daisy_theme_context(request)` context processor returning `daisy_theme` dict.
- Produces: `daisy_direction(request)` template tag returning `'rtl'` or `'ltr'`.
- Produces: `daisy_theme_attr()` template tag returning `data-theme="..."`.
- Produces: `daisy_icon(name, css_class="")` template tag rendering inline SVG icons.

- [ ] **Step 1: Write failing tests for context processor and template tags**

```python
# tests/test_templatetags.py
import pytest
from django.test import RequestFactory
from django.utils import translation
from django_daisy_theme.context_processors import daisy_theme_context
from django_daisy_theme.templatetags.daisy_theme import daisy_direction, daisy_theme_attr, daisy_icon

def test_context_processor():
    rf = RequestFactory()
    request = rf.get("/admin/")
    ctx = daisy_theme_context(request)
    assert "daisy_theme" in ctx
    assert ctx["daisy_theme"]["DEFAULT_THEME"] == "light"

def test_direction_auto_persian():
    rf = RequestFactory()
    request = rf.get("/admin/")
    with translation.override("fa"):
        assert daisy_direction(request) == "rtl"

def test_direction_auto_english():
    rf = RequestFactory()
    request = rf.get("/admin/")
    with translation.override("en"):
        assert daisy_direction(request) == "ltr"

def test_daisy_icon_rendering():
    svg = daisy_icon("home", css_class="w-5 h-5")
    assert "<svg" in svg
    assert "w-5 h-5" in svg
```

- [ ] **Step 2: Run test to verify failure**

```bash
source .venv/bin/activate
pytest tests/test_templatetags.py -v
```
Expected: FAIL with `ModuleNotFoundError` for context_processors.

- [ ] **Step 3: Implement context processor and template tags**

Implement `django_daisy_theme/context_processors.py`:
```python
from django_daisy_theme.settings import get_theme_config

def daisy_theme_context(request):
    return {
        "daisy_theme": get_theme_config(),
    }
```

Implement `django_daisy_theme/templatetags/daisy_theme.py`:
- `daisy_direction(request)`: Checks `get_theme_config("DIRECTION")`. If `'auto'`, uses `translation.get_language_bidi()`. Otherwise returns `'rtl'` or `'ltr'`.
- `daisy_theme_attr()`: Returns `get_theme_config("DEFAULT_THEME")`.
- `daisy_icon(name, css_class="")`: Returns Lucide inline SVGs for common admin icons (`home`, `users`, `folder`, `edit`, `trash`, `plus`, `search`, `sun`, `moon`, `chevron-down`, `menu`, etc.).

- [ ] **Step 4: Run tests to verify they pass**

```bash
source .venv/bin/activate
pytest tests/test_templatetags.py -v
```
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add django_daisy_theme/context_processors.py django_daisy_theme/templatetags/ tests/test_templatetags.py
git commit -m "feat: add context processor, direction detection and daisy template tags"
```

---

### Task 3: Asset Build Pipeline & Static Files (Tailwind + DaisyUI + Fonts + Alpine)

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/tailwind.config.js`
- Create: `frontend/src/styles.css`
- Create: `django_daisy_theme/static/django_daisy_theme/css/fonts.css`
- Create: `django_daisy_theme/static/django_daisy_theme/js/alpine.min.js`
- Create: `django_daisy_theme/static/django_daisy_theme/js/daisy-theme.js`
- Create: `django_daisy_theme/static/django_daisy_theme/fonts/` (Vazirmatn & Inter woff2 files)
- Test: `tests/test_assets.py`

**Interfaces:**
- Produces: `django_daisy_theme/static/django_daisy_theme/css/daisy-theme.min.css` (compiled CSS containing all daisyUI components and utility classes).
- Produces: `django_daisy_theme/static/django_daisy_theme/js/daisy-theme.js` containing Alpine store for theme toggling (`localStorage` sync) and drawer controls.

- [ ] **Step 1: Write test to verify static assets presence and integrity**

```python
# tests/test_assets.py
from pathlib import Path

def test_static_assets_exist():
    base_static = Path(__file__).resolve().parent.parent / "django_daisy_theme" / "static" / "django_daisy_theme"
    assert (base_static / "css" / "daisy-theme.min.css").is_file()
    assert (base_static / "css" / "fonts.css").is_file()
    assert (base_static / "js" / "alpine.min.js").is_file()
    assert (base_static / "js" / "daisy-theme.js").is_file()
    assert (base_static / "fonts" / "vazirmatn").is_dir()
    assert (base_static / "fonts" / "inter").is_dir()
```

- [ ] **Step 2: Run test to verify failure**

```bash
source .venv/bin/activate
pytest tests/test_assets.py -v
```
Expected: FAIL (files do not exist yet)

- [ ] **Step 3: Setup frontend build configuration and download fonts/scripts**

1. Create `frontend/package.json` with dependencies:
   - `tailwindcss@^3.4.17`
   - `daisyui@^4.12.23`
   - `autoprefixer@^10.4.20`
   - `postcss@^8.4.49`
2. Create `frontend/tailwind.config.js`:
   - Content scans all templates in `django_daisy_theme/templates/**/*.html`
   - DaisyUI plugin configured with all 30+ themes
3. Download Alpine.js v3.x bundle into `django_daisy_theme/static/django_daisy_theme/js/alpine.min.js`.
4. Bundle Vazirmatn and Inter woff2 font files and write `fonts.css` with `@font-face` declarations.
5. Create `daisy-theme.js` containing Alpine component `daisyThemeApp()`:
   - Manages active theme from `localStorage` or defaults to `data-theme`.
   - Syncs dark/light toggle and dropdown selection.
   - Manages mobile drawer state.
6. Run `npm install` and `npm run build` to compile `daisy-theme.min.css`.

- [ ] **Step 4: Run test to verify static assets pass**

```bash
source .venv/bin/activate
pytest tests/test_assets.py -v
```
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add frontend/ django_daisy_theme/static/ tests/test_assets.py
git commit -m "feat: compile daisyUI CSS, bundle Alpine.js and web fonts"
```

---

### Task 4: Base Layout & Authentication Templates

**Files:**
- Create: `django_daisy_theme/templates/admin/base.html`
- Create: `django_daisy_theme/templates/admin/base_site.html`
- Create: `django_daisy_theme/templates/admin/login.html`
- Create: `django_daisy_theme/templates/admin/includes/navbar.html`
- Create: `django_daisy_theme/templates/admin/includes/sidebar.html`
- Create: `django_daisy_theme/templates/admin/includes/theme_toggle.html`
- Create: `django_daisy_theme/templates/admin/includes/breadcrumbs.html`
- Test: `tests/test_templates_base.py`

**Interfaces:**
- Consumes: `daisy_theme_context`, `daisy_theme` template tags, static CSS & JS.
- Produces: Standard Django Admin base layout responsive on mobile (DaisyUI drawer) and desktop (collapsible sidebar), with glassmorphic `login.html`.

- [ ] **Step 1: Write failing test for base template and login rendering**

```python
# tests/test_templates_base.py
from django.template.loader import render_to_string
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser

def test_login_template_renders():
    rf = RequestFactory()
    request = rf.get("/admin/login/")
    request.user = AnonymousUser()
    rendered = render_to_string("admin/login.html", {
        "title": "Log in",
        "app_path": "/admin/login/",
        "daisy_theme": {"SITE_HEADER": "Test Daisy Admin", "DEFAULT_THEME": "light", "DIRECTION": "auto", "AVAILABLE_THEMES": ["light", "dark"]},
    }, request=request)
    assert "Test Daisy Admin" in rendered
    assert "daisy-theme.min.css" in rendered
    assert "<form" in rendered
```

- [ ] **Step 2: Run test to verify failure**

```bash
source .venv/bin/activate
pytest tests/test_templates_base.py -v
```
Expected: FAIL with `TemplateDoesNotExist: admin/login.html`

- [ ] **Step 3: Implement base layout, partials and login template**

1. `admin/base.html`:
   - Dynamic `<html dir="{% daisy_direction request %}" lang="{{ LANGUAGE_CODE }}" data-theme="...">`
   - Responsive drawer container (`<div class="drawer lg:drawer-open">`)
   - Drawer toggle checkbox (`<input id="admin-drawer" type="checkbox" class="drawer-toggle" />`)
   - Drawer content: `navbar.html`, `breadcrumbs.html`, messages alert blocks, `{% block content %}`, and footer.
   - Drawer side: `sidebar.html` with app/model hierarchy, Lucide icons, and collapse toggle.
2. `admin/includes/navbar.html`:
   - Mobile hamburger button (`label for="admin-drawer"`).
   - Brand title/logo.
   - Theme toggle dropdown (`theme_toggle.html`).
   - User profile dropdown with avatar, change password, and logout links.
3. `admin/login.html`:
   - Centered card layout with subtle backdrop glassmorphism.
   - Brand logo, clean username/password inputs (`input input-bordered`), and submit button with hover effects.

- [ ] **Step 4: Run tests to verify they pass**

```bash
source .venv/bin/activate
pytest tests/test_templates_base.py -v
```
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add django_daisy_theme/templates/ tests/test_templates_base.py
git commit -m "feat: implement responsive base layout, drawer, navbar and login templates"
```

---

### Task 5: Dashboard & Error Templates

**Files:**
- Create: `django_daisy_theme/templates/admin/index.html`
- Create: `django_daisy_theme/templates/admin/includes/stats_cards.html`
- Create: `django_daisy_theme/templates/admin/404.html`
- Create: `django_daisy_theme/templates/admin/500.html`
- Create: `django_daisy_theme/templates/admin/delete_confirmation.html`
- Test: `tests/test_templates_dashboard.py`

**Interfaces:**
- Consumes: Django admin context (`app_list`, `has_permission`, `user`).
- Produces: Modern dashboard featuring app & model cards, quick metric stats, and styled recent actions feed.

- [ ] **Step 1: Write failing test for dashboard index rendering**

```python
# tests/test_templates_dashboard.py
from django.template.loader import render_to_string
from django.test import RequestFactory
from django.contrib.auth.models import User

def test_index_dashboard_renders():
    rf = RequestFactory()
    request = rf.get("/admin/")
    user = User(username="admin", is_staff=True, is_superuser=True)
    request.user = user
    app_list = [{
        "name": "Authentication",
        "app_label": "auth",
        "app_url": "/admin/auth/",
        "has_module_perms": True,
        "models": [
            {
                "name": "Users",
                "object_name": "User",
                "admin_url": "/admin/auth/user/",
                "add_url": "/admin/auth/user/add/",
                "view_only": False,
            }
        ],
    }]
    rendered = render_to_string("admin/index.html", {
        "app_list": app_list,
        "user": user,
        "title": "Site administration",
        "daisy_theme": {"SHOW_RECENT_ACTIONS": True, "DEFAULT_THEME": "light", "DIRECTION": "auto", "AVAILABLE_THEMES": ["light", "dark"]},
    }, request=request)
    assert "Authentication" in rendered
    assert "Users" in rendered
    assert "/admin/auth/user/add/" in rendered
```

- [ ] **Step 2: Run test to verify failure**

```bash
source .venv/bin/activate
pytest tests/test_templates_dashboard.py -v
```
Expected: FAIL with `TemplateDoesNotExist: admin/index.html`

- [ ] **Step 3: Implement dashboard index and error templates**

1. `admin/index.html`:
   - Welcome banner with greeting and date.
   - Quick stats cards: total apps, total models.
   - Responsive grid of apps (`grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6`).
   - Each app card has app title, model list items with links, badge counts, and quick `+` add buttons.
   - Right/bottom column for recent activity feed with color-coded badges (created/modified/deleted).
2. `admin/404.html` and `500.html`:
   - Friendly modern DaisyUI card with clear message and "Back to Dashboard" button.
3. `admin/delete_confirmation.html`:
   - Alert modal style card with warning icon and explicit object deletion tree.

- [ ] **Step 4: Run tests to verify they pass**

```bash
source .venv/bin/activate
pytest tests/test_templates_dashboard.py -v
```
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add django_daisy_theme/templates/admin/index.html django_daisy_theme/templates/admin/includes/stats_cards.html django_daisy_theme/templates/admin/404.html django_daisy_theme/templates/admin/500.html django_daisy_theme/templates/admin/delete_confirmation.html tests/test_templates_dashboard.py
git commit -m "feat: implement modern dashboard cards, stats, and error templates"
```

---

### Task 6: Data Table (Change List) & Filter Drawer

**Files:**
- Create: `django_daisy_theme/templates/admin/change_list.html`
- Create: `django_daisy_theme/templates/admin/change_list_results.html`
- Create: `django_daisy_theme/templates/admin/includes/pagination.html`
- Create: `django_daisy_theme/templates/admin/actions.html`
- Test: `tests/test_templates_changelist.py`

**Interfaces:**
- Consumes: Django standard `cl` (ChangeList) object, `action_form`.
- Produces: DaisyUI `table table-zebra table-hover` inside card container, slide-over filter drawer, floating bulk actions bar, and `join` pagination.

- [ ] **Step 1: Write failing test for change_list rendering**

```python
# tests/test_templates_changelist.py
from django.template.loader import render_to_string
from django.test import RequestFactory
from django.contrib.auth.models import User

def test_changelist_template_exists_and_loads():
    rf = RequestFactory()
    request = rf.get("/admin/auth/user/")
    user = User(username="admin", is_staff=True, is_superuser=True)
    request.user = user
    rendered = render_to_string("admin/change_list.html", {
        "title": "Select user to change",
        "module_name": "users",
        "has_add_permission": True,
        "daisy_theme": {"DEFAULT_THEME": "light", "DIRECTION": "auto", "AVAILABLE_THEMES": ["light", "dark"]},
    }, request=request)
    assert "table" in rendered or "table-zebra" in rendered
```

- [ ] **Step 2: Run test to verify failure**

```bash
source .venv/bin/activate
pytest tests/test_templates_changelist.py -v
```
Expected: FAIL with `TemplateDoesNotExist: admin/change_list.html`

- [ ] **Step 3: Implement change_list, results, actions, and pagination**

1. `admin/change_list.html`:
   - Top action bar: Search input with search icon and clear button, "+ Add <model>" primary button, and Filter drawer toggle button.
   - Table wrapper with rounded card, border, and horizontal scroll indicator.
   - Filter drawer/modal: Off-canvas drawer on the right/left displaying date hierarchies and field filters with clean DaisyUI radio/select pills.
2. `admin/change_list_results.html`:
   - Styled table headers with sort indicator arrows.
   - Table rows with zebra stripes, hover effects, and boolean chips (`badge badge-success` / `badge badge-error`).
3. `admin/actions.html`:
   - Floating action toolbar showing count of selected items with select dropdown and submit button.
4. `admin/includes/pagination.html`:
   - DaisyUI `join` button group with previous, next, and active page numbers.

- [ ] **Step 4: Run tests to verify they pass**

```bash
source .venv/bin/activate
pytest tests/test_templates_changelist.py -v
```
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add django_daisy_theme/templates/admin/change_list.html django_daisy_theme/templates/admin/change_list_results.html django_daisy_theme/templates/admin/includes/pagination.html django_daisy_theme/templates/admin/actions.html tests/test_templates_changelist.py
git commit -m "feat: implement change_list data table, filter drawer, pagination and actions"
```

---

### Task 7: Form View (Change Form) & Inlines

**Files:**
- Create: `django_daisy_theme/templates/admin/change_form.html`
- Create: `django_daisy_theme/templates/admin/submit_line.html`
- Create: `django_daisy_theme/templates/admin/edit_inline/tabular.html`
- Create: `django_daisy_theme/templates/admin/edit_inline/stacked.html`
- Test: `tests/test_templates_changeform.py`

**Interfaces:**
- Consumes: Django standard `adminform`, `inline_admin_formsets`, `errors`.
- Produces: Card-based form fieldsets, modern styled inputs/selects, styled tabular and stacked inlines, and sticky bottom save bar (`submit_line.html`).

- [ ] **Step 1: Write failing test for change_form rendering**

```python
# tests/test_templates_changeform.py
from django.template.loader import render_to_string
from django.test import RequestFactory
from django.contrib.auth.models import User

def test_changeform_template_renders():
    rf = RequestFactory()
    request = rf.get("/admin/auth/user/add/")
    user = User(username="admin", is_staff=True, is_superuser=True)
    request.user = user
    rendered = render_to_string("admin/change_form.html", {
        "title": "Add user",
        "has_change_permission": True,
        "has_add_permission": True,
        "has_delete_permission": False,
        "save_as": False,
        "show_save": True,
        "daisy_theme": {"DEFAULT_THEME": "light", "DIRECTION": "auto", "AVAILABLE_THEMES": ["light", "dark"]},
    }, request=request)
    assert "<form" in rendered
```

- [ ] **Step 2: Run test to verify failure**

```bash
source .venv/bin/activate
pytest tests/test_templates_changeform.py -v
```
Expected: FAIL with `TemplateDoesNotExist: admin/change_form.html`

- [ ] **Step 3: Implement change_form, inlines and submit line**

1. `admin/change_form.html`:
   - Clean form wrapper with error summary banner (`alert alert-error`).
   - Group fieldsets into rounded DaisyUI cards (`card bg-base-100 shadow-sm border border-base-200`).
   - Fieldset titles and descriptions styled as card headers.
   - Form controls styled with DaisyUI (`input input-bordered`, `textarea textarea-bordered`, `select select-bordered`, `checkbox checkbox-primary`).
2. `admin/submit_line.html`:
   - Sticky bottom bar (`sticky bottom-0 z-20 bg-base-100/90 backdrop-blur border-t p-4 flex items-center justify-between`).
   - Save button (`btn btn-primary`), Save and add another (`btn btn-outline`), Save and continue (`btn btn-ghost`), and Delete button (`btn btn-error btn-outline`).
3. `admin/edit_inline/tabular.html` & `stacked.html`:
   - Nested card containers for related objects.
   - Clean "+ Add another" button and styled delete checkbox.

- [ ] **Step 4: Run tests to verify they pass**

```bash
source .venv/bin/activate
pytest tests/test_templates_changeform.py -v
```
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add django_daisy_theme/templates/admin/change_form.html django_daisy_theme/templates/admin/submit_line.html django_daisy_theme/templates/admin/edit_inline/ tests/test_templates_changeform.py
git commit -m "feat: implement change_form fieldsets, inlines, and sticky submit bar"
```

---

### Task 8: Demo Sandbox Project & Live Verification

**Files:**
- Create: `demo/manage.py`
- Create: `demo/demo/__init__.py`
- Create: `demo/demo/settings.py`
- Create: `demo/demo/urls.py`
- Create: `demo/demo/wsgi.py`
- Create: `demo/shop/__init__.py`
- Create: `demo/shop/apps.py`
- Create: `demo/shop/models.py` (Category, Product, Order, OrderItem)
- Create: `demo/shop/admin.py` (CategoryAdmin, ProductAdmin with inlines and filters, OrderAdmin)
- Create: `demo/setup_sample_data.py`
- Test: `tests/test_demo_project.py`

**Interfaces:**
- Consumes: `django_daisy_theme` in `INSTALLED_APPS`.
- Produces: Fully functional demo Django project ready to run with `python manage.py runserver`, loaded with Persian and English test data, for live browser testing and visual verification.

- [ ] **Step 1: Write test to verify demo project initializes and passes system checks**

```python
# tests/test_demo_project.py
import subprocess
import sys

def test_demo_check():
    result = subprocess.run(
        [sys.executable, "demo/manage.py", "check"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"System check failed: {result.stderr}"
```

- [ ] **Step 2: Run test to verify failure**

```bash
source .venv/bin/activate
pytest tests/test_demo_project.py -v
```
Expected: FAIL (demo project does not exist yet)

- [ ] **Step 3: Create demo project, shop app, and sample data script**

1. Create `demo/demo/settings.py`:
   - `INSTALLED_APPS` includes `'django_daisy_theme'`, `'django.contrib.admin'`, ..., `'shop'`.
   - SQLite database configured.
   - `LANGUAGE_CODE = 'fa'` (with toggle to 'en').
   - `DAISY_THEME_CONFIG` sample with customized site title and custom links.
2. Create `demo/shop/models.py`:
   - `Category` (name, slug, is_active).
   - `Product` (category, title, price, stock, is_featured, description, created_at).
   - `Order` (customer_name, status, total_price, created_at).
   - `OrderItem` (order, product, quantity, unit_price).
3. Create `demo/shop/admin.py`:
   - `ProductAdmin` with `list_display`, `list_filter`, `search_fields`, `fieldsets`.
   - `OrderAdmin` with `OrderItemInline` (tabular).
4. Create `demo/setup_sample_data.py`:
   - Migrates database, creates superuser `admin` / `admin1234`.
   - Generates realistic test categories and products in Persian and English.

- [ ] **Step 4: Run database migrations and sample data script**

```bash
source .venv/bin/activate
python demo/manage.py migrate
python demo/setup_sample_data.py
pytest tests/test_demo_project.py -v
```
Expected: PASS

- [ ] **Step 5: Visual and browser verification of all screens**

Run the demo server:
```bash
python demo/manage.py runserver 0.0.0.0:8000
```
Verify:
1. Login page: centered glassmorphism card, inputs, responsive on mobile.
2. Dashboard: stats cards, app cards, recent actions.
3. RTL / LTR: Persian direction and font Vazirmatn; toggle to English and font Inter.
4. DaisyUI theme switcher: toggle between light, dark, emerald, cupcake, etc., stored in localStorage.
5. Change list: table zebra, search, filter drawer, pagination, bulk action bar.
6. Change form: card fieldsets, inlines, sticky save bar.

- [ ] **Step 6: Commit**

```bash
git add demo/ tests/test_demo_project.py
git commit -m "feat: add demo sandbox project with sample shop models and seed data"
```
