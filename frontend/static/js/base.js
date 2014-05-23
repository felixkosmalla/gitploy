$(function(){

    // fancy checkbox
    $(".bs-switch").bootstrapSwitch();

    $('.print-printjob').click(function(){
        var me = $(this);

        me.button('loading');

        var print_id = me.attr('data-print-id');

        $.ajax({
            url: Urls.print_printjob(print_id)
        })
        .done(function(e) {
            
            me.button('reset');
            $('tr.printjob-'+print_id).addClass("success");
            
        })
        .fail(function() {
            console.log("error");
        })
        .always(function() {
            console.log("complete");
        });
        

        // alert(print_id);
    });


    

});