<?php 

/*--------------------------------------------------------------------------------*/
$emailTo            =  'test@test.com';
$subject            =  'sample Subject form';
$nameError          =  'Please enter your name.';
$emailError         =  'Please enter your email address.';
$emailInvalidError  =  'You entered an invalid email address.';
$commentError       =  'Please enter a message.';
$alertMessage       =  'Please fill in all the fields correctly.';
$successMessage     =  'Thank you, your email was sent successfully.'; 
/*--------------------------------------------------------------------------------*/


if(isset($_REQUEST['submitted'])) {
    $error_flag = FALSE;
    $error_msg  = array();
    
    if(trim($_REQUEST['contactName']) === '') {
        $error_flag     = TRUE;
        $error_msg[]    = array(
            'key'       => 'contactName',
            'message'   => $nameError
        );
    } else {
            $name = trim($_REQUEST['contactName']);
    }
		
    if(trim($_REQUEST['email']) === '')  {
        $error_flag     = TRUE;
        $error_msg[]    = array(
            'key'       => 'email',
            'message'   => $emailError
        );
    } else if (!eregi("^[A-Z0-9._%-]+@[A-Z0-9._%-]+\.[A-Z]{2,4}$", trim($_REQUEST['email']))) {
        $error_flag     = TRUE;
        $error_msg[]    = array(
            'key'       => 'email',
            'message'   => $emailInvalidError
        );
    } else {
        $email = trim($_REQUEST['email']);
    }
			
    if(trim($_REQUEST['comments']) === '') {
        $error_flag     = TRUE;
        $error_msg[]    = array(
            'key'       => 'comments',
            'message'   => $commentError
        );
    } else {
        if(function_exists('stripslashes')) {
            $comments = stripslashes(trim($_REQUEST['comments']));
        } else {
            $comments = trim($_REQUEST['comments']);
        }
    }
			
    if(!$error_flag) {
        
        $body       = "Name: $name \n\nEmail: $email \n\nComments: $comments";
        $headers    = 'From: '.$name.' <'.$email.'>' . "\r\n" . 'Reply-To: ' . $email;
        
        mail($emailTo, $subject, $body, $headers);
        ?>
        <script type="text/javascript">
            jQuery('#messageDiv').html('<?PHP echo $successMessage; ?>').removeClass().addClass('alert alert-success');
            jQuery('input[type=text],textarea').val('');
            jQuery('.error_lbl').html('').hide();
            jQuery('.dis_lbl').show();
        </script>
        <?PHP
    }else{
        ?>
        <script type="text/javascript">
            jQuery('#messageDiv').html('<?PHP echo $alertMessage; ?>').removeClass().addClass('alert alert-danger');
            error_obj = <?PHP echo json_encode($error_msg); ?>;
            for(i=0;i<error_obj.length;i++){
                jQuery('#'+error_obj[i].key+'Ct').find('.dis_lbl').hide();
                jQuery('#'+error_obj[i].key+'Ct').find('.error_lbl').html(error_obj[i].message).show();
            }
        </script>
        <?PHP
    }
	
} ?>
