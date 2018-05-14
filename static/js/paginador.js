$(function(){
	
	var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
	var url;

	function llamar_paginador(p, s, url){
		
		$.ajax({
			type: 'POST',
			url: url,
			data: {
				'p': p,
				's': s,
				csrfmiddlewaretoken:  token,
			},
			success: function(server_data) {
				$(".root_paginator").attr('p',server_data.data.pagina);
				var sdata = server_data.data.modelo;
				var version = undefined;
				var no_editable = Boolean(server_data.no_editable);
				var no_insertar = Boolean(server_data.no_insertar);
				var no_eliminable = Boolean(server_data.no_eliminable);

				$('.cabecera_tabla').html('');
				$('.cuerpo_tabla').html('');
				$('#prev').css('visibility', 'hidden');
				$('#next').css('visibility', 'hidden');

				if(sdata.length){
					
					$.each(sdata[0], function(key){
						if (key != 'id' && key != 'version_actual')
							$('.cabecera_tabla').append('<th >'+key.replace(/^[a-z]/, function(m){ return m.toUpperCase() }) +'</th>')
					});

					$('.cabecera_tabla').append('<th>Opciones</th>')				
					
					urledit = url.split('/');

					$.each(sdata, function(key, values){
						elemento_id = values.id;
						$('.cuerpo_tabla').append('<tr id="objeto_'+elemento_id+'"></tr>');

						$.each(values, function(key, value){
							if(key != 'id'){
								if(key === 'Estatus' && urledit[4] === 'funcionario'){
									if(value === 'Habilitado')
									{
									$('#objeto_'+elemento_id).append('<td> \
										<label class="label label-success etiqueta-estatus">'+value+'</td>');
										
									}else{
									$('#objeto_'+elemento_id).append('<td> \
										<label class="label label-danger etiqueta-estatus">'+value+'</td>');	
									}
								}else if(key === 'Versión' && urledit[4] === 'tabulador'){
									version = value;
								}else if(key === 'version_actual' && urledit[4] === 'tabulador'){
									if (value)
									{
										$('#objeto_'+elemento_id).append('<td><label class="label label-success etiqueta-estatus">v.'+version+'</td>');
									}else{
										$('#objeto_'+elemento_id).append('<td><label class="label label-default etiqueta-estatus">v.'+version+'</td>');
									}
								}else if(key === 'Representación' && urledit[4] === 'tipoicono'){
									$('#objeto_'+elemento_id).append('<td><i class="fa '+value+'"></i></td>');
								}else{
									$('#objeto_'+elemento_id).append('<td>'+value+'</td>');
								}
							}
						});					
						
						options_to_append = "<td>"
						/*
						*
						*	Opcion de edicion de recurso
						*
						**/
						if(!no_editable){
							options_to_append += '<a \
							href="/categorizacion/administrador/'+urledit[4]+'/'+elemento_id+'/editar/" \
							class="btn btn-info"> \
							<i class="fa fa-edit icon-white"></i> \
							</a>';
						}

						/*
						*
						*	Opcion de eliminacion de un recurso
						*
						**/
						if (!no_eliminable){
							options_to_append += '&nbsp;\
							<a class="eliminar btn btn-info" elemento_id="'+elemento_id+'">\
							<i class="fa fa-trash-o icon-white"></i>\
							</a>';							
						}

						/*
						*
						*	Vista previa del tabulador
						*
						*/
						if(urledit[4] === 'tabulador'){
							options_to_append += '&nbsp;\
							<a \
							class="ver btn btn-info" elemento_id="'+elemento_id+'"\
							href="/categorizacion/administrador/tabulador/vista/'+elemento_id+'" \
							>\
							<i class="fa fa-eye icon-white"></i>\
							</a>';
						}

						options_to_append += '</td>'
						$('#objeto_'+elemento_id).append(options_to_append);
					});
					
					pag=server_data.data.pagina;
					num_pag=server_data.data.num_pag;
					if (pag>0){
						$('#prev').css('visibility', 'visible');	
					}
					else {
						$('#prev').css('visibility', 'hidden');
					}
					
					if (pag==num_pag-1){
						$('#next').css('visibility', 'hidden');
					}
					else{
						$('#next').css('visibility', 'visible');
					}		
				}
				else{
					$('.cabecera_tabla').append('<th>No hay recursos para mostrar</th>');					
				}

				url_split = url.split('/');
				$('.agregar-btn').html('<button class="col-xs-12 btn btn-flat btn-primary crear"  url="'+server_data.data.url_agregar+'" >Agregar&nbsp; <i class="fa fa-plus"></i></button>');
				$('.crear').attr('url', server_data.data.url_agregar);
				$('.migas').html('<li>\
					<a href="/categorizacion/administrador/">\
					Inicio</a>\
					</li> \
					<li class="active">\
					<i class="fa fa-th-large"></i>&nbsp;&nbsp;'+server_data.data.nombre_modelo+'</li>');

				if('nombre_modelo' in server_data.data){
					$('.titulo-recurso').html(server_data.data.nombre_modelo);
				}
				
				window.history.pushState("", "", '/'+url_split[1]+'/'+url_split[2]+'/'+url_split[4]);
				
				if(!no_insertar){
					url_split = url.split('/');
					$('.agregar-btn').html('<button class="col-xs-12 btn btn-flat  btn-primary crear"  url="'+server_data.data.url_agregar+'" >Agregar&nbsp; <i class="fa fa-plus"></i></button>');
					window.history.pushState("", "", '/'+url_split[1]+'/'+url_split[2]+'/'+url_split[4]);
				}else{
					$('.agregar-btn').html('');					
				}
			
		},
		error: function(xhr, textStatus, errorThrown) {
			$('#notificacion-general-Label').html('Problemas del lado del servidor');
			$('#notificacion-general-body').html(
			    '<div class="col-lg-12 text-center">\
			        <h4>Hemos encontrado algunos problemas los cuales nos impiden establecer conexion con el servidor</h4>\
			    </div>'
			);
			$('#notificacion-general-footer').html(
			    '<div class="col-xs-offset-4 col-xs-4" data-dismiss="modal">\
			        <a href="#" class="btn btn-danger col-xs-12">Cerrar</a>\
			    </div>'
			);
			$('#notificacion-general').modal({});
			
			console.log(errorThrown);
			console.log(xhr.status);
			console.log(xhr.responseText);
		}
		});
	}

	if ($('#url_ajax').length){
		url = $('#url_ajax').attr('url');

		llamar_paginador(0, '', url);
	}

	$(".pagina, .cargador_recursos").click(function(e){				
		
		e.preventDefault();
		e.stopImmediatePropagation();
		$('#esconder').hide();
		url = $(this).attr('url');
		$("button.pagina").each(function(){
			$(this).attr("url",url);
		});

		p = $(this).parent().attr('p');
		s = $(this).attr('s');
		url = $(this).attr('url');
		llamar_paginador(p, s, url);
	});

	$(document).on('click','.eliminar',function(){
        $('#notificacion-general-Label').html('Confirmar eliminaci&oacute;n');
        $('#notificacion-general-body').html(
            '<div class="col-lg-12 text-center">\
                <h4>¿Est&aacute; seguro que desea eliminar este recurso?</h4>\
            </div>'
        );
        $('#notificacion-general-footer').html(
            '<div class="col-xs-6" data-dismiss="modal">\
                <a href="#" class="btn btn-danger col-xs-12">Cancelar</a>\
            </div>\
            <div class="col-xs-6" data-dismiss="modal">\
                <a href="#" elemento_id="'+$(this).attr("elemento_id")+'" class="btn btn-primary col-xs-12 confirmar_eliminar">Aceptar</a>\
            </div>'
        );
        $('#notificacion-general').modal();
	});

	$(document).on('click','.confirmar_eliminar',function(){

		$.ajax({
			type: 'POST',
			url: '/categorizacion/administrador/'+urledit[4]+'/eliminar',
			data:{
			'id':$(this).attr("elemento_id"),
			csrfmiddlewaretoken:  token},
			success: function(server_data) {
				error = server_data.err_msg;
				$('#notificacion-general').modal('hide');
				if (server_data.success.length!=0){
					$('#objeto_'+server_data.data.elemento_id).remove();
        			$('#notificacion-guardado-body').html(
			            '<div class="col-lg-12 text-center">\
			                <h4>El recurso ha sido eliminado</h4>\
			            </div>'
			        );
        			$('#notificacion-guardado').modal();
				}else{
					if(server_data.data == "funcionario"){
						if(error!=""){
							$('#notificacion-guardado-header').html('');
							$('#notificacion-guardado-header').html('<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\
							<h4 class="modal-title"> Error</h4>');
							$('#notificacion-guardado-header').attr('style',"background-color: #CE4744; color: white;");
						
							$('#notificacion-guardado-body').html(
		                        '<div class="col-lg-12 text-center">\
		                            <h4>No se encuentra el funcionario de reemplazo</h4>\
		                        </div>'
		                        );
		                	$('#notificacion-guardado').modal();
						}
					}
					
				};
			},
			error: function(xhr, textStatus, errorThrown) {
				alert('Please report this error: '+errorThrown+xhr.status+xhr.responseText);
			}
		});
	});

//------------------------ Paginador General -----------------------------------\\
/*
	function paginador_general(p,s,tipouser){
		$.ajax({
			type: 'GET',
			url: "{% url 'bandeja' %}",
			data: {
				'p': p,
				's': s,
				'tipouser': tipouser,
				csrfmiddlewaretoken:  token,
			},
			success: function(server_data){
				$('.root_paginator').attr('p', server_data.data.p);
				console.log($('.root_paginator').attr('p'));
			},	
		});

	}	

	$('.paginar' '.cargar_recurso').click(function(e){
		console.log("HEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEELLLLLLLLLLLLLLLLOOOOOOOOOOOOOOOOOOOOOOO")
		e.stopImmediatePropagation();
		e.preventDefault();
		tipouser = $(this).attr('tipouser');
		$("button.paginar").each(function(){
			$(this).attr("tipouser",tipouser);
		});

		p = $(this).parent().attr('p');
		s = $(this).attr('s');
		tipouser = $(this).attr('tipouser');
		paginador_general(p, s, tipouser);
	})
*/
});


