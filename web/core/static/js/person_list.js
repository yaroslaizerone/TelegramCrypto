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
            placeholder: "Выберите пол",
            allowClear: true,
            closeOnSelect: true,
        });
    }
    if (tagSelect.length) {
        tagSelect.select2({
            placeholder: "Выберите тег",
            allowClear: true,
            closeOnSelect: true,
        });
    }
});

$(document).ready(function () {
    const exportExcelButton = $('.btn-export-excel');

    exportExcelButton.on('click', function (event) {
        if ($(this).hasClass('no-export')) {
            event.preventDefault();
            alert('Слишком много данных для экспорта.');
        }
    });
});
