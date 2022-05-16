
$(document).ready( function()
{
    $("#logo").hide();
    $(".btn-danger").hide();
    

   
    $("#logo").show(3000);
    $(".btn-danger").show(3000);

    $("#sell").hide();
    $("#rent").hide();
    $("#radio1, #radio2").change(function () {
        if ($("#radio1").is(":checked")) {
            $('#sell').show();
            $("#rent").hide();
        }
        else if ($("#radio2").is(":checked")) {
            $('#rent').show();
            $("#sell").hide();
        }

    });


})