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

  // Intercept and replace Django's SelectFilter (filter_horizontal / filter_vertical)
  // so that ManyToMany fields become modern Select2 multi-selects with search tags.
  function setupSelectFilterInterceptor() {
    var customSelectFilter = {
      init: function (field_id, field_name, is_stacked) {
        var $ = getJQuery();
        if (!$) return;
        var $select = $('#' + field_id);
        if (!$select.length) return;

        // Clean legacy classes
        $select.removeClass('selectfilter selectfilterstacked filtered');
        $select.prop('multiple', true);

        // Remove any old selector container if already rendered
        var $selector = $select.closest('.selector');
        if ($selector.length) {
          $selector.replaceWith($select);
        }

        var isRtl = document.documentElement.getAttribute('dir') === 'rtl';
        var lang = document.documentElement.getAttribute('lang') || 'en';
        var placeholder = field_name
          ? (isRtl ? 'انتخاب ' + field_name + '...' : 'Select ' + field_name + '...')
          : (isRtl ? 'انتخاب موارد...' : 'Select options...');

        $select.select2({
          dir: isRtl ? 'rtl' : 'ltr',
          language: lang.startsWith('fa') ? 'fa' : 'en',
          width: '100%',
          placeholder: placeholder,
          closeOnSelect: false
        });
      }
    };

    window.SelectFilter = customSelectFilter;
  }

  // Dismantle any legacy dual-listboxes already created by SelectFilter2.js
  function dismantleLegacySelectors() {
    var $ = getJQuery();
    if (!$) return;

    $('.selector').each(function () {
      var $selector = $(this);
      var $from = $selector.find('select[id$="_from"]');
      var $to = $selector.find('select[id$="_to"]');
      if ($from.length && $to.length) {
        var baseId = $from.attr('id').replace(/_from$/, '');
        var fieldName = $from.data('fieldName') || $to.data('fieldName') || '';
        var name = $to.attr('name') || $from.attr('name').replace(/_old$/, '');

        // Collect all options with their selected states
        var optionsHtml = '';
        $from.find('option').each(function () {
          optionsHtml += '<option value="' + $(this).val() + '">' + $(this).text() + '</option>';
        });
        $to.find('option').each(function () {
          optionsHtml += '<option value="' + $(this).val() + '" selected>' + $(this).text() + '</option>';
        });

        var $newSelect = $('<select multiple name="' + name + '" id="' + baseId + '" class="w-full">' + optionsHtml + '</select>');
        $selector.replaceWith($newSelect);

        var isRtl = document.documentElement.getAttribute('dir') === 'rtl';
        var lang = document.documentElement.getAttribute('lang') || 'en';
        var placeholder = fieldName
          ? (isRtl ? 'انتخاب ' + fieldName + '...' : 'Select ' + fieldName + '...')
          : (isRtl ? 'انتخاب موارد...' : 'Select options...');

        $newSelect.select2({
          dir: isRtl ? 'rtl' : 'ltr',
          language: lang.startsWith('fa') ? 'fa' : 'en',
          width: '100%',
          placeholder: placeholder,
          closeOnSelect: false
        });
      }
    });
  }

  function initSelect2(context) {
    var $ = getJQuery();
    if (!$) {
      return;
    }
    var isRtl = document.documentElement.getAttribute('dir') === 'rtl';
    var lang = document.documentElement.getAttribute('lang') || 'en';

    var $root = context ? $(context) : $(document);

    // Target select elements
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

      // Skip internal selects of .selector if not yet dismantled
      if ($select.closest('.selector').length) {
        return;
      }

      var isMultiple = $select.prop('multiple');
      var hasEmptyOption = $select.find('option[value=""]').length > 0;
      var fieldName = $select.data('fieldName') || $select.attr('data-field-name') || '';

      try {
        var options = {
          dir: isRtl ? 'rtl' : 'ltr',
          language: lang.startsWith('fa') ? 'fa' : 'en',
          width: '100%',
          dropdownAutoWidth: false,
          minimumResultsForSearch: 0,
          closeOnSelect: !isMultiple
        };

        if (isMultiple) {
          options.placeholder = $select.data('placeholder') || (fieldName ? (isRtl ? 'انتخاب ' + fieldName + '...' : 'Select ' + fieldName + '...') : (isRtl ? 'انتخاب موارد...' : 'Select options...'));
        } else if (hasEmptyOption) {
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
    setupSelectFilterInterceptor();
    dismantleLegacySelectors();
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
  setupSelectFilterInterceptor();
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run);
  } else {
    run();
  }
  window.addEventListener('load', run);
  setTimeout(run, 50);
  setTimeout(run, 200);
  setTimeout(run, 600);

  // Global helper for manual re-init if needed
  window.initDaisySelect2 = initSelect2;
  window.dismantleLegacySelectors = dismantleLegacySelectors;
})();
