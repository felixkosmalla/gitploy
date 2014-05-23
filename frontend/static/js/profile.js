$(function(){



	var timer = false;
	var running = false;
	var delay =200;



	function set_valid(css_class, valid){

		if(valid){
			$(css_class).addClass('has-success');
			$(css_class).removeClass('has-error');


			$(css_class+" .field-valid").show();
			$(css_class+" .field-not-valid").hide();

		}else{
			$(css_class).addClass('has-error');
			$(css_class).removeClass('has-success');

			$(css_class+" .field-valid").hide();
			$(css_class+" .field-not-valid").show();
		}

	}


	function tokenRequest(){
		var token = $('#gitlab_access_token').val();

		$.post(Urls.validate_token(), {'token':token}, function(res){
			running = false;

			if(res == "1"){
				set_valid('#gitlab_token_group',true);
			}else{
				set_valid('#gitlab_token_group',false);
			}

			
			


		});
	}

	function validateToken(){

		if(timer != false){
			clearTimeout(timer);
			running = false;
		}


		if(!running){
			running = true;

			
			timer = setTimeout(tokenRequest, delay);

		}

	}

	tokenRequest();

	$('#gitlab_access_token').keyup(validateToken);



});