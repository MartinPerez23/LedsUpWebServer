$(document).ready(function (){
    setInterval(function(){
        if($("#imagenLogo").attr("class") == "logoRojo")
        {
            $("#imagenLogo").attr("class","logoVerde")
        }
        else if($("#imagenLogo").attr("class") == "logoVerde")
        {
            $("#imagenLogo").attr("class","logoAzul")
        }else
        {
            $("#imagenLogo").attr("class","logoRojo")
        }
        
    },1500)
    
});

$(document).ready(function(){
    $('.venobox').venobox(); 
});

