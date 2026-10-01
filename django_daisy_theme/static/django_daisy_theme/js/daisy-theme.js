/**
 * django-daisy-theme Client Runtime
 * Powered by Alpine.js & DaisyUI
 */

function registerDaisyAdmin() {
  if (typeof Alpine !== 'undefined') {
    Alpine.data('daisyAdmin', (defaultTheme = 'light', darkTheme = 'dark') => ({
      currentTheme: defaultTheme,
      darkTheme: darkTheme,
      drawerOpen: false,
      filterDrawerOpen: false,
      searchModalOpen: false,
      selectedItemsCount: 0,

    init() {
      // Restore theme preference
      const savedTheme = localStorage.getItem('daisy_admin_theme');
      if (savedTheme) {
        this.currentTheme = savedTheme;
      } else {
        const rootTheme = document.documentElement.getAttribute('data-theme');
        if (rootTheme) {
          this.currentTheme = rootTheme;
        }
      }
      this.applyTheme(this.currentTheme);

      // Listen for system theme change if needed
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('daisy_admin_theme')) {
          this.setTheme(e.matches ? this.darkTheme : 'light');
        }
      });

      this.updateSelectedCount();
    },

    setTheme(theme) {
      this.currentTheme = theme;
      localStorage.setItem('daisy_admin_theme', theme);
      this.applyTheme(theme);
    },

    toggleDarkLight() {
      const isDark = this.currentTheme === this.darkTheme || this.currentTheme === 'dark';
      this.setTheme(isDark ? 'light' : this.darkTheme);
    },

    applyTheme(theme) {
      document.documentElement.setAttribute('data-theme', theme);
    },

    toggleDrawer() {
      this.drawerOpen = !this.drawerOpen;
    },

    toggleFilterDrawer() {
      this.filterDrawerOpen = !this.filterDrawerOpen;
    },

    openSearchModal() {
      this.searchModalOpen = true;
    },

    closeSearchModal() {
      this.searchModalOpen = false;
    },

    // Bulk selection helper for Django change_list table
    toggleSelectAll(event) {
      const checked = event.target.checked;
      const checkboxes = document.querySelectorAll('input.action-select');
      checkboxes.forEach((cb) => {
        cb.checked = checked;
      });
      this.updateSelectedCount();
    },

    updateSelectedCount() {
      const selected = document.querySelectorAll('input.action-select:checked');
      this.selectedItemsCount = selected.length;
    },
  }));
  }
}

if (typeof Alpine !== 'undefined') {
  registerDaisyAdmin();
} else {
  document.addEventListener('alpine:init', registerDaisyAdmin);
}

// Immediate theme execution to prevent dark mode flash
(function () {
  const saved = localStorage.getItem('daisy_admin_theme');
  if (saved) {
    document.documentElement.setAttribute('data-theme', saved);
  }
})();
