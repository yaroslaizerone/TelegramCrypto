$(document).ready(function () {
// Раскрытие/скрытие блоков с датами использования данных
    $('.usage-wrapper').click(function () {
        $(this).find('.more').toggle();
    });
// Обновление ссылки на экспорт при изменении флажков выбора колонок
    $('.column-checkbox').change(function () {
        let queryParams = new URLSearchParams(window.location.search);
        queryParams.delete('columns');

        $('.column-checkbox:checked').each(function () {
            queryParams.append('columns', $(this).val());
        });

        const newUrl = window.location.pathname + '?' + queryParams.toString() + '&export=excel';
        $('.btn-export-excel').attr('href', newUrl);
    });

// Инициализация выпадающих списков с помощью плагина Select2
    const regionSelect = $("#id_region");
    const utcSelect = $("#id_utc");
    const genderSelect = $("#id_gender");
    const tagSelect = $("#id_tag");
    const statusSelect = $("#id_status");


    if (regionSelect.length) {
        regionSelect.select2({
            placeholder: "Выберите регион",
            allowClear: true,
            multiple: true,
            closeOnSelect: true,
        });
    }
    if (utcSelect.length) {
        utcSelect.select2({
            placeholder: "Выберите часовой пояс",
            allowClear: true,
            multiple: true,
            closeOnSelect: true,
        });
    }
    if (genderSelect.length) {
        genderSelect.select2({
            placeholder: "Пол",
            allowClear: true,
            closeOnSelect: true,
        });
    }
    if (tagSelect.length) {
        tagSelect.select2({
            placeholder: "Тег",
            allowClear: true,
            closeOnSelect: true,
        });
    }
    if (statusSelect.length) {
        statusSelect.select2({
            placeholder: "Статус",
            allowClear: true,
            closeOnSelect: true,
        });
    }
});

$(document).ready(function () {
  const exportExcelButtons = $('.btn-export-excel');

  exportExcelButtons.each(function () {
    if ($(this).hasClass('no-export')) {
      $(this).prop('disabled', true).addClass('disabled');
    }
  });
});


$(document).ready(function() {
  $('[data-toggle="tooltip"]').tooltip({
    show: { delay: 0 }
  });
});

$(document).ready(function() {
  $("#merge_fio").on("click", function() {
    const isChecked = $(this).prop("checked");
    const link = $(".btn-export-excel");
    const url = new URL(link.attr("href"), window.location.href);

    if (isChecked) {
      url.searchParams.set("merge_fio", "1");
    } else {
      url.searchParams.delete("merge_fio");
    }

    link.attr("href", url.toString());
  });
});

$(document).ready(function() {
  $(".btn-export-excel").one("click", function() {
    const link = $(this);
    const url = new URL(link.attr("href"), window.location.href);

    link.prop("disabled", true).addClass("disabled").attr("href", url.toString());
  });
});

