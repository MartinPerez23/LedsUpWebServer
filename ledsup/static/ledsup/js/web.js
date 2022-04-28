$(document).ready(function (){
    setInterval(function(){
        if($("#imagenLogo").attr("class") === "logoRojo d-inline-block align-text-top")
        {
            $("#imagenLogo").attr("class","logoVerde d-inline-block align-text-top")
        }
        else if($("#imagenLogo").attr("class") === "logoVerde d-inline-block align-text-top")
        {
            $("#imagenLogo").attr("class","logoAzul d-inline-block align-text-top")
        }else
        {
            $("#imagenLogo").attr("class","logoRojo d-inline-block align-text-top")
        }

    },1500)

});

$(document).ready(function(){
    $('.venobox').venobox();
});

