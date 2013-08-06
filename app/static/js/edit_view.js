$(document).ready(function () {
    $('#add_column').click(function () {
        clone_field_list('.clonable-col:last', '.clonable-col', '.removeCol');
    });

    $(".removeCol").click(function() {
        var clonable = '.clonable-col';
        var remove = '.removeCol';
        if ($(clonable).size() > 1)
        {
            $(this).parent('div').parent('div').parent(clonable).remove();
            reorder_columns(clonable, remove);

            if ($(clonable).size() == 1)
            {
                $(clonable).find(remove).addClass('disabled');
            }
        }
    });


     $( "#sortable.columns" ).sortable({
placeholder: "ui-state-highlight",
update: function (e, ui) {
            reorder_columns('.clonable-col', '.removeCol');
        }
});

     $( "#sortable.sorters" ).sortable({
placeholder: "ui-state-highlight",
update: function (e, ui) {
            reorder_columns('.clonable-sort', '.removeSort');
        }
});


bind_toggle_filter_options();
reorder_columns('.clonable-col', '.removeCol');
reorder_columns('.clonable-sort', '.removeSort');
});

function clone_field_list(selector, colClass, btnClass) {
    var new_element = $(selector).clone(true);
    $(selector).after(new_element);
    reorder_columns(colClass, btnClass);
}

function reorder_columns(colClass, btnClass) {
    $(colClass).each(function( index )  {
        $(this).find('select').each(function( indexd ) {
            var old_id = $(this).attr('id');
            var old_num = parseInt(old_id.replace(/.*-(\d{1,4})-.*/m, '$1')); 
            var new_id = old_id.replace('-' + (old_num) + '-', '-' + index + '-');
            $(this).attr({'name': new_id, 'id': new_id});
        }); 
        if ($(colClass).size() > 1)
        {
            $(this).find(btnClass).removeClass('disabled');
        }
    });
}

function bind_toggle_filter_options() {
    $('.filter').each(function( index )  {
        $(this).find('select').each(function() {
            update_toggle_filter_options($(this));
            $(this).change(function() {
                update_toggle_filter_options($(this));
            });

        });
    });
}

function update_toggle_filter_options(selector) {
    var value =  selector.val();
    var filter_options = selector.parent().find('.filter_options');
    if (value == 'off' || value == 'hide')
        filter_options.hide();
    else
        filter_options.show();
}


