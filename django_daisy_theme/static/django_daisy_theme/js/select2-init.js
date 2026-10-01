(function () {
  'use strict';

  function initSelect2(context) {
    if (typeof django === 'undefined' || !django.jQuery || !django.jQuery.fn.select2) {
      return;
    }
    const $ = django.jQuery;
    const isRtl = document.documentElement.getAttribute('dir') === 'rtl';
    const lang = document.documentElement.getAttribute('lang') || 'en';

    const $root = context ? $(context) : $(document);

    // Target select elements
    $root.find('select').each(function () {
      const $select = $(this);

      // Skip already initialized selects
      if ($select.hasClass('select2-hidden-accessible')) {
        return;
      }

      // Skip Django's built-in AJAX autocomplete fields (handled by autocomplete.js)
      if ($select.hasClass('admin-autocomplete')) {
        return;
      }

      // Skip empty form templates in formsets
      if ($select.closest('.empty-form').length) {
        return;
      }

      // Skip calendar and clock popup selects
      if ($select.closest('.calendarbox, .clockbox, #calendarbox0, #clockbox0').length) {
        return;
      }

      // Skip specifically excluded selects
      if ($select.hasClass('no-select2') || $select.data('no-select2')) {
        return;
      }

      // Check for empty placeholder option
      const hasEmptyOption = $select.find('option[value=""]').length > 0;
      const isMultiple = $select.prop('multiple');

      try {
        $select.select2({
          dir: isRtl ? 'rtl' : 'ltr',
          language: lang.startsWith('fa') ? 'fa' : 'en',
          width: '100%',
          dropdownAutoWidth: true,
          allowClear: hasEmptyOption && !isMultiple,
          placeholder: hasEmptyOption ? ($select.find('option[value=""]').text() || '---') : undefined,
          minimumResultsForSearch: 0 // Always show search box
        });
      } catch (err) {
        console.warn('Select2 init failed for element:', this, err);
      }
    });
  }

  // Run on DOM ready
  document.addEventListener('DOMContentLoaded', function () {
    if (window.django && window.django.jQuery) {
      initSelect2();

      // Listen for dynamically added inlines (Tabular / Stacked)
      window.django.jQuery(document).on('formset:added', function (event, $row) {
        initSelect2($row);
      });
    }
  });

  // Global helper for manual re-init if needed
  window.initDaisySelect2 = initSelect2;
})();
