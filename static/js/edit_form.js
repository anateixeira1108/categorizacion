$(function(){

/* Al cargar */
	
	if ($(".activar-campos").attr("editable") === "false")
	{
		$("input, select, textarea").each(function(){		
			$(this).attr("disabled",true);
			
			if(!$(this).is(":hidden")){
            	$(this).addClass('form-control');
          	}
		});
	}

/* Activar y Desactivar edicion */

	$(".activar-campos").click(function(){				
		toggle = $(this).attr("editable");
		var b = undefined;
		var msg = "";

		if(toggle === "true")
		{
			$(this).attr("editable","false");
			b = true;					
			msg = "Activar Edici&oacute;n&nbsp; <i class='fa fa-edit'></i>";
			
			$('#mostrar').remove();			

		}else if(toggle === "false")
		{	
			$(this).attr("editable","true");
			b = false;
			msg = "Desactivar Edici&oacute;n&nbsp;<i class='fa fa-edit'></i>";
			
			$('#mostrar').remove();
			$('.botones-formulario').append(
			'<div class="col-lg-6 col-md-6 col-sm-6 col-xs-6" id="mostrar">\
			     <a class="col-xs-12 btn btn-flat btn-primary submit-form-editar" \
			     id="editar"> \
			     Guardar&nbsp;&nbsp;<i class="fa fa-save"></i> \
			     </a>\
			</div>');
		}

		$("input").each(function(){		
			$(this).attr("disabled",b);
		});

		$("select").each(function(){
			$(this).attr("disabled",b);
		});
		$("textarea").each(function(){
			$(this).attr("disabled",b);
		});

		$("button#id_representacion").each(function(){
			$(this).attr("disabled",b);
		});

		$("#id_habilitado").bootstrapSwitch('toggleDisabled', true, false);

		$(this).html(msg);		
	});


});