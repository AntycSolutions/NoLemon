var vin;
var id;

jQuery().ready(function($){
	$('.inspection_select').click(function(){
		id = $(this).attr("id");

		if (owner){
			url = "/inspections/" + id + "/";
			window.location = url;
		}

		$('#stripeButton').attr('disabled', 'disabled');
		$('input[name=payment_level]').attr('checked', false);
		$('#inspection_modal').fadeIn("slow");
		$('#inspection_modal').css('pointer-events', 'auto');
		$('input[name=inspection]').attr('value', id);
		$('input[type=radio').hide();
		$('#id_inspection option[value=' + id + ']').prop('selected', true);
		$('#inspection_select_form').trigger('reset');
	});

	$('.close').click(closeModal);

	$('#inspection_modal').keypress(function(e){
		if (e.keyCode == 27) { 
	        $("#inspection_modal").hide(500);
	    }
	});

	$('input[name=payment_level]').on('click', function(e){
		$('#stripeButton').removeAttr('disabled');
		$('li').css('background-color', 'white');
		$(this).parent().parent().css('background-color', "blue");
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
		      $('inspection_select_form').append($('<input type="hidden" name="stripeToken" />').val(token));
		      $('#inspection_select_form').submit();
		    }
		  });
		value = $('input[name=payment_level]:checked', '#inspection_select_form').val(); 

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
	$('input[name=payment_level]:checked').attr('checked', false).checkboxradio("refresh");
	$('#stripeButton').attr('disabled', 'disabled');
}