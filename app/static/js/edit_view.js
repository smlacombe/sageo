LI_CLASS_NAME = '.clonable-row';
REMOVE_CLASS_NAME = '.removeRow';
ADD_ROW_CLASS_NAME = '.add_row';
UL_CLASS_NAME = '.sortable.clonable';

$(document).ready(function () {
    $(ADD_ROW_CLASS_NAME).click(function () {
        var currentUl = $(this).siblings(UL_CLASS_NAME);
        clone_field_list(currentUl);
    });

    $(REMOVE_CLASS_NAME).click(function() {
        if ($(this).closest(UL_CLASS_NAME).find(LI_CLASS_NAME).size() > 1)
        {
            var currentLi = $(this).closest(LI_CLASS_NAME);
            var currentUl = currentLi.closest(UL_CLASS_NAME);
            currentLi.remove();
            
            reorder_columns(currentUl);

            if (currentUl.find(LI_CLASS_NAME).size() == 1)
            {
                currentUl.find(LI_CLASS_NAME).find(REMOVE_CLASS_NAME).addClass('disabled');
            }
        }
    });


     $(UL_CLASS_NAME).sortable({
    placeholder: "ui-state-highlight",
    update: function (e, ui) {
                reorder_columns($(this));
        }
    });

    bind_toggle_filter_options();
    $(UL_CLASS_NAME).each(function () {
        reorder_columns($(this));
    });
});

function clone_field_list(currentUl) {
    var clonable = currentUl.find(LI_CLASS_NAME).last()
    var new_element = clonable.clone(true);
    clonable.after(new_element);
    reorder_columns(currentUl);
}

function reorder_columns(currentUl) {
    currentUl.find(LI_CLASS_NAME).each(function( index )  {
        $(this).find('select').each(function( indexd ) {
            var old_id = $(this).attr('id');
            var old_num = parseInt(old_id.replace(/.*-(\d{1,4})-.*/m, '$1')); 
            var new_id = old_id.replace('-' + (old_num) + '-', '-' + index + '-');
            $(this).attr({'name': new_id, 'id': new_id});
        }); 

        if (currentUl.find(LI_CLASS_NAME).size() > 1)
        {
            $(this).find(REMOVE_CLASS_NAME).removeClass('disabled');
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


