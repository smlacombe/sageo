$(document).ready(function () {
    $('#add_column').click(function () {
        clone_field_list('.clonable-col:last');
    });

    $(".removeCol").click(function() {
        if ($('.clonable-col').size() > 1)
        {
            $(this).parent('div').parent('div').parent('.clonable-col').remove();
            reorder_columns();

            if ($('.clonable-col').size() == 1)
            {
                $('.clonable-col').find('.removeCol').addClass('disabled');
            }
        }
    });

     $( "#sortable" ).sortable({
placeholder: "ui-state-highlight",
update: function (e, ui) {
           reorder_columns() 
        }
});

bind_toggle_filter_options();

});

function clone_field_list(selector) {
    var new_element = $(selector).clone(true);
    $(selector).after(new_element);
    reorder_columns();
}

function reorder_columns() {
    $('.clonable-col').each(function( index )  {
        var selectCol = $(this).find('select');
        var labelCol = $(this).find('label');
        
        var old_id = selectCol.attr('id');
        var old_num = parseInt(old_id.replace(/.*-(\d{1,4})-.*/m, '$1')); 

        var new_id = old_id.replace('-' + (old_num) + '-', '-' + index + '-');
        selectCol.attr({'name': new_id, 'id': new_id});
        labelCol.attr('for', new_id);
        
        if ($('.clonable-col').size() > 1)
        {
            $(this).find('.removeCol').removeClass('disabled');
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


