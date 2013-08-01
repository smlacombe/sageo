$(document).ready(function () {
    $('#filters_button').click(function () {
        bind_toggle_filter_panel();
    });
});

function bind_toggle_filter_panel() {
    $('#filters-panel').toggle(); 
}

