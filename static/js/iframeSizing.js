$(function() {
        function updateIFrameSize()
        {

        var heightSubstraction = parseInt($('body').css('padding-top').replace(/[^-\d\.]/g, '')) + parseInt($('#top-bar').css('height').replace(/[^-\d\.]/g, ''));  
        var widthSubstraction = parseInt($('.sidebar-nav-fixed').css('width').replace(/[^-\d\.]/g, '')) +30;  

        $('.myModal').css('height', $(window).height()-heightSubstraction+'px'); 
        $('.myModal').css('width', $(window).width()-widthSubstraction+'px'); 
        }

        $(window).resize(function() {
            updateIFrameSize(); 
            });
        $(window).load(function() {
            updateIFrameSize(); 
            });
        });
