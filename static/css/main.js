"use strict";
function scroll_to_class(element_class, removed_height) {
	var scroll_to = $(element_class).offset().top - removed_height;
	if($(window).scrollTop() != scroll_to) {
		$('.form-wizard').stop().animate({scrollTop: scroll_to}, 0);
	}
}
function checkRange() {
    var tempK_text = document.getElementById("tempK_text")
    var tempC_text = document.getElementById("tempC_text")
    var fouling_factor = document.getElementById("fouling")
    if (tempC_text?.value < 10) {
        alert("Temperature of permeate should be greater than 10°C/283K")
        return false;
    }
    if (tempC_text?.value > 35) {
        alert("Temperature of permeate should be less than 35°C/308K")
        return false;
        
    }
    if (fouling_factor?.value > 1) {
        alert("Fouling factor should be less than 1")
        return false;
    }
    if (fouling_factor?.value < 0) {
        alert("Fouling factor should be greater than 0")
        return false;
    }
    
    return true;
}
function checkRange2() {
    if (document.getElementById("waterConc")?.value > 50000) {
        alert("Feed Water Conc should be less than 50,000 mg/l")
        return false;
    }
    if (document.getElementById("waterConc")?.value < 250) {
        alert("Feed Water Conc should be greater than 250 mg/l")
        return false;
    }
    if (document.getElementById("flowRate")?.value > 5) {
        alert("Flow Rate should be less than 5 m^3/s")
        return false;
    }
    console.log(document.getElementById("flowRate").value)
    if (document.getElementById("flowRate")?.value < 0) {
        alert("Flow Rate should be greater than 0")
        return false;
    }
    return true;
}

function bar_progress(progress_line_object, direction) {
	var number_of_steps = progress_line_object.data('number-of-steps');
	var now_value = progress_line_object.data('now-value');
	var new_value = 0;
	if(direction == 'right') {
		new_value = now_value + ( 100 / number_of_steps );
	}
	else if(direction == 'left') {
		new_value = now_value - ( 100 / number_of_steps );
	}
	progress_line_object.attr('style', 'width: ' + new_value + '%;').data('now-value', new_value);
}

jQuery(document).ready(function() {
    
    /*
        Form
    */
    $('.form-wizard fieldset:first').fadeIn('slow');
    
    $('.form-wizard .required').on('focus', function() {
    	$(this).removeClass('input-error');
    });
    
    // next step
    $('.form-wizard .btn-next').on('click', function() {
    	var parent_fieldset = $(this).parents('fieldset');
    	var next_step = true;
    	// navigation steps / progress steps
    	var current_active_step = $(this).parents('.form-wizard').find('.form-wizard-step.active');
    	var progress_line = $(this).parents('.form-wizard').find('.form-wizard-progress-line');
    	
    	// fields validation
    	parent_fieldset.find('.required').each(function() {
    		if( $(this).val() == "" ) {
    			$(this).addClass('input-error');
    			next_step = false;
    		}
    		else {
    			$(this).removeClass('input-error');
    		}
    	});
    	// fields validation
        
    	
        if (next_step && checkRange() && checkRange2()) {
            console.log(checkRange())
           
            parent_fieldset.fadeOut(400, function () {
                    // change icons
                    current_active_step.removeClass('active').addClass('activated').next().addClass('active');
                    // progress bar
                    bar_progress(progress_line, 'right');
                    // show next step
                
                    $(this).next().fadeIn();
                    // scroll window to beginning of the form
                    scroll_to_class($('.form-wizard'), 20);
                
                });
            
    	}
    	
    });
    
    // previous step
    $('.form-wizard .btn-previous').on('click', function() {
    	// navigation steps / progress steps
    	var current_active_step = $(this).parents('.form-wizard').find('.form-wizard-step.active');
    	var progress_line = $(this).parents('.form-wizard').find('.form-wizard-progress-line');
    	
    	$(this).parents('fieldset').fadeOut(400, function() {
    		// change icons
    		current_active_step.removeClass('active').prev().removeClass('activated').addClass('active');
    		// progress bar
    		bar_progress(progress_line, 'left');
    		// show previous step
    		$(this).prev().fadeIn();
    		// scroll window to beginning of the form
			scroll_to_class( $('.form-wizard'), 20 );
    	});
    });
    
    // submit
    $('.form-wizard').on('submit', function(e) {
    	
    	// fields validation
    	$(this).find('.required').each(function() {
    		if( $(this).val() == "" ) {
    			e.preventDefault();
    			$(this).addClass('input-error');
    		}
    		else {
    			$(this).removeClass('input-error');
    		}
    	});
    	// fields validation
    	
    });
    
    
});





// image uploader scripts 

var $dropzone = $('.image_picker'),
    $droptarget = $('.drop_target'),
    $dropinput = $('#inputFile'),
    $dropimg = $('.image_preview'),
    $remover = $('[data-action="remove_current_image"]');

$dropzone.on('dragover', function() {
  $droptarget.addClass('dropping');
  return false;
});

$dropzone.on('dragend dragleave', function() {
  $droptarget.removeClass('dropping');
  return false;
});

$dropzone.on('drop', function(e) {
  $droptarget.removeClass('dropping');
  $droptarget.addClass('dropped');
  $remover.removeClass('disabled');
  e.preventDefault();
  
  var file = e.originalEvent.dataTransfer.files[0],
      reader = new FileReader();

  reader.onload = function(event) {
    $dropimg.css('background-image', 'url(' + event.target.result + ')');
  };
  
  console.log(file);
  reader.readAsDataURL(file);

  return false;
});

$dropinput.change(function(e) {
  $droptarget.addClass('dropped');
  $remover.removeClass('disabled');
  $('.image_title input').val('');
  
  var file = $dropinput.get(0).files[0],
      reader = new FileReader();
  
  reader.onload = function(event) {
    $dropimg.css('background-image', 'url(' + event.target.result + ')');
  }
  
  reader.readAsDataURL(file);
});

$remover.on('click', function() {
  $dropimg.css('background-image', '');
  $droptarget.removeClass('dropped');
  $remover.addClass('disabled');
  $('.image_title input').val('');
});

$('.image_title input').blur(function() {
  if ($(this).val() != '') {
    $droptarget.removeClass('dropped');
  }
});


var slider = document.getElementById("range-slider__range");
console.log(slider)
var output = document.getElementById("range-slider__value");
console.log(output)
output.innerHTML = slider.value;

// This function input current value in span and add progress colour in range
slider.oninput = function() {

  output.innerHTML = this.value;

  var value = (this.value-this.min)/(this.max-this.min)*100;
  
  this.style.background = 'linear-gradient(to right,#db1818 0%, #db1818 ' + value + '%, #d7dcdf ' + value + '%, #d7dcdf 100%)'
}
  
// console.log(document.getElementById(temp).checked)


function enable_tempC() {
    var temp=document.getElementById("temp")
    var tempK_text = document.getElementById("tempK_text")
    var tempC_text = document.getElementById("tempC_text")


    // console.log(temp.checked);
    // console.log(tempK.checked);
    tempC_text.disabled = temp.checked ? false : true;
    // console.log(tempC_text.disabled)
    // console.log(temp.checked)
    if (temp.checked) {
        tempK_text.disabled = true;
       
    } else {
        tempK_text.disabled = false;
    }

    if (!tempC_text.disabled) {
        tempC_text.focus();
    }
    
}



function enable_tempK() {
    var tempK=document.getElementById("tempK")
    var tempC_text = document.getElementById("tempC_text")
    var tempK_text = document.getElementById("tempK_text")

    // console.log(tempK.checked);
    tempK_text.disabled = tempK.checked ? false : true;
    // console.log(tempC_text.disabled)
    if (tempK.checked) {
        
        tempC_text.disabled = true;
        
    } else {
        tempC_text.disabled = false;
    }
   
    

    if (!tempK_text.disabled) {
        tempK_text.focus();
    }
    
}


var temp = document.getElementById("temp")
var tempK=document.getElementById("tempK")
var tempK_text = document.getElementById("tempK_text")
var tempC_text = document.getElementById("tempC_text")
function equateK() {
    
        if (tempK_text.value != parseInt(tempC_text.value) + 273) {
            tempK_text.value = parseInt(tempC_text.value) +273
        }    
}
function equateC() {
    
    if (tempC_text.value != parseInt(tempK_text.value) -273) {
        tempC_text.value = parseInt(tempK_text.value) -273
    }   
}

function loader() {
    $('#loading').show();
    $('.form-wizard').hide();
} 
console.log($('#btn-submit'))
