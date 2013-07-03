$(document).ready(function () {
    $('#add_column').click(function () {
        clone_field_list('.clonable-col:last');
    });

    $(".removeCol").click(function() {
        $(this).parent('div').parent('div').remove();
    });
});

function clone_field_list(selector) {
    var new_element = $(selector).clone(true);
    var elem_id = new_element.find('select')[0].id;
    var elem_num = parseInt(elem_id.replace(/.*-(\d{1,4})-.*/m, '$1')) + 1;
    new_element.find('select').each(function() {
        var id = $(this).attr('id').replace('-' + (elem_num - 1) + '-', '-' + elem_num + '-');
        $(this).attr({'name': id, 'id': id});
    });
    new_element.find('label').each(function() {
        var new_for = $(this).attr('for').replace('-' + (elem_num - 1) + '-', '-' + elem_num + '-');
        $(this).attr('for', new_for);
        $(this).text($(this).text().replace('#' + (elem_num), '#' + (elem_num+1)));
    });
    $(selector).after(new_element);
}


