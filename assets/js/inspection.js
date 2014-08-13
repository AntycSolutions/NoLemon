var vin;

jQuery().ready(function($){
	$('.inspection_select').click(function(){
		$('#inspection_modal').show();
		$('#inspection_modal').css('pointer-events', 'auto');
	});

	$('.close').click(function(){
		$('#inspection_modal').hide();
		$('#inspection_modal').css('pointer-events', 'none');
	});

	$('#inspection_modal').keypress(function(e){
		if (e.keyCode == 27) { 
	        $("#inspection_modal").hide(500);
	    }
	});
});