jQuery().ready(function($){

  $("#show_all").hide();
  $("#form-btn").hide();

  $(".user_select").click(function(e){
    url = '/register/';
    url += $(this).attr('id');
    url += '/';
    
    $(".user_select").not(this).hide("fast" );
    $("#show_all").show("fast");
    $("#form-btn").show("fast");

    $("#user_form").attr('action', url);
  });

  $("#show_all").click(function(){
    $(".user_select").show("fast");
    $(this).hide("fast");
    $("#form-btn").hide("fast");
  });

});