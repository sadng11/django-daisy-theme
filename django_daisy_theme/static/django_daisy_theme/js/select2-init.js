(function () {
  'use strict';

  function getJQuery() {
    if (typeof window.django !== 'undefined' && window.django.jQuery && window.django.jQuery.fn && window.django.jQuery.fn.select2) {
      return window.django.jQuery;
    }
    if (typeof window.jQuery !== 'undefined' && window.jQuery.fn && window.jQuery.fn.select2) {
      return window.jQuery;
    }
    if (typeof window.$ !== 'undefined' && window.$.fn && window.$.fn.select2) {
      return window.$;
    }
    return null;
  }

  function initSelect2(context) {
    var $ = getJQuery();
    if (!$) {
      return;
    }
    var isRtl = document.documentElement.getAttribute('dir') === 'rtl';
    var lang = document.documentElement.getAttribute('lang') || 'en';

    var $root = context ? $(context) : $(document);

    // Target all select elements
    $root.find('select').each(function () {
      var $select = $(this);

      // Skip already initialized selects
      if ($select.hasClass('select2-hidden-accessible')) {
        return;
      }

      // Skip Django AJAX autocomplete fields (handled by autocomplete.js)
      if ($select.hasClass('admin-autocomplete')) {
        return;
      }

      // Skip empty form templates in formsets (Django inlines clone template)
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
      var hasEmptyOption = $select.find('option[value=""]').length > 0;
      var isMultiple = $select.prop('multiple');

      try {
        var options = {
          dir: isRtl ? 'rtl' : 'ltr',
          language: lang.startsWith('fa') ? 'fa' : 'en',
          width: '100%',
          dropdownAutoWidth: true,
          minimumResultsForSearch: 0 // Always enable search box
        };

        if (hasEmptyOption && !isMultiple) {
          options.allowClear = true;
          options.placeholder = $select.find('option[value=""]').text() || '---';
        }

        $select.select2(options);
      } catch (err) {
        console.error('Select2 initialization error on:', this, err);
      }
    });
  }

  function run() {
    initSelect2();

    var $ = getJQuery();
    if ($) {
      // Listen for dynamically added inlines (Tabular / Stacked)
      $(document).off('formset:added.daisySelect2').on('formset:added.daisySelect2', function (event, $row) {
        setTimeout(function () {
          initSelect2($row);
        }, 50);
      });
    }
  }

  // Execute immediately, on DOM ready, on load, and with brief retry
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run);
  } else {
    run();
  }
  window.addEventListener('load', run);
  setTimeout(run, 150);
  setTimeout(run, 500);

  // Global helper for manual re-init if needed
  window.initDaisySelect2 = initSelect2;
})();
