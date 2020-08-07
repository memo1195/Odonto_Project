$(document).ready(function() {

//  Pasar datos del form al modal 
$("#button-modal").click(function(){
    //  Nombre
    let namef1 = document.getElementById("namef1");
    let namef2 = document.getElementById("nombre_paciente");
    namef2.value = namef1.value;

    //  Tratamiento
    let t1 = document.getElementById("treatf1");
    let t2 = document.getElementById("tratamiento");
    t2.value = t1.value;
});

});