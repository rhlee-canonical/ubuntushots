/*
Define a Javascript function to set up handlers and plugins. It is called when the
page is loaded and upon every AJAX subrequest.
*/
function inithandlers() {
    /*
    ## Bug: Thumbnails of different sizes don't get centered properly.
    ## Bug: After a cycle animation occured and another thumbnail is currently displayed
    ##      then when clicking on the full-size screenshot it does not just shrink but move
    ##      to the top left position of the browser window. Probably because its reference
    ##      thumbnail image is currently not displayed or something.
    ##
    ## Use 'cycle' plugin to rotate thumbnails if multiple exist for one package.
    */
    $("div.screenshots").filter( function () {
        return $(this).find("img").length>1;
    }).cycle({
	    fx: 'fade',
            timeout: 3000,
            speed: 500
	});

    /*
    ## Use the 'quicksand' jQuery plugin to smoothly change from one page of displayed
    ## thumbnails to another. See also: http://razorjack.net/quicksand/demos/ajax.html
    ##$('#load-webbies a.button').click(function(e) {
    ##  $.get( $(this).attr('href'), function(data) {
    ##      $('.webbies').quicksand( $(data).find('li'), { adjustHeight: 'dynamic' } );
    ##  });
    ##  e.preventDefault();
    ##});
    */

    // Flyout shows the large screenshots when clicking on the thumbnails
    $('.screenshots a.image').flyout({
        loadingSrc:'/images/spinner.gif',
        outSpeed: 300,
        inSpeed: 300
    });


    // Add tooltip behavior to IMG with class 'tooltip'
        $(document).ready(function() {
            $('.tooltip').tooltip({
                showURL: false,
                fade: 150
            });
        });
};
