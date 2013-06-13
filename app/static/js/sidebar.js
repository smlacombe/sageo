$(function() {
        $( ".column" ).sortable({
connectWith: ".column"
});
        $( ".portlet" ).addClass( "ui-widget ui-widget-content ui-helper-clearfix ui-corner-all" )
        .find( ".portlet-header" )
        .addClass( "ui-widget-header ui-corner-all" )
        .prepend( "<span class='ui-icon toggle ui-icon-minusthick'></span>")
        .prepend( "<span class='ui-icon ui-icon-close'></span>")
        .end()
        .find( ".portlet-content" );
        $( ".portlet-header .toggle" ).click(function() {
            $( this ).toggleClass( "ui-icon-minusthick" ).toggleClass( "ui-icon-plusthick" );
            $( this ).parents( ".portlet:first" ).find( ".portlet-content" ).toggle();
            });

        $( ".portlet-header .ui-icon-close" ).click(function() {
            $( this ).parents( ".portlet:first" ).hide();
            });
        $( ".column" ).disableSelection();
        });
