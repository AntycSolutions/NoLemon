var vin;

jQuery().ready(function($){
	$('.inspection_select').click(function(){
		$('#stripeButton').attr('disabled', 'disabled');
		$('input[name=option]').attr('checked', false);
		$('#inspection_modal').fadeIn("slow");
		$('#inspection_modal').css('pointer-events', 'auto');

		if (owner){
			url = "/inspections/" + $(this).attr("id") + "/";
			window.location = url;
		}

	});

	$('.close').click(closeModal);

	$('#inspection_modal').keypress(function(e){
		if (e.keyCode == 27) { 
	        $("#inspection_modal").hide(500);
	    }
	});

	$('input[name=option]').on('click', function(e){
		$('#stripeButton').removeAttr('disabled');
	});

	$('#stripeButton').click(function(e){
		var handler = StripeCheckout.configure({
		    key: 'pk_test_3aCn8J9IdHtqTUaCMWrABmQI',
		    image: image,
		    name: 'Inspection Type',
		    panelLabel: 'Pay',
		    token: function(token) {
		      // Use the token to create the charge with a server-side script.
		      // You can access the token ID with `token.id`
		    }
		  });
		value = $('input[name=option]:checked', '#inspection_select_form').val(); 

		var amount;
		var description;
		switch(value){
			case '1':
				amount = option1;
				description = "NoLemon Report";
				break;
			case '2':
				amount = option2;
				description = "Expert Car Condition Inspection Report and Video";
				break;
			case '3':
				amount = option3;
				description = "NoLemon + Expert Car Condition Inspection Report and Video (Value Pack)";
				break;
			default:
				alert('Something goofed');
				break;
		}
		handler.open({
	      description: description,
	      amount: amount
	    });
	    e.preventDefault();

	    $('#inspection_modal').fadeOut("slow");
	    $('#inspection_modal').css('pointer-events', 'none');
	});

});

closeModal = function () {
	$('#inspection_modal').fadeOut("slow");
	$('#inspection_modal').css('pointer-events', 'none');
	$('input[name=option]:checked').attr('checked', false).checkboxradio("refresh");
	$('#stripeButton').attr('disabled', 'disabled');
}