$(function(){	
	/*~~~~~~~~ Desplegar y esconder los subitems ~~~~~~~~*/
	$('.icono-control').click(function(event){
		element = $(this);
		subitem = $('#'+element.attr('id')+"_subitem");

		if($(subitem).is(":visible")){
			
			$(element).children().addClass('fa-plus');
			$(subitem).fadeOut('200');
			$(element).children().removeClass('fa-minus');
		}
		else{
			
			$(element).children().addClass('fa-minus');
			$(subitem).fadeIn('200');
			$(element).children().removeClass('fa-plus');
		}
	});

	/*~~~~~~~~ Desaparecer la subseccion cuando el item tenga No o N/A ~~~~~~~~*/
	$('.item-select').change(function(event){
		id = $(this).attr('name');
		subitem = $('#'+id+"_subitem");
		valor_select = $(this).val();
		
		if(valor_select == 1 || valor_select == 2){
			$('#'+id).fadeOut('200');
			subitem.fadeOut('200');
		}
		else{
			$('#'+id).children().removeClass('fa-plus');
			$('#'+id).children().addClass('fa-minus');
			$('#'+id).fadeIn('200');
			subitem.fadeIn('200');
		}
	})

	/*~~~~~~~~Activar modal carga de imagenes formulario de autoevaluación ~~~~~~~~*/
	$('.activar-modal').click(function(){
		$('#myModal').modal({
			keyboard: false,
			backdrop: 'static'
		});
	});

	$('.hide-input-onselect').change(function(){		
		var cast = String($(this).find("option:selected").text().toLowerCase());			
		var input = $("input[type='text'][name='"+$(this).attr('id')+"']");
		cast === "no aplica" || cast === "no" ? $(input).fadeOut('200').prop('disabled', true) : $(input).fadeIn('200').prop('disabled',false);
	});

	/*~~~~~~~~ BANDEJA COORDINADOR CALIDAD TURÍSTICA ~~~~~~~~*/
	//--------- AJAX - ASIGNAR ANALISTAS----------------------
	
	var fila_tabla = '';
	var analista = '';
	var id;



	$('.activar-modal-analistas').click(function(){

		$('#quitar-analista').unbind("click");
		$('#quitar-analista').attr('id','asignar-analista');

		id= $(this).attr('solicitudid');
		$('#asignar-analista-modal').attr('solicitudid',id);
		$.ajax({
			type: 'GET',
			url: '/categorizacion/coordinador_ct/solicitud/'+id+'/asignaranalista',
			data:{
				'analista_id': null,	
			},
			success: function(server_data) {
				$('#table-body-analista').html('');
				analistas = server_data.data.analistas;
				$.each(analistas, function(position, analista){
					$('#table-body-analista').append('<tr class="fila-tabla" id='+analista[0]+'><td>'+analista[1]+" "+analista[2]+'</td></tr>');
				});
			}, 
			error: function(e){
				console.log(e);
			}
		});

		$('#asignar-analista-modal').modal({
			keyboard: false,
			backdrop: 'static'
		});
	});
	
	var token = document.getElementsByName('csrfmiddlewaretoken')[0] != undefined ? document.getElementsByName('csrfmiddlewaretoken')[0].value : undefined ;
	
	$(document).on('click', '#asignar-analista', function(){

		console.log("entrando en asignar-analista");	

		id=$('#asignar-analista-modal').attr('solicitudid');		
		$.ajax({
			type: 'POST',
			url: '/categorizacion/coordinador_ct/solicitud/'+id+'/asignaranalistapost',
			data:{
				'analista_id': $('.analista_id').attr('id'),
				csrfmiddlewaretoken: token,
			},
			success: function(server_data) {
				analista=server_data.data.analista;
				$('.analista_'+id).html('');
				$('.analista_'+id).html('<div class="quitar-analista_'+analista[0]+'" id="'+analista[0]+'">\
						<span>'+analista[1]+'</span>\
						<a class="quitar-analista-get icono-accion"><span><i class="fa fa-times"></i></span></a>\
                        </div>');
				$('#2_boton_'+id).addClass('disabled');
				//$('.menu_'+id).addClass('disabled');
				//$('#estatus_'+id).html('');
				//$('#estatus_'+id).html('<label data-toggle="tooltip" title="Solicitud en Análisis" class="label label-warning etiqueta-estatus">Análisis de Requisitos</label>');
			},
			error: function(e){
				console.log(e);
			}
		});
	});


	
	$(document).on('click', '#asignar-analista-libro', function(){

		console.log("entrando en asignar-analista");	

		id=$('#asignar-analista-modal').attr('solicitudid');	
		console.log($('.analista_id').attr('id'));
		$.ajax({
			type: 'POST',
			url: '/categorizacion/coordinador_ct/solicitud/'+id+'/asignaranalistalibro',
			data:{
				'analista_id': $('.analista_id').attr('id'),
				csrfmiddlewaretoken: token,
			},
			success: function(server_data) {
				analista=server_data.data.analista;
				$('.analista_'+id).html('');
				$('.analista_'+id).html('<div class="quitar-analista_'+analista[0]+'" id="'+analista[0]+'">\
						<span>'+analista[1]+'</span>\
						<a class="quitar-analista-get icono-accion"><span><i class="fa fa-times"></i></span></a>\
                        </div>');
				$('#2_boton_'+id).addClass('disabled');
				//$('.menu_'+id).addClass('disabled');
				//$('#estatus_'+id).html('');
				//$('#estatus_'+id).html('<label data-toggle="tooltip" title="Solicitud en Análisis" class="label label-warning etiqueta-estatus">Análisis de Requisitos</label>');
			},
			error: function(e){
				console.log(e);
			}
		});
	});


	$(document).on('click', '.quitar-analista-get', function(){
		id= $(this).parent().parent().attr('id'); // El id de la solicitud

		$('#asignar-analista-modal').attr('solicitudid',id);
		if ($('#asignar-analista-libro').attr('libro')){
			libro='SI';
		}
		else{
			libro='NO';
		}

		$('#asignar-analista-modal').attr(
			'analistaid',
			$(this).parent().attr('id')
		); // El id del analista
		
		$('#asignar-analista').unbind( "click" );
		$('#asignar-analista').attr('id','quitar-analista');

		$.ajax({
			type: 'GET',
			url: '/categorizacion/coordinador_ct/solicitud/'+id+'/asignaranalista',
			data:{
				'analista_id': $(this).parent().attr('id'),	
				'libro': libro,
			},
			success: function(server_data) {
				$('#table-body-analista').html('');
				analistas = server_data.data.analistas;

				$.each(analistas, function(position, analista){
					$('#table-body-analista').append('<tr class="fila-tabla" id='+analista[0]+'><td>'+analista[1]+" "+analista[2]+'</td></tr>');
				});

				$('#asignar-analista-modal').modal({
					keyboard: false,
					backdrop: 'static'
				});
			}, 
			error: function(e){
				console.log(e);
			}
		});		
	});


	$(document).on('click','.fila-tabla',function(){
		$(this).removeClass('warning');
		$('.fila-tabla').removeClass('active');
		$('.fila-tabla').removeClass('analista_id');
		$(this).addClass('active');
		$(this).addClass('analista_id')
	});	



	$(document).on( 'click', '#quitar-analista',function(){
		console.log("entrando en quitar-analista");
		
		id =$('#asignar-analista-modal').attr('solicitudid');
		console.log($('.analista_id').attr('id'));
		console.log($('#asignar-analista-modal').attr('analistaid'));
		$.ajax({
			type: 'POST',
			url: '/categorizacion/coordinador_ct/solicitud/'+id+'/eliminaranalistapost',
			data:{
				'analista_id': $('.analista_id').attr('id'),
				'analista_eliminado': $('#asignar-analista-modal').attr('analistaid'),
				csrfmiddlewaretoken: token,
			},
			success:function(server_data){
				error=server_data.err_msg;
				analista=server_data.data.analista;
				if(error==""){
					$('.analista_'+id).html('');
					$('.analista_'+id).html('<div class="quitar-analista_'+analista[0]+'" id="'+analista[0]+'">\
						<span>'+analista[1]+'</span>\
						<a class="quitar-analista-get icono-accion"><span><i class="fa fa-times"></i></span></a>\
                        </div>');
				}else{
					$('#notificacion-guardado-header').html('');
					$('#notificacion-guardado-header').html('<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\
						<h4 class="modal-title"> Error</h4>');
					$('#notificacion-guardado-header').attr('style',"background-color: #CE4744; color: white;");
					
					$('#notificacion-guardado-body').html(
	                        '<div class="col-lg-12 text-center">\
	                            <h4>En este estado no está en capacidad de eliminar analistas</h4>\
	                        </div>'
	                        );
	                $('#notificacion-guardado').modal();
				};
			},
			error: function(e){
				console.log(e);
			}
		});
	});


	$('.activar-modal-credenciales').click(function(){
		$('#ver-documento-pdf .modal-dialog .modal-content .modal-footer').remove();
		$("#ver-documento-pdf").modal();		
	});

	/*~~~~~~~~  BANDEJA COORDINADOR DIF ~~~~~~~~*/	
	var t=0;
	$('.activar-modal-inspectores').click(function(){
		
		id=$(this).attr('solicitudid');
		$('#quitar-inspector-post').unbind( "click" );
		$('#quitar-inspector-post').attr('id','asignar-inspector');
		$('#asignar-inspector').removeClass('quitar-inspector-post');

		t=0;
		
		$('#asignar-inspector-modal').attr('solicitudid',id);
		
		$.ajax({
			type: 'GET',
			url: '/categorizacion/coordinador_dif/solicitud/'+id+'/asignarinspector',
			success: function(server_data) {
				inspectores=server_data.data.inspectores;
				cantidad=server_data.cantidad;
				$('#table_body_inspector').html('');
				$('#table_body_inspector').attr('cantidad',cantidad);

				$.each(inspectores, function(position, inspector){
					$('#table_body_inspector').append(
						'<tr class="fila-inspector-tabla"  \
						id='+inspector[0]+'> \
						<td>'+inspector[1]+" "+inspector[2]+'</td> \
						</tr>'
					);
				});

				$('#asignar-inspector-modal').modal({
					keyboard: false,
					backdrop: 'static'
				});
			},
			error: function(e){
				console.log(e);
			}
		});	
	});

	$(document).on('click', '.fila-inspector-tabla', function(){
		
		var cupo = 0;

		if( $('.fila-inspector-tabla').length >= 1){
			var cupo = 2 - $(
				'#table_body_inspector'
				).children(
					'.active'
					).length - $('#table_body_inspector').attr('cantidad');
		}
		if( $(this).hasClass('active') ){
			$(this).removeClass('active').removeClass('inspector_candidato_'+id);
		}else if ( cupo > 0){			
			$(this).addClass('inspector_candidato_'+id);
			$(this).addClass('active');
		}		
	});

	$(document).on('click', '#asignar-inspector', function(){
		
		id = $('#asignar-inspector-modal').attr('solicitudid');
		var inspectores = {};
		var c = 0;
		$('.inspector_candidato_'+id).each(function(){			
			inspectores['i'+c] = parseInt($(this).attr('id'));
			c++;
		});
		console.log(inspectores);
		$.ajax({
			type: 'POST',
			url: '/categorizacion/coordinador_dif/solicitud/'+id+'/asignarinspectorpost',
			data: {
				'inspectores': JSON.stringify(inspectores),
				csrfmiddlewaretoken : token,
			},			
			success: function(server_data) {
				error = server_data.err_msg;
				if(error==""){
					inspectores=server_data.data.inspectores;
					cantidad = server_data.data.cantidad;
					if(cantidad == 1){

						//$('.otorgar-credenciales').attr('cantidad', 1);
						$.each(inspectores, function(k,v){
							/*Agregar todos los inspectores que han sido agregados en el servidor*/
							$('.inspector_'+id).append(
								'<div class="quitar-inspector_'+k+'" id="'+k+'">\
								<span>'+v+'</span><a class="quitar-inspector-get icono-accion"> \
								<span><i class="fa fa-times"></i></span></a>\
								<br></div>');
						});

					}else{
						$.each(inspectores, function(k,v){
							/*Agregar todos los inspectores que han sido agregados en el servidor*/
							$('.inspector_'+id).append(
								'<div class="quitar-inspector_'+k+'" id="'+k+'">\
								<span>'+v+'</span><a class="quitar-inspector icono-accion"> \
								<span><i class="fa fa-times"></i></span></a>\
								<br></div>');
						});
						$('.inspector_'+id).children('div').each(function(){
							$(this).children('a').removeClass('quitar-inspector-get');
							$(this).children('a').addClass('quitar-inspector');
						});
					}

					if($('.inspector_'+id).children().length == 2){
						$('#2_boton_'+id).addClass('disabled');
						$('.cred_'+id).removeClass('disabled');
					}
				}else{
					$('#notificacion-guardado-header').html('');
					$('#notificacion-guardado-header').html('<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\
						<h4 class="modal-title"> Error</h4>');
					$('#notificacion-guardado-header').attr('style',"background-color: #CE4744; color: white;");					
					$('#notificacion-guardado-body').html(
	                        '<div class="col-lg-12 text-center">\
	                            <h4>Debe asignar un inspector para pode proseguir</h4>\
	                        </div>'
	                        );
	                $('#notificacion-guardado').modal();
				}
					
				
			},
			error: function(e){
				console.log(e);
			}
		});
	});

	$(document).on('click', '.quitar-inspector-get', function(){
		id= $(this).parent().parent().attr('id'); // El id de la solicitud

		$('#asignar-inspector-modal').attr('solicitudid',id);

		$('#asignar-inspector-modal').attr('inspectorid',$(this).parent().attr('id'));
		
		$('#asignar-inspector').unbind( "click" );
		$('#asignar-inspector').addClass('quitar-inspector-post');
		$('#asignar-inspector').attr('id','quitar-inspector-post');


		$.ajax({
			type: 'GET',
			url: '/categorizacion/coordinador_dif/solicitud/'+id+'/asignarinspector',
			success: function(server_data) {
				$('#table-body_inspector').html('');
				inspectores=server_data.data.inspectores;
				cantidad=server_data.cantidad;
				$('#table_body_inspector').html('');
				$('#table_body_inspector').attr('cantidad',cantidad);

				$.each(inspectores, function(position, inspector){
					$('#table_body_inspector').append(
						'<tr class="fila-inspector-tabla-get"  \
						id='+inspector[0]+'> \
						<td>'+inspector[1]+" "+inspector[2]+'</td> \
						</tr>'
					);
				});

				$('#asignar-inspector-modal').modal({
					keyboard: false,
					backdrop: 'static'
				});
			}, 
			error: function(e){
				console.log(e);
			}
		});
	
	});

	$(document).on('click', '.fila-inspector-tabla-get', function(){

			$('.fila-inspector-tabla-get').removeClass('active');
			$('.fila-inspector-tabla-get').removeClass('inspector_candidato_1');		
			$(this).addClass('inspector_candidato_1');
			$(this).addClass('active');		
	});	

	$(document).on( 'click', '.quitar-inspector-post',function(){
		id = $('#asignar-inspector-modal').attr('solicitudid');
		inspector_id= $('#asignar-inspector-modal').attr('inspectorid');
		$.ajax({
			type: 'POST',
			url: '/categorizacion/coordinador_dif/solicitud/'+id+'/eliminarinspector',
			data:{
				'inspector_id': inspector_id,
				'inspector_nuevo': $('.inspector_candidato_1').attr('id'),
				csrfmiddlewaretoken: token,
			},
			success:function(server_data){
				error=server_data.err_msg;
				inspector=server_data.data.inspector;
				inspector_nuevo=server_data.data.inspector_nuevo; 
				if(error==""){					
					$('.quitar-inspector_'+inspector_id, $('.inspector_'+id)).remove();
					$('.inspector_'+id).append('<div class="quitar-inspector_'+inspector_nuevo[0]+'\
						" id="'+inspector_nuevo[0]+'">\
						<span>'+inspector_nuevo[1]+'</span><a class="quitar-inspector-get icono-accion"> \
						<span><i class="fa fa-times"></i></span></a>\
						<br></div>');
					$('#2_boton_'+id).removeClass('disabled');
				}else{
					$('#notificacion-guardado-header').html('');
					$('#notificacion-guardado-header').html('<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\
						<h4 class="modal-title"> Error</h4>');
					$('#notificacion-guardado-header').attr('style',"background-color: #CE4744; color: white;");					
					$('#notificacion-guardado-body').html(
	                        '<div class="col-lg-12 text-center">\
	                            <h4>En este estado no está en capacidad de eliminar inspectores</h4>\
	                        </div>'
	                        );
	                $('#notificacion-guardado').modal();
				};
			},
			error: function(e){
				console.log(e);
			}
		});
	});

	$(document).on( 'click', '.quitar-inspector',function(){
		id = $(this).parent().parent().attr('id');
		inspector_id= $(this).parent().attr('id');
		$.ajax({
			type: 'POST',
			url: '/categorizacion/coordinador_dif/solicitud/'+id+'/eliminarinspector',
			data:{
				'inspector_id': inspector_id,
				'inspector_nuevo': null,
				csrfmiddlewaretoken: token,
			},
			success:function(server_data){
				error=server_data.err_msg;
				inspector=server_data.data.inspector;
				estado=server_data.data.estado;
				if(error==""){					
					$('.quitar-inspector_'+inspector_id, $('.inspector_'+id)).remove();
					if(estado == 'RIT'){
						$('.quitar-inspector_'+inspector[0]).children('a').attr('class','quitar-inspector-get');
					}
					$('.quitar-inspector_'+inspector[0]).children('a').addClass('icono-accion');
					$('#2_boton_'+id).removeClass('disabled');
					//$('.otorgar-credenciales').addClass('disabled');
					$('.ver-credenciales').addClass('disabled');
				}else{
					$('#notificacion-guardado-header').html('');
					$('#notificacion-guardado-header').html('<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\
						<h4 class="modal-title"> Error</h4>');
					$('#notificacion-guardado-header').attr('style',"background-color: #CE4744; color: white;");					
					$('#notificacion-guardado-body').html(
	                        '<div class="col-lg-12 text-center">\
	                            <h4>En este estado no está en la capacidad de eliminar inspectores</h4>\
	                        </div>'
	                        );
	                $('#notificacion-guardado').modal();
				};
			},
			error: function(e){
				console.log(e);
			}
		});
	});

	/*~~~~~~~~~~~~~~~~~~~~~~~~ ADMINISTRACION DE EMPLEADOS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/


	$(document).on('click', '#boton-aceptar-empleados', function(){
		tiporol_id = $('.table_empleados').attr('id');
		funcionario_id = $(this).attr('funcionarioid');
        $.ajax({
			type: 'GET',
			url: '/categorizacion/'+tiporol_id+'/admin_empleados',
			data:{
				'funcionario_id': funcionario_id,
			},
			success:function(server_data){
				error= server_data.err_msg;
				if(error==""){
					$('#table-body-analista').html('');
					analistas = server_data.data.analistas;

					$.each(analistas, function(position, analista){
						$('#table-body-analista').append('<tr class="fila-tabla" id='+analista[0]+'><td>'+analista[1]+" "+analista[2]+'</td></tr>');
					});

					$('#asignar-empleado-analista').attr('funcionarioid',funcionario_id);
					$('#asignar-empleado-analista').attr('coordinador',tiporol_id);
					$('#asignar-analista-modal').modal({
						keyboard: false,
						backdrop: 'static'
					});
				}else{
					$('body').removeClass('modal-open');
					$('.modal-backdrop').remove();
					$('#notificacion-general-Label').html('Notificacion');
                    $('.notificacion-general-cerrar').addClass('notificacion-unchecked-cerrar');
                    $('.notificacion-general-cerrar').addClass('desvanecer-modal');
                    $('#notificacion-general-body').html(
                        '<div class="col-lg-12 text-center">\
                            <h4>No es necesario reemplazar a este funcionario, ¿desea proseguir a deshabilitarlo? </h4>\
                        </div>')
                    $('#notificacion-general-footer').html(
                    	'<div class="col-xs-6" data-dismiss="modal">\
                            <a href="#" class="btn btn-danger desvanecer-modal col-xs-12">Cancelar</a>\
                        </div>\
                        <div class="col-xs-6" id="sin-funcionario" data-dismiss="modal">\
                            <a href="#" id="asignar-empleado-analista" class="btn btn-primary col-xs-12" funcionarioid="'+funcionario_id+'" coordinador="'+tiporol_id+'">Aceptar</a>\
                        </div>');
                   	$('#notificacion-general').modal("show");
				}				
			},
			error: function(e){
				console.log(e);
			}
        });
        
    });

	$(document).on('click', '.desvanecer-modal', function(){
		$('body').removeClass('modal-open');
		$('.modal-backdrop').remove();
	})

	$(document).on('click', '#boton-inspector-empleados', function(){
		tiporol_id = $('.table_empleados').attr('id');
		console.log(tiporol_id);
		funcionario_id = $(this).attr('funcionarioid');
		console.log(funcionario_id);
        $.ajax({
			type: 'GET',
			url: '/categorizacion/'+tiporol_id+'/admin_empleados',
			data:{
				'funcionario_id': funcionario_id,
			},
			success:function(server_data){
				error= server_data.err_msg;
				if(error==""){
					inspectores=server_data.data.inspectores;
					cantidad=server_data.cantidad;

					$('#table_body_inspector').html('');
					$.each(inspectores, function(position, inspector){
						$('#table_body_inspector').append(
							'<tr class="fila-inspector-tabla-get"  \
							id='+inspector[0]+'> \
							<td>'+inspector[1]+" "+inspector[2]+'</td> \
							</tr>'
						);
					});

					$('#asignar-empleado-inspector').attr('funcionarioid',funcionario_id);
					$('#asignar-empleado-inspector').attr('coordinador',tiporol_id);

					$('#asignar-inspector-modal').modal({
						keyboard: false,
						backdrop: 'static'
					});
				}else{
					$('#notificacion-general-Label').html('Notificacion');
                    $('.notificacion-general-cerrar').addClass('notificacion-unchecked-cerrar');
                    $('.notificacion-general-cerrar').addClass('desvanecer-modal');
                    $('#notificacion-general-body').html(
                        '<div class="col-lg-12 text-center">\
                            <h4>No es necesario reemplazar a este funcionario, ¿desea proseguir a deshabilitarlo? </h4>\
                        </div>')
                    $('#notificacion-general-footer').html(
                    	'<div class="col-xs-6" data-dismiss="modal">\
                            <a href="#" class="btn btn-danger desvanecer-modal col-xs-12">Cancelar</a>\
                        </div>\
                        <div class="col-xs-6" id="sin-funcionario" data-dismiss="modal">\
                            <a href="#" id="asignar-empleado-inspector" class="btn btn-primary col-xs-12" funcionarioid="'+funcionario_id+'" coordinador="'+tiporol_id+'">Aceptar</a>\
                        </div>');
                    $('#notificacion-general').modal({
                    	keyboard: false,
						backdrop: 'static'
                    });
				}

			},
			error: function(e){
				console.log(e);
			}
        });

        
    });

    $(document).on('click', '#asignar-empleado-analista', function(){
		tiporol_id = $(this).attr('coordinador');
		funcionario_id = $(this).attr('funcionarioid');
        $.ajax({
			type: 'POST',
			url: '/categorizacion/'+tiporol_id+'/admin_empleados',
			data:{
				'funcionario_nuevo': $('.analista_id').attr('id'),
				'funcionario_id': funcionario_id,
				'funcionario': $(this).parent().attr('id'),
				csrfmiddlewaretoken: token,
			},
			success:function(server_data){
				error = server_data.err_msg;
				$('#notificacion-guardado-header').html('');
				$('#notificacion-guardado-header').attr('style',"background-color: #CE4744; color: white;");
				
				if(error==""){
					$('#notificacion-guardado-header').html('<button type="button" class="close desvanecer-modal" data-dismiss="modal" aria-hidden="true">&times;</button>\
						<h4 class="modal-title"> Notificaci&oacute;n</h4>');					
					$('#notificacion-guardado-body').html(
		               	'<div class="col-lg-12 text-center">\
		       	            <h4>Se ha deshabilitado al analista exitosamente</h4>\
		                </div>');

				}else{
					$('#notificacion-guardado-header').html('<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\
						<h4 class="modal-title"> Error</h4>');				
					$('#notificacion-guardado-body').html(
		               	'<div class="col-lg-12 text-center">\
		       	            <h4>Debe haber un reemplazo de funcionario para proseguir</h4>\
		                </div>');
		            
				}
					$('#notificacion-guardado-footer').html('')
					$('#notificacion-guardado-footer').html('<div class="col-xs-offset-1 col-xs-10" id="sin-funcionario" data-dismiss="modal">\
				            <a href="#" id="boton-aceptar" class="btn btn-primary desvanecer-modal col-xs-12">Aceptar</a>\
				        </div>\
			      	</div>');
				$('#notificacion-guardado').modal();

				
			},
			error: function(e){
				console.log(e);
			}
        });
        
    });

    $(document).on('click', '#asignar-empleado-inspector', function(){
		tiporol_id = $(this).attr('coordinador');
		funcionario_id = $(this).attr('funcionarioid');
        $.ajax({
			type: 'POST',
			url: '/categorizacion/'+tiporol_id+'/admin_empleados',
			data:{
				'funcionario_nuevo': $('.inspector_candidato_1').attr('id'),
				'funcionario_id': funcionario_id,
				'funcionario': $(this).parent().attr('id'),
				csrfmiddlewaretoken: token,
			},
			success:function(server_data){
				error=server_data.err_msg;
				if(error==""){
					$('#notificacion-guardado-header').html('');
					$('#notificacion-guardado-header').html('<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\
						<h4 class="modal-title"> Notificaci&oacute;n</h4>');
					$('#notificacion-guardado-header').attr('style',"background-color: #CE4744; color: white;");					
					$('#notificacion-guardado-body').html(
		               	'<div class="col-lg-12 text-center">\
		       	            <h4>Se ha deshabilitado al inspector exitosamente</h4>\
		                </div>');
				}else{
					$('#notificacion-guardado-header').html('<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\
						<h4 class="modal-title"> Error</h4>');				
					$('#notificacion-guardado-body').html(
		               	'<div class="col-lg-12 text-center">\
		       	            <h4>Debe haber un reemplazo de funcionario para proseguir</h4>\
		                </div>');
				}
				$('#notificacion-guardado-footer').html('')
				$('#notificacion-guardado-footer').html('<div class="col-xs-offset-1 col-xs-10" id="sin-funcionario" data-dismiss="modal">\
			            <a href="#" id="boton-aceptar" class="btn btn-primary desvanecer-modal col-xs-12">Aceptar</a>\
			        </div>\
		      	</div>');
				$('#notificacion-guardado').modal();
				
				
			},
			error: function(e){
				console.log(e);
			}
        });
        
    });

	$(document).on('click', '#boton-habilitar-empleados', function(){
		tiporol_id = $(this).attr('coordinador');
		funcionario_id = $(this).attr('funcionarioid');
        $.ajax({
			type: 'POST',
			url: '/categorizacion/'+tiporol_id+'/admin_empleados',
			data:{
				'funcionario_nuevo': null,
				'funcionario_id': funcionario_id,
				csrfmiddlewaretoken: token,
			},
			success:function(server_data){
				$('#notificacion-guardado-header').html('');
				$('#notificacion-guardado-header').html('<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\
					<h4 class="modal-title"> Notificaci&oacute;n</h4>');
				$('#notificacion-guardado-header').attr('style',"background-color: #CE4744; color: white;");					
				$('#notificacion-guardado-body').html(
	               	'<div class="col-lg-12 text-center">\
	       	            <h4>Se ha habilitado al funcionario exitosamente</h4>\
	                </div>');
	            $('#notificacion-guardado').modal();
			},
			error: function(e){
				console.log(e);
			}
        });
    });


	/*~~~~~~~~~~~~~~~~~~~~~~~~~~~ BUSQUEDAS Y FILTROS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/

	$('#razon_social_check').children('div').children('input').on('ifChecked', function(event){
		$(this).val('checked');
    });
	$('#rif_check').children('div').children('input').on('ifChecked', function(event){
        $(this).addClass('checked');
        $(this).val('checked');  
    });
    $('#rtn_check').children('div').children('input').on('ifChecked', function(event){
       	$(this).val('checked');
    });

    $('#razon_social_check').children('div').children('input').on('ifUnchecked', function(event){
		$(this).val('');
    });
	$('#rif_check').children('div').children('input').on('ifUnchecked', function(event){
        $(this).val('');  
    });
    $('#rtn_check').children('div').children('input').on('ifUnchecked', function(event){
       	$(this).val('');
    });


    $(document).on('click', '#activar_buscar_modal', function(){
    	$('#msj-error-buscar').html('');
    	$('#activar_buscar_modal').addClass('disabled');
    	var categorizacion_bandeja = $('.categorizacion_bandeja');
    	var lsr_bandeja = $('.lsr_bandeja');
    	var entrada_portal = $('.entrada_portal');
    	var categorizacion_reporte = $('.categorizacion_reporte');
    	var gestion_casos = $('.gestion_casos');
    	var historial_prestador = $('.historial_prestador');
    	var placas_bandeja = $('.placas_bandeja');
    	var procesos_bandeja = $('.procesos_bandeja');
    	var consignaciones = $('.consignaciones');
    	var por_entregar = $('.por_entregar');
    	var reporte_dist_placas = $('.distribucion_placas');
    	var reporte_dist_eat = $('.reporte_dist_eat');
    	var reporte_dist_lsr = $('.reporte_dist_lsr');
    	var reporte_comparativo_eat = $('.reporte_comparativo_eat');
    	var bandeja="";
    	var tiporol="";
    	var funcionario = {};
    	if(categorizacion_bandeja.length>0 || categorizacion_reporte.length>0 || historial_prestador.length>0 || procesos_bandeja.length>0){
    		if(categorizacion_reporte.length>0){
    			tiporol = $('.categorizacion_reporte').attr('tiporol');
    			bandeja='categorizacion_reporte';
    		}else{
    			if (categorizacion_bandeja.length>0){
    				tiporol = $('.categorizacion_bandeja').attr('tiporol');
    				bandeja='categorizacion_bandeja';
    			}else{
    				if (historial_prestador.length>0){
    					tiporol = $('.historial_prestador').attr('tiporol');
    					bandeja='historial_prestador';
    				}else{
    					tiporol = $('.procesos_bandeja').attr('tiporol');
    					bandeja='procesos_bandeja';
    				}		
    			}
    			
    		}
    		if(tiporol!=undefined){
    			var c=0;
    			if (bandeja == 'historial_prestador'){
    				funcionario['funcionario0']=['Inspector', 'inspectores'];
					funcionario['funcionario1']=['CoordinadorCT','coordinador_cts'];
					funcionario['funcionario2']=['DirectorCT','director_cts'];
					$('#Analista').remove();
					$('#analistas').remove();
					$('#buscar_col_2').append('<label class="labelmodal" id="Analista">Analista</label>\
	                    <select name="analistas" id="analistas" class="select">\
	                    	<option value="">--Seleccione--</option>\
                    	</select>');

    			}else{
	    			if(tiporol=='coordinador_ct'){
	    				funcionario['funcionario0']=['Analista','analistas'];
	    			}else{
	    				if(tiporol=='coordinador_dif'){
	    					funcionario['funcionario0']=['Inspector', 'inspectores'];
	    				}else{
	    					if(tiporol=='director_ct'){
	    						funcionario['funcionario0']=['Analista','analistas'];
	    						funcionario['funcionario1']=['CoordinadorCT','coordinador_cts'];
	    					}else{
	    						if(tiporol=='viceministro'){
	    							funcionario['funcionario0']=['Analista','analistas'];
	    							funcionario['funcionario1']=['CoordinadorCT','coordinador_cts'];
	    							funcionario['funcionario2']=['DirectorCT','director_cts'];
	    						}else{
	    							if(tiporol=='ministro'){
	    								funcionario['funcionario0']=['Analista','analistas'];
	    								funcionario['funcionario1']=['CoordinadorCT','coordinador_cts'];
	    								funcionario['funcionario2']=['DirectorCT','director_cts'];
		    							funcionario['funcionario3']=['Viceministro','viceministros'];
	    							}
	    						}
	    					}
	    				}

	    			}
    			}
    			if (bandeja=='procesos_bandeja'){
    				funcionario['funcionario2']=['DirectorCT', 'director_cts'];
    				funcionario['funcionario3']=['Inspector', 'inspectores'];
    			}

    			$.each(funcionario,function(){
    				$('#'+funcionario['funcionario'+c][0]+'').remove();
    				$('#'+funcionario['funcionario'+c][1]+'').remove();
    				$('#buscar_col_3').append(
    					'<label class="labelmodal" id="'+funcionario['funcionario'+c][0]+'">'+funcionario['funcionario'+c][0]+'</label>\
	                    <select name="'+funcionario['funcionario'+c][1]+'" id="'+funcionario['funcionario'+c][1]+'" class="select">\
	                    	<option value="">--Seleccione--</option>\
                    	</select>');
                    ++c;
    			});
    		
			}else{
				$('#buscar_texto').remove();
		       	$('#razon_social_check_buscar').remove();
		        $('#rif_check_buscar').remove();
		       	$('#rtn_check_buscar').remove();
			};
    		$('#buscar_col_1').remove();
	       	$('#buscar_col_2').children('#libro').remove();
	       	$('#buscar_col_2').children('#libros').remove();
	    }
	    else if(reporte_dist_placas.length>0 || reporte_dist_eat.length>0 || reporte_dist_lsr.length>0 || reporte_comparativo_eat.length>0){
	    	if (reporte_dist_placas.length>0){

		    	//Se modifica la bandeja de busqueda para los filtors de los reportes
		    	//La busqueda simple ya no va
		    	$('#buscar_col_0').remove();
		    	//Se prepara los campos de ubicacion geografica, estado y municipio seran de seleccion multiple
		    	$('#municipios').attr('disabled', true);
	            $('#parroquias').attr('disabled', true);
	            $('#estados').html('');
	            $('#estados').attr('multiple', true);
            	bandeja = 'distribucion_placas';
	    	}
            //Comence yo (Ana)
            else if (reporte_dist_eat.length>0 || reporte_comparativo_eat.length>0 || reporte_dist_lsr.length>0){
            	$("#filtros-busqueda-avanzada").show();
            	$('#municipios').attr('disabled', true);
	            $('#parroquias').attr('disabled', true);
            	$('#buscar_col_0').remove();
            	$('#buscar_col_2').children().remove();
            	if (reporte_dist_eat.length>0){
	            	$('#buscar_col_2').html(
	                  	'<label class="labelmodal" id="clasificacion">Clasificaci&oacute;n</label>\
	                    	<select name="clasificacion" id="clasificaciones" class="select">\
	                      		<option value="">--Seleccione--</option>\
	                    	</select>\
	                  	<label class="labelmodal" id="categoria">Categor&iacute;a</label>\
	                    	<select name="categoria" id="categorias" class="select" disabled="true">\
	                      		<option value="">--Seleccione--</option>\
	                    	</select>'
	                );
	            	bandeja='reporte_dist_eat';
            	}else{
	            	$('#buscar_col_2').html(
	                  	'<label class="labelmodal" id="clasificacion">Clasificaci&oacute;n</label>\
	                    	<select name="clasificacion" id="clasificaciones" class="select">\
	                      		<option value="">--Seleccione--</option>\
	                    	</select>'
	                );
	                if (reporte_comparativo_eat.length>0){
	            		$('#buscar-estatus').remove();
    	        		$('#estatus_placas').remove();
	            		bandeja='reporte_comparativo_eat';      		
	                }else{
	                	bandeja='reporte_dist_lsr'; 
	                }
            	}
            }

	    }else{
	    	if(lsr_bandeja.length>0 || entrada_portal.length>0 || consignaciones.length>0 || por_entregar.length>0){
	    		if(lsr_bandeja.length>0 || por_entregar.length>0){
	    			if (lsr_bandeja.length>0){
	    				tiporol = $('.lsr_bandeja').attr('tiporol');
	    				bandeja= 'lsr_bandeja';
	    			}
	    			else {
	    				tiporol =$('.por_entregar').attr('tiporol');
	    				bandeja = 'por_entregar';	    				
	    				$('#campo-fecha').remove();
	    			}
	    			$('#libro').remove();
	    			$('#libros').remove();
	    		}else{
	    			if(consignaciones.length>0){
	    				tiporol = $('.consignaciones').attr('tiporol');
	    				bandeja = 'consignaciones';
	    				$('#campo-fecha').remove();
	    				$('#buscar_col_1').remove();
	    			}
	    			else{
	    				tiporol = $('.entrada_portal').attr('tiporol');
	    			}
	    		}
	    		
	    		if(tiporol==undefined){
					$('#buscar_texto').remove();
					$('#razon_social_check_buscar').remove();
			        $('#rif_check_buscar').remove();
			       	$('#rtn_check_buscar').remove();
				}
		       	$('#municipios').attr('disabled', true);
                $('#parroquias').attr('disabled', true);
                $('#estados').html('');
                $('#estados').html('<option value="">--Seleccione--</option>');
	    		$('#municipios').html('');
	    		$('#municipios').html('<option value="">--Seleccione--</option>');
	    		$('#parroquias').html('');
	    		$('#parroquias').html('<option value="">--Seleccione--</option>');
	    		if (consignaciones.length>0){	
		    		$('#libros').html('');
		    		$('#libros').html('<option value="">--Seleccione--</option>');
	    		}
	    		if(entrada_portal.length>0){
	    			$('#buscar_col_2').html('')
	    			$('#buscar_col_3').html('')
	    			$('#buscar_col_2').html('<label class="labelmodal" id="sucursal">Sucursal</label>\
                        <select name="sucursal" id="sucursales" class="select">\
                          <option value="">--Seleccione--</option>\
                        </select>\
	    				<label class="labelmodal" id="turista">Nombre de Turista</label>\
                        <select name="sucursal" id="turistas" class="select">\
                          <option value="">--Seleccione--</option>\
                        </select>\
                        <label class="labelmodal" id="tipocomentario">Tipo de Comentario</label>\
                        <select name="tipo_comentario" id="tipocomentarios" class="select">\
                          <option value="">--Seleccione--</option>\
                        </select>\
                    ')
                    $('#buscar_col_3').append('<label class="labelmodal" id="severidad">Severidad</label>\
                        <select name="severidad" id="severidades" class="select">\
                          <option value="">--Seleccione--</option>\
                        </select>')

	    			bandeja= 'entrada_portal';
	    			$('#libro').remove();
	    			$('#libros').remove();
	    		}
	    	}else{
		    	if(placas_bandeja.length>0){
		    		tiporol = $('.placas_bandeja').attr('tiporol');
		    		bandeja = 'placas_bandeja';
			       	$('#estatus_placas').remove();
			       	$('#buscar-estatus').remove();
			       	$('#libro').remove();
			       	$('#libros').remove();
			       	$('#fecha-busqueda').remove();
			       	$('#buscar_col_2').html('<label class="labelmodal" id="sucursal">Sucursal</label>\
                        <select name="sucursal" id="sucursales" class="select">\
                          <option value="">--Seleccione--</option>\
                        </select>\
                        <label class="labelmodal" id="tipo_licencia">Tipo de Licencia</label>\
                        <select name="tipo_licencias" id="tipo_licencias" class="select">\
                          <option value="">--Seleccione--</option>\
                        </select>');
                	$("#filtros-busqueda-avanzada").show();
                	$('#municipios').attr('disabled', true);
    	            $('#parroquias').attr('disabled', true);
                	$('#buscar_col_0').remove();
		    	}
		    }
		}
		
       	$('#buscar-estatus').html('');

       	$('#sucursales').html('');

       	$('#buscar-estatus').html('<option value="">--Seleccione--</option>');

       	$('#sucursales').html('<option value="">--Seleccione--</option>');

       	if(gestion_casos.length>0){
       		bandeja= 'gestion_casos';
       		tiporol=$('.gestion_casos').attr('tiporol');

       		if(tiporol!=undefined){
       			$('#fecha-busqueda').remove();
       			$('#buscar_texto').remove();
				$('#razon_social_check_buscar').remove();
		        $('#rif_check_buscar').remove();
		       	$('#rtn_check_buscar').remove();
       			$('#buscar_col_1').remove();
       			$('#buscar-estatus').parent().remove();
       			$('#buscar-estatus').remove();
	       		$('#buscar_col_2').html('');
				$('#buscar_col_2').append('<label id="funcionario" class="labelmodal">Funcionario</label>\
	                <select id="funcionarios" name="funcionario" class="form-control input-sm"><option value="">--Seleccione--</option></select><br/>\
	                <label id="tiporol" class="labelmodal">Tipo de Rol</label>\
	                <select id="tiporoles" name="tiporol" class="form-control input-sm"><option value="">--Seleccione--</option></select>');
       		}
       		
       	}
       	console.log(bandeja)
       	$.ajax({
       		type: 'GET',
			url: '/categorizacion/funcionario/bandeja/buscar',
			data:{
				'bandeja': bandeja,
				'tiporol': tiporol,
				'funcionario': funcionario
			},
			success:function(server_data){
				error=server_data.err_msg;
				if(error==""){
					estados=server_data.data.estados;
					sucursales=server_data.data.sucursales;
					if (categorizacion_bandeja.length>0 || categorizacion_reporte.length>0 || historial_prestador.length>0 || procesos_bandeja.length>0){
						console.log("fdlkfpn")
						analistax=server_data.data.analistax;
						inspectorx=server_data.data.inspectorx;
						coordinador_ctx=server_data.data.coordinador_ctx;
						director_ctx=server_data.data.directorx;
						viceministrox=server_data.data.viceministrox;
						if(tiporol!=undefined){
							$.each(analistax,function(value){
								$('#analistas').append('<option value="'+analistax[value][0]+'">'+analistax[value][1]+'</option>');
							});
							$.each(inspectorx,function(value){
								$('#inspectores').append('<option value="'+inspectorx[value][0]+'">'+inspectorx[value][1]+'</option>');
							});
							$.each(coordinador_ctx,function(value){
								$('#coordinador_cts').append('<option value="'+coordinador_ctx[value][0]+'">'+coordinador_ctx[value][1]+'</option>');
							});
							$.each(director_ctx,function(value){
								$('#director_cts').append('<option value="'+director_ctx[value][0]+'">'+director_ctx[value][1]+'</option>');
							});
							$.each(viceministrox,function(value){
								$('#viceministros').append('<option value="'+viceministrox[value][0]+'">'+viceminstrox[value][1]+'</option>');
							});
						}


						$.each(estados,function(value){
							$('#buscar-estatus').append('<option value="'+estados[value]+'">'+estados[value]+'</option>');
						});

						$.each(sucursales,function(key,value){
							$('#sucursales').append('<option value="'+value[0]+'">\
								'+value[1]+'</option>');
						});		
						
							
					}
					else if(lsr_bandeja.length>0 || consignaciones.length>0 ||por_entregar.length>0){
						estado = server_data.data.estado;
						libros = server_data.data.libros;
						
						if(consignaciones.length>0){
							$.each(libros,function(value){
								$('#libros').append('<option value="'+libros[value]+'">'+libros[value]+'</option>');
							});
						}
						
						$.each(estado,function(value){
							$('#estados').append('<option value="'+estado[value][0]+'">'+estado[value][1]+'</option>');
						});


						$.each(estados,function(value){
							$('#buscar-estatus').append('<option value="'+estados[value]+'">'+estados[value]+'</option>');
						});

						$.each(sucursales,function(key,value){
							$('#sucursales').append('<option value="'+value[0]+'">\
								'+value[1]+'</option>');
						});	
					}
					else if(entrada_portal.length>0){
						estado = server_data.data.estado;
						turista = server_data.data.turista;
						tipo_comment = server_data.data.tipo_comment;
						severidad = server_data.data.severidad;

						$.each(estado,function(value){
							$('#estados').append('<option value="'+estado[value][0]+'">'+estado[value][1]+'</option>');
						});

						$.each(turista,function(value){
							$('#turistas').append('<option value="'+turista[value][0]+'">'+turista[value][1]+'</option>');
						});
						$.each(tipo_comment,function(value){
							$('#tipocomentarios').append('<option value="'+tipo_comment[value]+'">'+tipo_comment[value]+'</option>');
						});
						$.each(severidad,function(value){
							$('#severidades').append('<option value="'+severidad[value]+'">'+severidad[value]+'</option>');
						});


						$.each(estados,function(value){
							$('#buscar-estatus').append('<option value="'+estados[value]+'">'+estados[value]+'</option>');
						});

						$.each(sucursales,function(key,value){
							$('#sucursales').append('<option value="'+value[0]+'">\
								'+value[1]+'</option>');
						});	
					}
					else if(entrada_portal.length>0){
						estado = server_data.data.estado;
						turista = server_data.data.turista;
						tipo_comment = server_data.data.tipo_comment;
						severidad = server_data.data.severidad;

						$.each(estado,function(value){
							$('#estados').append('<option value="'+estado[value][0]+'">'+estado[value][1]+'</option>');
						});

						$.each(turista,function(value){
							$('#turistas').append('<option value="'+turista[value][0]+'">'+turista[value][1]+'</option>');
						});
						$.each(tipo_comment,function(value){
							$('#tipocomentarios').append('<option value="'+tipo_comment[value]+'">'+tipo_comment[value]+'</option>');
						});
						$.each(severidad,function(value){
							$('#severidades').append('<option value="'+severidad[value]+'">'+severidad[value]+'</option>');
						});


						$.each(estados,function(value){
							$('#buscar-estatus').append('<option value="'+estados[value]+'">'+estados[value]+'</option>');
						});

						$.each(sucursales,function(key,value){
							$('#sucursales').append('<option value="'+value[0]+'">\
								'+value[1]+'</option>');
						});	
					}
					else if(gestion_casos.length>0){
						funcionario=server_data.data.funcionario;
						tiporols=server_data.data.tiporol;
						$.each(funcionario,function(value){
							$('#funcionarios').append('<option value="'+funcionario[value][0]+'">'+funcionario[value][1]+'</option>');
						});

						$.each(tiporols,function(value){
							$('#tiporoles').append('<option value="'+tiporols[value]+'">\
								'+tiporols[value]+'</option>');
						});	
					}
					else if(placas_bandeja.length>0){
						$.each(server_data.data.entidades, function(key, value){
							$('#estados').append('<option value="'+key+'">\
								'+value+'</option>');
						});
						tipos = server_data.data.tipos;
						sucursales =server_data.data.sucursales;
						$.each(sucursales,function(key,value){
							$('#sucursales').append('<option value="'+key+'">\
								'+value+'</option>');
						});	
						$.each(tipos,function(key,value){
							$('#tipo_licencias').append('<option value="'+key+'">\
								'+value+'</option>');
						});	
					}
					else if(reporte_dist_placas.length>0){
						console.log(server_data);
					}else if (reporte_dist_eat.length>0 || reporte_comparativo_eat.length>0 || reporte_dist_lsr.length>0){
						$.each(server_data.data.entidades, function(key, value){
							$('#estados').append('<option value="'+key+'">\
								'+value+'</option>');
						});
						$.each(server_data.data.clasificaciones, function(key, value){
							$('#clasificaciones').append('<option value="'+key+'">\
								'+value+'</option>');
						});
						if (reporte_dist_eat.length>0 || reporte_dist_lsr.length>0){
							$.each(server_data.data.estatus, function(key, value){
								$('#buscar-estatus').append('<option value="'+key+'">\
									'+value+'</option>');
							});
						}
					}else{
						/*if(lsr_bandeja.length>0 || consignaciones.length>0){
							estado = server_data.data.estado;
							libros = server_data.data.libros;
							
							$.each(libros,function(value){
								$('#libros').append('<option value="'+libros[value]+'">'+libros[value]+'</option>');
							});
							
							$.each(estado,function(value){
								$('#estados').append('<option value="'+estado[value]+'">'+estado[value]+'</option>');
							});
							
						}else{
							if(entrada_portal.length>0){
								estado = server_data.data.estado;
								turista = server_data.data.turista;
								tipo_comment = server_data.data.tipo_comment;
								severidad = server_data.data.severidad;

								$.each(estado,function(value){
									$('#estados').append('<option value="'+estado[value]+'">'+estado[value]+'</option>');
								});

								$.each(turista,function(value){
									$('#turistas').append('<option value="'+turista[value][0]+'">'+turista[value][1]+'</option>');
								});
								$.each(tipo_comment,function(value){
									$('#tipocomentarios').append('<option value="'+tipo_comment[value]+'">'+tipo_comment[value]+'</option>');
								});
								$.each(severidad,function(value){
									$('#severidades').append('<option value="'+severidad[value]+'">'+severidad[value]+'</option>');
								});
							}
						}*/
					}
					/*if(gestion_casos.length>0){
						funcionario=server_data.data.funcionario;
						tiporols=server_data.data.tiporol;
						$.each(funcionario,function(value){
							$('#funcionarios').append('<option value="'+funcionario[value][0]+'">'+funcionario[value][1]+'</option>');
						});

						$.each(tiporols,function(value){
							$('#tiporoles').append('<option value="'+tiporols[value]+'">\
								'+tiporols[value]+'</option>');
						});		
					}else{
						if(placas_bandeja.length>0){
							placas = server_data.data.placas;
							sucursales =server_data.data.sucursales;
							$.each(sucursales,function(key,value){
								$('#sucursales').append('<option value="'+value[0]+'">\
									'+value[1]+'</option>');
							});	
							$.each(placas,function(key,value){
								$('#licencias').append('<option value="'+value[0]+'">\
									'+value[1]+'</option>');
								$('#tipo_licencias').append('<option value="'+value[0]+'">\
									'+value[2]+'</option>');
							});	
						}else{
							$.each(estados,function(value){
								$('#buscar-estatus').append('<option value="'+estados[value]+'">'+estados[value]+'</option>');
							});

							$.each(sucursales,function(key,value){
								$('#sucursales').append('<option value="'+value[0]+'">\
									'+value[1]+'</option>');
							});		
						}			
					}*/
					console.log("aqui q pasa?")
					$('#buscar_modal').modal({
			        	keyboard: false,
				        backdrop: 'static'
		       		});
				}else{
					$('#activar_buscar_modal').removeClass('disabled');
					$('#notificacion-guardado-header').html('');
					$('#notificacion-guardado-header').html('<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\
						<h4 class="modal-title"> Error</h4>');
					$('#notificacion-guardado-header').attr('style',"background-color: #CE4744; color: white;");					
					$('#notificacion-guardado-body').html(
	                    '<div class="col-lg-12 text-center">\
	                        <h4>Ninguna bandeja fue especificada</h4>\
	                    </div>'
	                    );
	                $('#notificacion-guardado').modal();
				}
			},
			error: function(e){
				console.log(e);
			}
       	});

    });

	$(document).on('change', '#estados', function(){
		$('#municipios').html('<option value="">--Seleccione--</option>');
		$('#parroquias').html('<option value="">--Seleccione--</option>');
		if($(this).val()!=""){
		    $.ajax({
		        type: 'POST',
		        url: '/categorizacion/funcionario/bandeja/buscar',
		        data:{
		            'estado_avanzado': $(this).val(),
		            csrfmiddlewaretoken:  token,
		    },success: function(server_data) {
		    	$('#municipios').attr('disabled', false);
		    	$.each(server_data.data.municipios, function(key, value){
		    		$('#municipios').append('<option value="'+key+'">\
		    			'+value+'</option>');
		    	})
		    },error: function(server_data) {
		        $('.msj-error-modal').html('<div class="alert alert-warning alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button><strong>Error:&nbsp;</strong>No es posible ubicar dicho estado</div>');
		        }
		    });
		}else{
		    $('#municipios').attr('disabled', true);
		    $('#parroquias').attr('disabled', true);
		}
	});

	$(document).on('change', '#municipios', function(){
		$('#parroquias').html('<option value="">--Seleccione--</option>');
		if($(this).val()!=""){
		    $.ajax({
		        type: 'POST',
		        url: '/categorizacion/funcionario/bandeja/buscar',
		        data:{
		            'municipio_avanzado': $(this).val(),
		            csrfmiddlewaretoken:  token,
		    },success: function(server_data) {
		    	$('#parroquias').attr('disabled', false);
		    	$.each(server_data.data.parroquias, function(key, value){
		    		$('#parroquias').append('<option value="'+key+'">\
		    			'+value+'</option>');
		    	})
		    },error: function(server_data) {
		        $('.msj-error-modal').html('<div class="alert alert-warning alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button><strong>Error:&nbsp;</strong>No es posible ubicar dicho municipio</div>');
		        }
		    });
		}else{
		    $('#parroquias').attr('disabled', true);
		}
		
	});

	$('#boton-aceptar-buscar').click(function(e){
		e.preventDefault();
		e.stopImmediatePropagation();
		if ($('.categorizacion_bandeja').length > 0){
			$('.buscar_bandeja').val('categorizacion_bandeja')
			bandeja='categorizacion_bandeja'
		}else{
			if($('.lsr_bandeja').length > 0){
				$('.buscar_bandeja').val('lsr_bandeja')
				bandeja='lsr_bandeja'
			}else{
				if($('.entrada_portal').length > 0){
					$('.buscar_bandeja').val('entrada_portal')
					bandeja='entrada_portal'
				}else{
					if($('.categorizacion_reporte').length > 0){
						$('.buscar_bandeja').val('categorizacion_reporte')
						bandeja= 'categorizacion_reporte'
					}else{
						if($('.gestion_casos').length > 0){
							$('.buscar_bandeja').val('gestion_casos')
							bandeja = 'gestion_casos'
						}else{
							if($('.historial_prestador').length > 0){
								$('.buscar_bandeja').val('historial_prestador')
								bandeja = 'historial_prestador'
							}else{
								if($('.placas_bandeja').length>0){
									$('.buscar_bandeja').val('placas_bandeja')
									bandeja = 'placas_bandeja'
								}else{
									if($('.consignaciones').length>0){
										$('.buscar_bandeja').val('consignaciones')
										bandeja = 'consignaciones'
									}
									else {
										if($('.por_entregar').length>0){
											$('.buscar_bandeja').val('por_entregar')
											bandeja = 'por_entregar'
										}
										else if($('.reporte_dist_eat').length>0){	
											$('.buscar_bandeja').val('reporte_dist_eat')
											bandeja = 'reporte_dist_eat'
										}else if($('.reporte_comparativo_eat').length>0){	
											$('.buscar_bandeja').val('reporte_comparativo_eat')
											bandeja = 'reporte_comparativo_eat'
										}else if($('.reporte_dist_lsr').length>0){
											$('.buscar_bandeja').val('reporte_dist_lsr')
											bandeja = 'reporte_dist_lsr'
										}
										else{
											$('.buscar_bandeja').val('procesos_bandeja')
											bandeja = 'procesos_bandeja'
										}
									}
								}
							}
						}
					}
				}
			}
		}
	
		if($('#buscar-texto')){
			var max = parseInt($('#buscar-texto').attr('maxlength'));
			var val = $('#buscar-texto').val();
			var i=0;
			var res="";
			var logic = false;
			while(i<max){
				res = val.slice(i);
				if(res==""){
					logic =true
					break
				}
				i+=1
			}
			if(i==max){
				$('#msj-error-buscar').html('\
					<div class="alert alert-warning alert-dismissible" role="alert">\
					<strong>Error:&nbsp;</strong> El limite de caracteres es excedido</div>');
			}
		}
		$('.form-busqueda').submit();
	});
		


	/*
	$('#boton-aceptar-buscar').click(function(){
		var bandeja="";
		if ($('.categorizacion_bandeja').length > 0){
			bandeja='categorizacion_bandeja'
		}else{
			if($('.lsr_bandeja').length > 0){
				bandeja='lsr_bandeja'
			}else{
				if($('.entrada_portal').length > 0){
					bandeja='entrada_portal'
				}else{
					if($('.categorizacion_reporte').length > 0){
						bandeja= 'categorizacion_reporte'
					}else{
						if($('.gestion_casos').length > 0){
							bandeja = 'gestion_casos'
						}else{
							bandeja = 'historial_prestador'
						}
					}
				}
			}
		}
		if($('#buscar-texto')){
			var max = parseInt($('#buscar-texto').attr('maxlength'));
			var val = $('#buscar-texto').val();
			var i=0;
			var res="";
			var logic = false;
			while(i<max){
				res = val.slice(i);
				if(res==""){
					logic =true
					break
				}
				i+=1
			}
			if(i==max){
				$('#msj-error-buscar').html('\
					<div class="alert alert-warning alert-dismissible" role="alert">\
					<strong>Error:&nbsp;</strong> El limite de caracteres es excedido</div>');
			}
		}
		
		$.ajax({
       		type: 'POST',
			url: '/categorizacion/funcionario/bandeja/buscar',
			data:{
				'fecha-desde': $('#periodo-desde').val(),
				'fecha-hasta': $('#periodo-hasta').val(),
				'estado': $('#buscar-estatus').val(),
				'sucursal': $('#sucursales').val(),
				'bandeja': bandeja,
				'estados': $('#estados').val(),
				'municipio': $('#municipios').val(),
				'parroquia': $('#parroquias').val(),
				'libro': $('#libros').val(),
				'analista':$('#analistas').val(),
				'inspector':$('#inspectores').val(),
				'coordinador_ct':$('#coordinador_cts').val(),
				'director_ct':$('#director_cts').val(),
				'viceministro':$('#viceministros').val(),
				'rtn': $('#rtn_check').children('div').children('input').val(),
				'rif': $('#rif_check').children('div').children('input').val(),
				'razon_social': $('#razon_social_check').children('div').children('input').val(),
				'buscar_texto': $('#buscar-texto').val(),
				'severidad':$('#severidades').val(),
				'turista': $('#turistas').val(),
				'tipo_comentario': $('#tipocomentarios').val(),
				'funcionario':$('#funcionarios').val(),
				'tiporol': $('#tiporoles').val(),
				csrfmiddlewaretoken:  token,
			},
			success:function(server_data){
				error=server_data.err_msg;
				if(error==""){
					solicitudes=server_data.data.solicitudes;
					var array_tiene = [];
					var array_quedan = [];
					var array_eliminados = [];
					$('tbody').children('tr').each(function(){
						var conditional = false
						var tr=$(this).attr('id');
						var i=0;
						var trs = parseInt(tr);
						$.each(solicitudes,function(){
							if(solicitudes[i]==trs){
								conditional=true
							}
							i+=1;
						});
						array_tiene.push(trs);
						if(conditional==true){
							array_quedan.push(trs);
						}
					});
					array_eliminados= $(array_tiene).not(array_quedan).get();
					$.each(array_eliminados, function(v){
						$('tbody').children('#'+array_eliminados[v]+'').hide();
					});
					$('#row-buscar').html('');
					if (bandeja == 'entrada_portal' || bandeja == 'categorizacion_reporte' || bandeja == 'gestion_casos' || bandeja == 'historial_prestador'){
						if($('.categorizacion_reporte').attr('tiporol')!=undefined || $('.entrada_portal').attr('tiporol')!=undefined || $('.gestion_casos').attr('tiporol')!=undefined || $('.historial_prestador').attr('tiporol')!=undefined){
							$("#row-buscar").html(
							'<div class="row">\
							<div class = "col-xs-2">Categorizacion</div>\
							<div class="col-xs-2 col-xs-offset-5">\
							<a \
							href="#"\
							class="btn btn-danger btn-block btn-flat pull-right" \
							id="desactivar-buscar">\
								Limpiar Busqueda&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
							<i class="fa fa-search btn-icon icon-white"></i>\
							</a>\
							</div>\
							<div class="col-xs-3">\
							<a \
							href="#" \
							class="btn btn-info btn-block btn-flat pull-right disabled" \
							id="activar_buscar_modal">\
								Filtrar Reportes\
							<i class="fa fa-search btn-icon icon-white"></i>\
							</a></div></div>');
						}else{
							$('#row-buscar').html('<div class="col-xs-2 col-xs-offset-8">\
							<a href="#" class="btn btn-danger btn-flat col-xs-12" id="desactivar-buscar">Limpiar Busqueda&nbsp;&nbsp;<i class="fa fa-search"></i></a>\
							</div>\
							<div class="col-xs-2"><a href="#" class="btn btn-primary btn-flat col-xs-12 disabled" id="activar_buscar_modal">Buscar&nbsp;&nbsp;<i class="fa fa-search"></i></a></div>');
						}	
					}else{
						$('#row-buscar').html('<div class="col-xs-2 col-xs-offset-8">\
						<a href="#" class="btn btn-danger btn-flat col-xs-12" id="desactivar-buscar">Limpiar Busqueda&nbsp;&nbsp;<i class="fa fa-search"></i></a>\
						</div>\
						<div class="col-xs-2"><a href="#" class="btn btn-primary btn-flat col-xs-12 disabled" id="activar_buscar_modal">Buscar&nbsp;&nbsp;<i class="fa fa-search"></i></a></div>');
					}
					

				}else{
					$('#activar_buscar_modal').removeClass('disabled');
					$('#notificacion-guardado-header').html('');
					$('#notificacion-guardado-header').html('<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\
						<h4 class="modal-title"> Error</h4>');
					$('#notificacion-guardado-header').attr('style',"background-color: #CE4744; color: white;");					
					$('#notificacion-guardado-body').html(
                    '<div class="col-lg-12 text-center">\
                        <h4>La busqueda no coincide con ninguna solicitud</h4>\
                    </div>'
                    );
	                $('#notificacion-guardado').modal();
				}
			},
			error: function(e){
				console.log(e);
			}
       	});
	});
	*/
	
	$('#quitar-busqueda').click(function(){
		$('#activar_buscar_modal').removeClass('disabled');
	});
	$('#quitar-busqueda2').click(function(){
		$('#activar_buscar_modal').removeClass('disabled');
	});

	$(document).on('click', '#desactivar-buscar', function(){
		$('tbody').children('tr').each(function(){
			$(this).show();
		});
		var entrada_portal = $('.entrada_portal');
		var categorizacion_reporte = $('.categorizacion_reporte');
		var gestion_casos = $('.gestion_casos');
		var historial_prestador = $('.historial_prestador');
		if(entrada_portal.length>0 || categorizacion_reporte.length > 0 || gestion_casos.length>0 || historial_prestador.length>0){
			if(categorizacion_reporte.length>0){
				tiporol = $('.categorizacion_reporte').attr('tiporol');
			}else{
				if(entrada_portal.length >0){
					tiporol = $('.entrada_portal').attr('tiporol');
				}else{
					if(gestion_casos.length>0){
						tiporol = $('.gestion_casos').attr('tiporol');
					}else{
						tiporol = $('.historial_prestador').attr('tiporol');
					}
					
				}
			}
			if(tiporol!=undefined){
				$('#row-buscar').html('');
				$('#row-buscar').html(
					'<div class="row">\
					<div class = "col-xs-2">Categorizacion</div>\
					<div class="col-xs-3 col-xs-offset-7">\
					<a \
					href="#" \
					class="btn btn-info btn-block btn-flat" \
					id="activar_buscar_modal">\
						Filtrar Reportes\
					<i class="fa fa-search btn-icon icon-white"></i>\
					</a></div></div>');				
			}else{
				$('#row-buscar').html('');
				$('#row-buscar').html('<div class="col-xs-2 col-xs-offset-10"><a href="#" class="btn btn-primary btn-flat col-xs-12" id="activar_buscar_modal">Buscar&nbsp;&nbsp;<i class="fa fa-search"></i></a></div>');
			}
		}else{
			$('#row-buscar').html('');
			$('#row-buscar').html('<div class="col-xs-2 col-xs-offset-10"><a href="#" class="btn btn-primary btn-flat col-xs-12" id="activar_buscar_modal">Buscar&nbsp;&nbsp;<i class="fa fa-search"></i></a></div>');
		}
		
	});

	/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
	/*~~~~~~ BEGIN Seccion de controles para la interacción con el formulario v1 ~~~~~~*/
	/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/

	/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
	/*~~~~~~ BEGIN Seccion de controles para la interacción con el formulario v2 ~~~~~~*/
	/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/

	$(".iCheck-helper").click(function(){
		
		var parent = $("#super_"+$(this).prev().attr("super"));			
		var id = $(this).parent().parent().attr('id');		

		if($(this).parent().hasClass("checked") && $(this).prev().attr('id') === "activador"){			
			var l ;
			for( var i = 0; i < 5; ++i )
			{	
				l = parent.children("#"+(++id))[0];
				if( l != undefined )
					break;
			}
			$(l).fadeIn('200');			
		
		}else if(!$(this).parent().hasClass("checked") && $(this).prev().attr('id') === "activador")
		{			
			var main_parent = $(this).parent().parent()[0];
			var p = 200;
			while((main_parent = $(main_parent).next()[0]) != undefined)
			{	
				$(main_parent).fadeOut(p);
				p *= 6;
			}
		}
	});

	$("select[id='activador']").change(function(){
		if ($(this).val() == 0)
		{
			var parent = $("#super_"+$(this).attr("super"));			
			var id = $(this).parent().attr('id');
			var l ;
			for( var i = 0; i < 5; ++i )
			{	
				l = parent.children("#"+(++id))[0];				
				if( l != undefined )
					break;
			}		
			$(l).fadeIn('200');		
		}else if( $(this).val() == 1){
			var main_parent = $(this).parent()[0];
			var p = 200;
			while((main_parent = $(main_parent).next()[0]) != undefined)
			{	
				$(main_parent).fadeOut(p);
				p *= 6;
			}
		}		
	});

	/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
	/*~~~~~~ END Seccion de controles para la interacción con el formulario v2 ~~~~~~*/
	/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/


	/*~~~~~~~~  REPORTES Coordinador CT ~~~~~~~~*/
	$("#filtros-busqueda-avanzada").hide();

	$("#btn-buscar-avanzada-filtros").bind('click', function(event) {
	    event.preventDefault();
	    $("#filtros-busqueda-avanzada").toggle("slow");
	});

	$(document).on('ifChecked', 'input', function(event){	
		$(".check-buscador").each(function(){
			$(this).iCheck('uncheck');
			$(this).iCheck('update');
		});
	});
	
	$('#ver-documento-pdf').on('show.bs.modal', function (e) {		
		$('#ver-documento-pdf .modal-content').css('height',$( window ).height());
		$('#ver-documento-pdf .modal-body').css('height',$( window ).height());        
		$('#ver-documento-pdf .modal-body').css('max-height',"80%");
	});
	
    $(".marco-visor-pdf").css('height',"100%");
    $(".marco-visor-pdf").css('width',"100%");

	
    $("#ver-documento-pdf").on('show.bs.modal', function (e) {    	
    	$('html').css("overflow-y","hidden");
    	$('.modal .modal-body').css('overflow-y', 'hidden');
    });
	
   $("#ver-documento-pdf").on('hide.bs.modal', function (e) {
   		$('html').css("overflow-y","visible");
   		$('.modal .modal-body').css('overflow-y', 'visible');    	   	
    });
   
   $(document).on('click', '.cargar-elemento', function(){ 		
   		$('#'+$(this).attr('id')+"-0").trigger('click');
   });   

   $(".cargar-folio").click(function(){   		
   		$('#'+$(this).attr('id')+"-0").trigger('click');
   });

   $("#ingresar-comprobante").on('show.bs.modal', function (e) {
   		$('.modal .modal-body').css('overflow-y', 'hidden');
   		$('.modal .modal-body').css('overflow-x', 'hidden');
   });

   $("#ingresar-folio").on('show.bs.modal', function (e) {
   		$('.modal .modal-body').css('overflow-y', 'hidden');
   		$('.modal .modal-body').css('overflow-x', 'hidden');
   });

   $(".cargar-comprobante").click(function(){   
   		var solicitud = $(this).attr('id');
   		$('.subir-comprobante-form').trigger('reset');
   		$('.msj-error-modal').html('');
        $('.dato-ingresado').attr('placeholder', "Número de comprobante de pago");
        $('.dato-ingresado').attr('id', "comprobante");
        $('#id_sol').attr('value', ''+solicitud+'')
        $('#ingresar-comprobante-Label').html('N&uacute;mero de Comprobante');
        $('.ingresar-comprobante-footer').html('<div class="col-xs-6" data-dismiss="modal">\
            <a href="#" class="btn btn-danger col-xs-12">Cancelar</a>\
            </div>\
            <div class="col-xs-6">\
            <a href="#" id="boton-aceptar-documento" solicitud="'+solicitud+'" class="btn btn-primary btn-subir-comprobante col-xs-12">Aceptar</a>\
            </div>');
   		$('#ingresar-comprobante').modal('show');
   });

	/*~~~~~~~~ Mostrar observaciones de las notificaciones ~~~~~~~~*/

	$('.mostrar_observaciones').click(function(){
	    observacion=$(this).attr('observacion');
	    src=$(this).attr('src');
	    ext=$(this).attr('extension');
	    $('#notificacion-Label').html('Notificaci&oacute;n');
	    $('#notificacion-body').html('');
	    if (ext == 'pdf'){
	    	$(".marco-visor-pdf").attr(
	    	    'src',
	    	    "/categorizacion/verpdf?file=/documents/files/"+src
	    	);
	    	$(".observaciones-pdf").html('<p>'+observacion+'</p>');
	    	$('#ver-documento-pdf').modal();
	    }else{
		    if (src != "None"){
			    $('#notificacion-body').append(
			        '<div class="thumbnail">\
		                <img class="img-responsive imagen-requisito" src="'+src+'" alt="Existen errores en el archivo. Por lo cual no es posible visualizarlo">\
		            </div>'
			    );
			}
			$('#notificacion-body').append(
			        '<div class="col-lg-12 ">\
			            <p>'+observacion+'</p>\
			        </div>'
			    );
		    $('#notificacion-footer').html('\
		    	<div class="col-xs-offset-1 col-xs-10" data-dismiss="modal">\
	            <button class="btn btn-primary col-xs-12">Aceptar</button>\
	        </div>')
		    $('#notificacion').modal({
		        keyboard: false,
		        backdrop: 'static'
		    });
		  }
	});

	/*~~~~~~~~ Mostrar Folio de LSR ~~~~~~~~*/
    $(document).on('click', '.ver-folio', function(){
        var id_folio = $(this).attr('id');
        var folio = $(this).attr('folio');
        if (folio.split(".")[1] == 'pdf'){
        	$(".marco-visor-pdf").attr(
        	    'src',
        	    "/categorizacion/verpdf?file="+folio
        	);
        	$('#ver-documento-pdf .modal-footer').html('');
        	//$('#ver-folios-modal').modal('hide');
        	$('#ver-documento-pdf').modal();
        }else{
	        $('#visualizar_modal_titulo').html('Folio '+id_folio+'');
	        $('.imagen-requisito').attr('src', folio);
	        //$('#ver-folios-modal').modal('hide');
	        $('#visualizar_modal').modal('show');
	    }
    });

//});

 /*-------------------  INICIO CODIGO PARA ENVIAR LA INFORMACION AL SERVIDOR  ------------------------*/
        
        var options = { 
            //beforeSubmit:  showRequest,  // pre-submit callback 
            url:       '',         // override for form's 'action' attribute 
            type:      'post',        // 'get' or 'post', override for form's 'method' attribute
            success: function(server_data) {
            	//id = $('.btn-devolver-obs').attr("solicitud_id");
            	id= $('#form_datos_comp').attr('id_solicitud');
                console.debug(server_data);
                estado = server_data.estado;
                descripcion = server_data.descripcion;
                if (!$('#form_datos_comp').attr('no_deshabilitar')){
                	$('.menu_'+id).addClass('disabled');
                }
                $('#estatus_'+id).html('<label data-toggle="tooltip" title="'+descripcion+'" class="label label-warning etiqueta-estatus">'+estado+'</label>');
                $('#notificacion-guardado-body').html(
                    '<div class="col-lg-12 text-center">\
                        <h4>'+$('#form_datos_comp').attr('respuesta')+'</h4>\
                    </div>'
                    );
                $('#notificacion-guardado').modal();
            },
            error:  function(xhr, textStatus, errorThrown) {
        		$('#notificacion-guardado-body').html(
        		    '<div class="col-lg-12 text-center">\
        		        <h4>'+xhr.responseText+'</h4>\
        		    </div>'
        		    );
        		$('#notificacion-guardado').modal();
            	
                //alert('Please report this error: '+errorThrown+xhr.status+xhr.responseText);
            }, 
            //dataType:  null        // 'xml', 'script', or 'json' (expected server response type) 
            //clearForm: true        // clear all form fields after successful submit 
            //resetForm: true        // reset the form after successful submit 
            //timeout:   3000 
        };

        $(document).on('submit', '#form_datos_comp', function(e){
        	e.preventDefault();
        	e.stopImmediatePropagation();
        	options["url"] = $('#form_datos_comp').attr('action');
        	$(this).ajaxSubmit(options); 
        	return true;
        });

        $(document).on('change', '#clasificaciones', function(){
        	$('#categorias').html('<option value="">--Seleccione--</option>');
        	if($(this).val()!=""){
        	    $.ajax({
        	        type: 'POST',
        	        url: '/categorizacion/funcionario/bandeja/buscar',
        	        data:{
        	            'clasificacion_buscar':$(this).val(),
        	            csrfmiddlewaretoken:  token,
        	    },success: function(server_data) {
        	    	$('#categorias').attr('disabled', false);
        	    	$.each(server_data.data.categorias, function(key, value){
        	    		$('#categorias').append('<option value="'+key+'">\
        	    			'+value+'</option>');
        	    	})
        	    },error: function(server_data) {
        	        $('.msj-error-modal').html('<div class="alert alert-warning alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button><strong>Error:&nbsp;</strong>No es posible ubicar dicha clasificaci&oacute;n</div>');
        	        }
        	    });
        	}else{
        	    $('#categorias').attr('disabled', true);
        	}
        });
        /*$('#form_datos_comp').submit(function(e){ 
			e.preventDefault();
			e.stopImmediatePropagation();

			console.log("g1");
			// inside event callbacks 'this' is the DOM element so we first 
			// wrap it in a jQuery object and then invoke ajaxSubmit 

			options["url"] = '/categorizacion/funcionario/devolverobservaciones';

			//$(this).ajaxSubmit(options); 
			console.log("g2");
			// !!! Important !!! 
			// always return false to prevent standard browser submit and page navigation 
			return false; 
        });*/
});
/*-------------------  INICIO DE LAS FUNCIONES PARA ENVIAR LA INFORMACION AL SERVIDOR  ------------------------

function showRequest(formData, jqForm, options){ 
    // formData is an array; here we use $.param to convert it to a string to display it 
    // but the form plugin does this for you automatically when it submits the data 
    /*
    var queryString = $.param(formData);
    console.log(queryString); 
 	
    $('#cargando').html('<div><img src="/static/img/ajax-loader.gif"/></div>');
    alert('About to submit: \n\n' + queryString);  
    // here we could return false to prevent the form from being submitted; 
    // returning anything other than false will allow the form submit to continue 
    return true; 
} 
 
// post-submit callback 
function showResponse(server_data){ 
    // for normal html responses, the first argument to the success callback 
    // is the XMLHttpRequest object's responseText property 
 
    // if the ajaxSubmit method was passed an Options Object with the dataType 
    // property set to 'xml' then the first argument to the success callback 
    // is the XMLHttpRequest object's responseXML property 
 
    // if the ajaxSubmit method was passed an Options Object with the dataType 
    // property set to 'json' then the first argument to the success callback 
    // is the json data object returned by the server 
 
    /*alert('status: ' + statusText + '\n\nresponseText: \n' + responseText + 
        '\n\nThe output div should have already been updated with the responseText.');*/
        /*console.log(responseText);
        estado=server_data.estado;
        descripcion=server_data.descripcion;
        $('.menu_'+id).addClass('disabled');
        $('#estatus_'+id).html('<label data-toggle="tooltip" title="'+descripcion+'" class="label label-warning etiqueta-estatus">'+estado+'</label>');
        $('#notificacion-guardado-body').html(
            '<div class="col-lg-12 text-center">\
                <h4>Se ha devuelto la solicitud con sus observaciones.</h4>\
            </div>'
            );
        $('#notificacion-guardado').modal();

function showError(responseText, statusText, xhr, $form){ 
    // for normal html responses, the first argument to the success callback 
    // is the XMLHttpRequest object's responseText property 
 
    // if the ajaxSubmit method was passed an Options Object with the dataType 
    // property set to 'xml' then the first argument to the success callback 
    // is the XMLHttpRequest object's responseXML property 
 
    // if the ajaxSubmit method was passed an Options Object with the dataType 
    // property set to 'json' then the first argument to the success callback 
    // is the json data object returned by the server 
        
   /*alert(form.childNodes[0]);
        alert('status: ' + statusText + '\n\nresponseText: \n' + responseText + 
        '\n\nThe output div should have already been updated with the responseText.');
        $('.error_cont').html('');
    $.each(responseText, function(key, value){
    console.log(key,value.message);
                    sel = key + '_error';
                    $('#'+sel).html(value.message);
    });
        alert("ERROR");
   //$('#cargando').fadeIn(1000).html("");

    /*window.location.replace("/licencias/pst/solicitudes/"); 
} */