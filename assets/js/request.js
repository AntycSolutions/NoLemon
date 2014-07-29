jQuery().ready(function($){

  $("#show_all").hide();
  $('.stripe-button').hide();

  $(".mechanic_li").click(function(){
    mech = $(this).find('#mech_id').text();
    $(".mechanic_li").not(this).hide("fast" );
    $("#show_all").show("fast");
    $("#id_mechanic").val(mech).trigger('change');
    $('.stripe-button').show("fast");
  });

  $("#show_all").click(function(){
    $(".mechanic_li").show("fast");
    $(this).hide("fast");
    $('.stripe-button').hide("fast");
  });

});