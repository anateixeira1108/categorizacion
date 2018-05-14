/* add-tabulator.js */

/*
|
|	Modulo de agregacion de tabuladores para
|	el sistema de categorizacion (v.1.0)
|
|	AngularJS Implemetation
|
*/
(function(){

	/*Eliminar scroll dentro de los paneles para permitir la visibilidad de los elementos*/

	$('.tab-pane').css(
		{
		  'bottom': '0',
		  'left': '0',
		  'overflow': 'auto',
		  'position': 'absolute',
		  'right': '0',
		  'top': '9.3%'
		}
	);

	/* Implementacion de arbol para manejo de estructura de cookies */

	function Tree(id, name, content, state, type, extra ) {

	    var cached_this = this;
	    cached_this.id = id;
	    cached_this.name = name;
	    cached_this.state = state;
	    cached_this.type = type;
	    cached_this.content = content;
	    cached_this.children = [];
	    cached_this.extra = extra;
	    cached_this.parent = undefined;

	    cached_this.isEmpty = function(){
	    	return cached_this.id === undefined;
	    }

	    cached_this.childrenCounter = function(){
	    	return cached_this.children.length;
	    }

	    cached_this.setParentNode = function(node) {
	        if( cached_this !== undefined ){
	            cached_this.parent = {'id': node.id, 'type': node.type};
	        }
	    }

	    cached_this.getParentNode = function() {
	        return cached_this !== undefined? cached_this.parent : undefined;
	    }

	    cached_this.addChild = function(node) {
	        if( cached_this !== undefined ){
	            node.setParentNode(cached_this);
	            cached_this.children.push(node);
	        }
	    }

	    cached_this.getChildren = function() {
	        return cached_this !== undefined? cached_this.children : undefined;
	    }

	    cached_this.removeChildren = function() {
	        if(cached_this!== undefined){                  
	            delete cached_this.id;
	            delete cached_this.name;
	            delete cached_this.state;
	            delete cached_this.content;
	            delete cached_this.children;
	            delete cached_this.parent;
	            delete cached_this.type;
	            delete cached_this.extra;
	            delete cached_this;
	        }
	    }

	    cached_this.render = function(ignore_data){
	        if( cached_this !== undefined && cached_this.children !== undefined ){

	            var data = ['data has been ignored'];
	            if (ignore_data !== undefined){
	                data = [];
	                for ( var i =0; i<cached_this.children.length; ++i){
	                    data.push(cached_this.children[i].render(false));
	                }
	            }
	            return {
	                'id': cached_this.id, 
	                'name': cached_this.name, 
	                'state': cached_this.state,
	                'content': cached_this.content,
	                'children': data,
	                'parent': cached_this.parent,
	                'extra': cached_this.extra,
	                'type': cached_this.type
	            }
	        }   
	    }

	    cached_this.addChildByIndex = function(id, type, node){
	        if( cached_this !== undefined ){
	            if( cached_this.id == id && cached_this.type == type )
	            {
	                cached_this.addChild(node);
	            }else{
	                for ( var i =0; i<cached_this.children.length; ++i ){
	                    cached_this.children[i].addChildByIndex( id, type, node );
	                }
	            }
	        }
	    }
	    cached_this.notNullChildren = function(id,type){
	    	if(cached_this !== undefined ){
	    		if( cached_this.id == id && cached_this.type == type ){
	    			console.log("entrando en la condicion del notNullChildren")
	    			cached_this.children = []; 
	    		}else{
	    			for ( var i =0;  i< cached_this.children.length; ++i ){
	                    cached_this.children[i].notNullChildren( id, type );
	                }
	    		}
	    	}	
	    }
	    cached_this.deleteByIndex = function( id, type)
	    {
	        if(cached_this !== undefined ){
	            if( cached_this.id == id && cached_this.type == type )
	            {
	                if(cached_this.getParentNode() !== undefined ){
	                    var aux = cached_this.parent;
	                    cached_this.removeChildren();
	                    return aux;
	                }else{
	                    cached_this.removeChildren();
	                    delete cached_this.id;
	                    delete cached_this.name;
	                    delete cached_this.state;
	                    delete cached_this.content;
	                    delete cached_this.children;
	                    delete cached_this.parent;
	                    delete cached_this.type;
	                    delete cached_this.extra;
	                    delete cached_this;
	                }
	            }else{
	            	var dummy = undefined;
	                for ( var i =0;  i< cached_this.children.length && dummy == undefined; ++i ){
	                    dummy = cached_this.children[i].deleteByIndex( id, type );
	                }
	                return dummy;
	            }
	        }
	    }

	    cached_this.load = function(obj, pid, ptype, uids, old_ids, parent_id){
	    	/*
	    	*
	    	* uids: { old_id, old_type, new_id }
	    	*
	    	*/
	        if( cached_this.id === undefined)
	        {  
	        	var entity = $.isArray( obj )? obj[0] : obj;
	            cached_this.id = entity.id ;
	            cached_this.type = entity.type;
	           	 
	            if(uids !== undefined && cached_this.id == uids.old_id && cached_this.type == uids.old_type)
	            {
	            	cached_this.id = uids.new_id;
	            	// Se actualizan los elementos de interfaz que podrian 
	            	// resultar afectados de la operacion de guardado
	            	console.log("from :"+uids.old_id+" "+uids.old_type);
	            	console.log("to :"+uids.new_id+" "+uids.old_type);
	            	console.log($("[id="+uids.old_id+"][type="+uids.old_type+"]"));

	            	$("[id="+uids.old_id+"][type="+uids.old_type+"]").each(function(){
	            		$(this).attr("id",uids.new_id);
	            	});
	            }

	            cached_this.name = entity.name;
	            cached_this.state = entity.state;
	            cached_this.extra = entity.extra;
	            if(old_ids !=undefined){
	            	cached_this.state="done";
	            }          
	            cached_this.load (entity.children, cached_this.id, cached_this.type,undefined,old_ids);
	        }else{
	        	var conditional = false;           
	            for (var i = 0; obj!==undefined && i < obj.length; ++i){

	            	if(obj[i].state != "delete"){
		            	if(old_ids!=undefined){
		            		if (obj[i].state == "added"){
		            			obj[i].state = "done";	
		            		}
		            		for(var f=0; f<old_ids.length; ++f){
		            			if(obj[i].id == old_ids[f].pid && obj[i].type == old_ids[f].type){
		            				
		            				obj[i].id = old_ids[f].nid;			            				
		            				
		            				// Actualizacion mejorada de los elementos dentro de la 
		            				// interfaz de usuario
		            				$("[id="+old_ids[f].pid+"][type="+old_ids[f].type+"]").each(function(){
		            					$(this).attr("id",old_ids[f].nid);
		            				});

		            				//Cambiar el Parent
		            				if(parent_id != undefined){
		            					obj[i].parent.id = parent_id;
		            				}
		            				parent_id = obj[i].id;

		            				var t = old_ids.indexOf(old_ids[f]);
		            				if(t!=-1){
		            					old_ids.splice(t,1);
		            					conditional = true;
		            				}
		            				break;
		            			}		
	 	            		}
	 	            		if(conditional == false){
	 	            			parent_id = undefined;
	 	            		}
		            	}
		                cached_this.addChildByIndex(
		                    pid,
		                    ptype, 
		                    new Tree(
		                    	uids !== undefined && obj[i].id == uids.old_id && obj[i].type == uids.old_type ? uids.new_id : obj[i].id, 
		                    	obj[i].name, 
		                    	obj[i].content, 
		                    	obj[i].state, 
		                    	obj[i].type, 
		                    	obj[i].extra
		                    )
		            	)
		            
		            	if(old_ids!=undefined){
		            		cached_this.load( obj[i].children, obj[i].id, obj[i].type, undefined, old_ids, parent_id);
		            	}else{
		            		cached_this.load( obj[i].children, obj[i].id, obj[i].type);	
		            	}
	            	}                   
	            }
	        }
	    }

	    cached_this.conditionalTree = function(obj, id, type, posneg, counter, tabcurrent, conditionfirst){
    		if(obj.extra.subtype == "C"){
    			//console.log("Entro en condicional")
    			var aux = '';    			
    			var options = obj.content.options;
    			var options_val = obj.content.options_val;
    			var t=0
    			for(var i=0;i<options.length;i+=2){
    				options = options.slice(0,i+1).concat(options_val[t]).concat(options.slice(i+1,options.length))
    				t+=1
    			}
    			
    			if (conditionfirst == false){
    				var data = JSON.parse(localStorage.getItem(tabcurrent));
    				data.ss +=1;
    				obj.id = data.ss
    				localStorage.setItem(tabcurrent, JSON.stringify(data));
    			}

    			if(posneg=="P"){
    				aux = "Condici&oacute;n Positiva"
    			}else if(posneg=="N"){
    				aux = "Condici&oacute;n Negativa"
    			}
				ss_counter = $("."+currentTab+"-body .panel[id="+id+"][type="+type+"]").find(".panel-body").eq(0).children(".panel[type=SS],.panel[type=S]").length+1;				
				// ss_counter = $("."+currentTab+"-body .panel[id="+id+"][type="+type+"] .panel[type=SS]").length + $("."+currentTab+"-body .panel[id="+id+"][type="+type+"] .panel[type=S]").length+1;
    			parent_counter = $("[id="+id+"][type="+type+"]").attr("element_fisical_idenfitier");

	    		$("[id="+id+"][type="+type+"] .panel-body").eq(0).append(
					_.template($("#subseccion-conditional-template").html())({
						"condicion":aux,
						"name": obj.name,
						"id": obj.id,
						"body": options,
						"parent_counter": parent_counter,
						"counter": ss_counter
					})
				);

				$(".panel_subsec[id="+obj.id+"][type='SS'] .panel_conditional input").iCheck({
				    radioClass: 'iradio_minimal',
				    increaseArea: '20%'
				})
	    		for(var i=0;i<obj.children.length;i++){
	    			if(i<parseInt(obj.content.extra[0])){
	    				cached_this.conditionalTree(obj.children[i],obj.id,obj.type,"P",counter+=1,tabcurrent,conditionfirst);
	    			}else if(i<parseInt(obj.content.extra[0])+parseInt(obj.content.extra[1])){
	    				cached_this.conditionalTree(obj.children[i],obj.id,obj.type,"N",counter+=1,tabcurrent,conditionfirst);
	    			}
	    		}
	    	}else{
	    		if(conditionfirst == false){
					var data = JSON.parse(localStorage.getItem(tabcurrent));
    				data.ss +=1;
    				obj.id = data.ss;
    				localStorage.setItem(tabcurrent, JSON.stringify(data));
    			}
	    		if(obj.content.options_val){
    				var options = obj.content.options;
	    			var options_val = obj.content.options_val;
	    			var t=0
	    			for(var i=0;i<options.length;i+=2){
	    				options = options.slice(0,i+1).concat(options_val[t]).concat(options.slice(i+1,options.length))
	    				t+=1
	    			}
    				conditionalTemplate(obj,id,type,posneg,options);
	    		}else if(obj.content.unit_val){
	    			conditionalTemplate(obj,id,type,posneg,obj.content.unit_val);
	    		}else if(obj.content.repetition_star){
	    			conditionalTemplate(obj,id,type,posneg,obj.content.repetition_star);
	    		}else if(obj.content.formula_string){
	    			conditionalTemplate(obj,id,type,posneg,obj.content.formula_string);
	    		}else{
	    			conditionalTemplate(obj,id,type,posneg,undefined);
	    		}
				for(var i=0;i<obj.children.length;i++){
    				conditionalTree(obj.children[i],obj.id,obj.type,posneg,counter+=1,tabcurrent,conditionfirst);
	    		}	
	    	}
    	}

    	cached_this.getElementByIdType = function(id, type, update, uobj){
    		if( id != undefined && type != undefined )
    		{
    			if( cached_this.id == id && cached_this.type == type )
    			{
    				if (update != undefined && update == true)
    				{
    					// Perform update operation in case of being requested
						$.each(uobj, function(k,v){
							console.log(k);
							cached_this[k] = v;
						});
     				}

    				return cached_this;
    			}else{
    				var r = undefined;
    				for(var i =0;  i< cached_this.children.length && r == undefined; ++i){
	            		r = cached_this.children[i].getElementByIdType(id, type, update, uobj);	            		
	            	}
	            	return r;
    			}
    		}else{
    			console.log("type and id must not be undefined");
    		}
    	}

    	cached_this.editNode = function(id, type, obj){
    		//Editar el elemento seleccionado con el objeto pasado
    		//por parametro
    		if(cached_this.id === id  && cached_this.type === type){
			    cached_this.state = cached_this.state !== "added" ? "edited" : cached_this.state;
			    if(obj.name!==undefined){cached_this.name = obj.name;}
			    if(obj.content!==undefined){cached_this.content = obj.content;}
			    if(obj.extra!==undefined){cached_this.extra = obj.extra;}
    		}else{
				for(var i =0; cached_this.children !== undefined &&  i<cached_this.children.length; ++i)
				{
					cached_this.children[i].editNode(id, type, obj);
				}
			}
    	}
	}


	var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
	
	// Check for cookies support	
	if ( typeof(Storage) !== "undefined"){

		var selectid = [];
		var globalselect = [];
		var globalselectneg = [];
		var arbolaux = new Tree();
		var is_initial_condition_added = false;

		if(!$("#constructor_core").length){
			localStorage.setItem('main-config-cookie', "[]");
			localStorage.setItem('documental-req-cookie', "[]");
			localStorage.setItem('specific-values-cookie', "[]");
			localStorage.setItem('basic-req', "[]");
			localStorage.setItem('specific-req', "[]");
			localStorage.setItem('cookies-ids', "[]");
		}

		var is_modal_up = "";
		var currentCounter = 0;
		var currentTab = "";
		var configSaved = $("#constructor_core").length && true;
		var app = angular.module('control-tabulador', ['ngCookies']);
			
		// AngularJS Section		
		app.controller('GlobalController',
			[
				'$scope', 
				'$http',
				'$compile', 
				'$cookieStore',
				function($scope, $http, $compile, $cookieStore, $timeout){

					// Handles the add process 
					$scope.agregarElemento = function(){
						globaldef = [];
						selectid = [];
						globalselect = [];
						globalselectneg = [];
						is_initial_condition_added = false;
						
						/*  
							Movimientos dentro de las respuestas condicionales
						*/							
						moves_tree = new Tree();

						// console.log(globaldef.length);
						// console.log(selectid.length);
						// console.log(globalselect.length);
						// console.log(globalselectneg.length);
						
						$( "#mutable-form-container" ).html('');
						$( "#modal-agregar-elemento-body" ).show();
						$( "#mutable-form-container" ).hide();
						
						if($scope.currentTab === 'specific-values-cookie')
						{
							title = $("#modal-agregar-elemento-title").html();
							
							$("#modal-agregar-elemento-title").html(
								"<i class='fa fa-plus'></i>&nbsp;Agregar Elemento&nbsp;<i class='fa fa-angle-right'></i>&nbsp;Datos Espec&iacute;ficos"
							);
							
							// Se construye el formulario de elementos valor especifico 
							var valor_categoria = _.template($("#valor-por-categoria").html())(
								{
									'categories': parseInt($("#tipo-prestador").find("option:selected").attr("pstcategorie")),
									'values': [],
									'extra_class': '',
									'editable': true,
									'icon': $("#tipo-prestador").find("option:selected").attr("icon")
								}
							);

							$("#modal-agregar-elemento-body").html(
								_.template($("#specific_values_template").html())(
									{
										'extra_content': valor_categoria
									}
								)
							);

					  		$('#modal-agregar-contenido-footer').html(
					  			$("#specific_values_footer_template").html()
					  		);

					  		$("#modal-agregar-elemento-body input[type=checkbox]").iCheck({
			    				checkboxClass: 'icheckbox_minimal',	
			    				radioClass: 'iradio_minimal',
			    				increaseArea: '20%'
							});
							
							$("#modal-agregar-elemento").modal();						
							is_modal_up = 'basic-data';
							currentCounter = ++$scope.currentCounter ;

						}else if( $scope.currentTab === 'documental-req' ){

							title = $("#modal-agregar-elemento-title").html();
							
							$("#modal-agregar-elemento-title").html(
								"<i class='fa fa-plus'></i>&nbsp;Agregar Elemento&nbsp;<i class='fa  fa-angle-right'></i>&nbsp;Requisitos Documentales"
							);

						  	$("#modal-agregar-elemento-body").html($("#documentals-section-template").html());
	
					  		$('#modal-agregar-contenido-footer').html(					  	
					  			"<div class='col-xs-6'><a \
					  			  class='col-xs-12 btn btn-danger btn-flat' data-dismiss='modal'>\
					  			  Cancelar\
					  			</a></div>\
					  			<div class='col-xs-6'><a \
					  			  class='col-xs-12 btn btn-primary btn-flat add-documental-req'>\
					  			  Agregar\
					  			</a></div>"						  	
					  		);
					  		$('#modal-agregar-contenido-footer').removeAttr('data-dismiss');

							$("#modal-agregar-elemento").modal();						
							is_modal_up = 'documental-req';
							currentCounter = ++$scope.currentCounter ;

						}else{
							$http.get('tipos-respuesta').success(function(data, status, headers, config) {
							  	data = JSON.parse(data.data);
							  	var title = $scope.currentTab === 'basic-req' ? "Requisitos B&aacute;sicos" : "Requisitos Espec&iacute;ficos";

								icons = {
									'D': 'dot-circle-o',
									'E':'ellipsis-h',
									'R':'list-ol',																		
									'C':'question-circle',
									'RP':'question-circle',
									'F': 'superscript',
									'REP': 'repeat',
								}

							  	var template = _.template( $("#element-template").html());
							  	$("#modal-agregar-elemento-body").html('');

							  	var e = $(".choosen-one").length ? $($(".choosen-one")[0]).parents(".panel").attr("type"):'';
							  	
							  	if( e === '' ){
							  		var acum = 0.0;	
							  		
							  		$(".percent").each(function(){
							  			acum += parseFloat( $(this).html() );
							  		});
					  		  		if( acum && 100.0 - acum <= 0 && $scope.currentTab === 'specific-req'){
					  				  	$("#modal-agregar-elemento-body").append(
					  				  		_.template($("#notification-zone").html())(
					  				  		{
					  				  			'msg': "Ya ha asignado el 100% disponible en aspectos fundamentales por lo que no es posible realizar la creaci&oacute;n de uno adicional."
					  				  		})
					  				  	);
					  			  	}else{					  			  		
									  	$("#modal-agregar-elemento-body").append(
									  		template({
									  			"name": "Aspecto Fundamental",
									  			"code": "book",
									  			"id": "E_ASPECTOF"
									  		})
									  	);
					  			  	}
								}

							  	if( e !== '' ){
							  		if (e === "AF" || e === "S"){
									  	$("#modal-agregar-elemento-body").append(
									  		template({
									  			"name": "Secci&oacute;n",
									  			"code": "book",
									  			"id": "E_SECCION"
									  		})
									  	);
									}
									if( e === "S" || e === "SS" ){
										$.each(data, function( i, v ) {
									  		if( _.has(icons,v.fields.codigo) ){
										  		$("#modal-agregar-elemento-body").append(
										  			template({
										  				"name": v.fields.nombre, 
										  				"code": icons[v.fields.codigo],
										  				"id": v.fields.codigo
										  			})
										  		);
										  	}
									  	});
									}
							  	}

							  	$("#modal-agregar-elemento-title").html(
							  		"<i class='fa fa-plus'></i>&nbsp;Agregar Elemento&nbsp;<i class='fa  fa-angle-right'></i>&nbsp;"+title
							  	);

							  	$("#modal-agregar-contenido-footer").html(
							  		"<a \
							  		data-dismiss='modal' \
	          						class='col-xs-12 btn btn-danger btn-flat'> \
	          						Cancelar\
	        						</a>"
							  	);

					  			$('#modal-agregar-elemento').modal({
					  	  			backdrop: 'static',
					  	  			keyboard: false
					  			});

							  	is_modal_up = '*';

							  }).error(function(data, status, headers, config) {
							  	console.log(status);
							  	console.log(data);
							  });
						}
					}

					$scope.tabChanger = function(id){

						$(".zone-selector").each(function(){
							$(this).iCheck('enable');
							$(this).iCheck('uncheck');
							$(this).iCheck('update');

							if($(this).hasClass("choosen-one"))
							{
								$(this).removeClass("choosen-one");
							}
						});

						currentTab = id;
						$scope.currentTab = id;
						$scope.showAdd = id != 'basic-config';
						$scope.currentCounter = (id != 'basic-config' ? parseInt( $('.table-'+id).attr('added-elements') ) : parseInt($('#basic-config').attr('added-elements')));
					}

					$scope.guardarEstructura = function(){
						if($('#form_tab') != "" && $('#form_tab') != undefined){
							
							var cond = false;
							if($('#nombre-tabulador').val() !=undefined && $('#nombre-tabulador').val().length!=0 && $('#nombre-tabulador').val()){
							  	cond = true;
							}else{
								$('#nombre-tabulador').after('<div role="alert" class="alert alert-ajustado alert-warning alert-dismissible error" id="id_nombre-error"><button data-dismiss="alert" class="close" type="button"><span aria-hidden="true">×</span><span class="sr-only">Close</span></button><li>Este campo es obligatorio</li></div>');
							}

							if($('#tipo-prestador').val()!=-1){
								if(cond == true){
									autosave();
									$scope.showAllTabs = configSaved;
								}
							}else{
								$('#tipo-prestador').after('<div role="alert" class="alert alert-ajustado alert-warning alert-dismissible error" id="id_tipo-error"><button data-dismiss="alert" class="close" type="button"><span aria-hidden="true">×</span><span class="sr-only">Close</span></button><li>Este campo es obligatorio</li></div>');
							}
							
						}else{
							autosave();
							$scope.showAllTabs = configSaved;
							console.log($scope.showAllTabs);
						}
					}

					angular.element(document).ready(function($timeout){
						currentTab = 'basic-config';
						configSaved = $("#constructor_core").length && true;
						$scope.showAllTabs = $("#constructor_core").length && true;
						localStorage.setItem('cookies-ids', $("#basic-config").attr('data-cookie-ids') );
						
						if(!$("#constructor_core").length){
							$("#modal-create-choose").modal({
						        keyboard: false,
						        backdrop: 'static'
						    });

						    $(document).on("click", "#all_new_pick", function(){
						    	$("#modal-create-choose").modal("hide");
						    });
						}
					})
				}
			]
		);

		app.controller('PreviewController',
			[
				'$scope', 
				'$http', 
				function($scope, $http){					
					// Handles for the preview process
					$scope.vistaPrevia = function(){
						$("#notificacion #notificacion-Label").html("Generacion de Vista Previa");
						$("#notificacion #notificacion-body").html("<h4>Se generar&aacute; una vista previa del trabajo realizado. ¿Desea continuar?</h4>");
					    
					    $('#notificacion-footer').html('<div class="col-xs-6">\
				        	<a class="col-xs-12 btn btn-danger btn-flat cancel-modal" data-dismiss="modal">Cancelar</a>\
				        </div>\
				        <div class="col-xs-6">\
				        	<a class="col-xs-12 btn btn-primary btn-flat accept-modal preview-ok">Aceptar</a>\
				        </div>');

					    $('#notificacion').modal({
					        keyboard: false,
					        backdrop: 'static'
					    });

					    $(document).on('click', '.preview-ok', function(){
					    	autosave();
					    	var json = JSON.parse(localStorage.getItem("main-config-cookie"));
					    	if( json.length )
					    	{
					    		var data ={
					    			'main-config-cookie': localStorage.getItem('main-config-cookie'),
					    			'documental-req-cookie': localStorage.getItem('documental-req-cookie'),
					    			'specific-values-cookie': localStorage.getItem('specific-values-cookie'),
					    			'basic-req': localStorage.getItem('basic-req'),
					    			'specific-req': localStorage.getItem('specific-req'),
					    			'cookies-ids': localStorage.getItem('cookies-ids')
					    		}

					    		$http.defaults.headers.post['X-CSRFToken'] = token;
					    		$http.post(
					    			"/categorizacion/administrador/tabulador/vista/"+json[0].id+"/",
					    			data
					    		).success(
					    			function(data, status, headers, config) {
					    				// Colocamos el id del tabulador para permitir la vista previa del mismo 
					    				location.href = "/categorizacion/administrador/tabulador/vista/"+json[0].id+"/*";
					    			}
					    		);
					    		
					    	}else{
					    		$("#notificacion #notificacion-Label").html("Vista previa no disponible");
					    		$("#notificacion #notificacion-body").html("<h4>A&uacute;n no existen elementos disponibles para su visualizaci&oacute;n.</h4>");
					    	    $('#notificacion-footer').html('\
					    	    	<div class="col-xs-12" data-dismiss="modal">\
					    	        <button class="btn btn-flat btn-primary col-xs-12">Aceptar</button>\
					    	    </div>')
					    	    $('#notificacion').modal({
					    	        keyboard: false,
					    	        backdrop: 'static'
					    	    });							
					    	}
					    });
					}				
				}
			]
		);

		// Common functions

		getRelevanceByCategory = function(){
			var a = [];
			$('input[type=checkbox][name*="star"]').each(function(){
			   a.push( $(this).parent().hasClass('checked') );
			});
			return a;
		}

		getRelevanceByCategoryLimited = function(){
			var a = [];
			var main_object = {'limit' : 0,'apply' : false};
			var closest = undefined;
			var c1, c2, o;
			for( var i =0; i < $(".stars_table").find("tr").length - 1; ++i )
			{	
				o = {'inf_aplica': false, 'inf_star': -1, 'sup_aplica': false, 'sup_star': -1};
				c1 = $('input[type=checkbox][name=inf_aplica_'+i+']');
				c2 = $('input[type=checkbox][name=sup_aplica_'+i+']');

				if( $(c1).parent().hasClass('checked') ){
					o.inf_aplica = true;
					o.inf_star = $('input[type=number][name=inf_star_'+i+']').val();
				}			

				if( $(c2).parent().hasClass('checked') ){
					o.sup_aplica = true;
					o.sup_star = $('input[type=number][name=sup_star_'+i+']').val();
				}

				if(o.inf_aplica && o.sup_aplica && (parseFloat(o.inf_star) > parseFloat(o.sup_star)))
				{
					a = false;
					break;
				}

				a.push(o);
			}
			return a;
		}

		getRepetitionByCategory = function(){
			var a = [];
			var val = undefined;
			$('input[type=number][name*="star"]').each(function(){
				val = $(this).val();
				if(val !== undefined && val!=='' && val >= 0){
					a.push(val);					
				}else{
					a = false;
					return a;
				}
			});
			return a;
		}

		addElement = function( cname, pid, ptype, obj ){			
			var tree = new Tree();		
			tree.load( JSON.parse(localStorage.getItem(cname)) );
			tree.addChildByIndex( pid, ptype, obj );
			localStorage.setItem(cname, JSON.stringify([tree.render(false)]));
		}

		getValue = function( cname ){		
			return   JSON.parse(localStorage.getItem(cname));
		}

		appendValue = function( cname, value, type ){
			
			//	Busca y actualiza en el nivel superior unicamente
			var a =  JSON.parse(localStorage.getItem(cname));
			var booleano = true;
			var m = $.map(a, function(e){
				if(e.id == value.id){
					if( type != undefined )
					{
						if( e.type == type ){
							e = value;
							booleano = false;
						}
					}else{
						e = value;
						booleano = false;
					}
				}
				return e
			});
			if(booleano==true){				
				m.push(value);
			}
			localStorage.setItem(cname ,JSON.stringify( m ));
		}

		hasValue = function( obj, key, value ) {
		    return obj.hasOwnProperty(key) && obj[key] === value;
		}

		positional = function( a, o ){
		  	var m = $.map(a,
				function(e, i){
					if ( _.isEqual(e, o) )
						return i; 
					else return;
				}
			);
		  return m.length ? m[0]: -1;
		}

		deleteElement = function( cname, id ){
			localStorage.setItem( cname, JSON.stringify( 
					$.map(
						JSON.parse(localStorage.getItem( cname )), 
						function( e ) {
							if (e.id == id){
								e.state = "deleted";
							}
							return e;
						}
					)
				)
			);
		}

		editElement = function( cname, id, obj, nstate){		
			localStorage.setItem( 
				cname, 
				JSON.stringify(
					$.map( 
						 JSON.parse(localStorage.getItem( cname )),
						function( e ) {						
							if (e.id == id || id == "*"){
								$.each(obj, function(k,v){
									console.log(k+ " " +v);
									e[k] = v;
								});
								e.state = nstate;
							}						
							return e;
						}
					)
				)
			);
		}

		isDataLoaded = function(){			
			return  JSON.parse(localStorage.getItem('basic-req')).length ||  JSON.parse(localStorage.getItem('specific-req')).length ||  JSON.parse(localStorage.getItem('main-config-cookie')).length ||  JSON.parse(localStorage.getItem('documental-req-cookie')).length ||  JSON.parse(localStorage.getItem('specific-values-cookie')).length
		}

		isDataEdited = function( cname ){
			var m = false;		
			$.each( JSON.parse(localStorage.getItem( cname )), function(){
				if ( this.state != 'done' ){
					m = true;
					return false;
				}
			});
			return m;
		}

		autosave = function(){	
			if( isDataLoaded() )
			{
				var mcc = getValue('main-config-cookie').length > 0 && isDataEdited('main-config-cookie');
				var dqc = getValue('documental-req-cookie').length > 0 && isDataEdited( 'documental-req-cookie' );
				var svc = getValue('specific-values-cookie').length > 0 && isDataEdited('specific-values-cookie');
				var data_temp = {
						'tabulador': !$("#constructor_core").length?$('#basic-config').attr('added-elements'): JSON.parse(localStorage.getItem("main-config-cookie"))[0].id,
						'main_cookie': localStorage.getItem('main-config-cookie'),
						'documental_cookie': dqc ? localStorage.getItem('documental-req-cookie') : "{}",
						'specific_values_cookie': svc ? localStorage.getItem('specific-values-cookie'): "{}",
						'basic_req': localStorage.getItem('basic-req'),
						'specific_req': localStorage.getItem('specific-req'),
						csrfmiddlewaretoken: token
					}
				
				if($(".tabulador_sustituto").length){
					data_temp['tabulador_sustituto'] = parseInt($(".tabulador_sustituto").val());
				}

				// console.log("IS SO FUNK")
				// console.log( getValue('specific-values-cookie').length);
				// console.log( isDataEdited('specific-values-cookie') );
				// console.log(localStorage.getItem('specific-values-cookie'));

				$(".fixed-spinner").fadeIn('slow');
				$.ajax({
					type: "POST",
					url: "/categorizacion/administrador/tabulador/agregar/",
					async:false,
					data:data_temp,
					success: function(server_data){
						
						console.log(server_data.data);

						/*
						*
						* Actualizar ids locales de elementos y estados	
						*
						*/

						// Actualizar main-config-cookie
						editElement(
							'main-config-cookie',
							 JSON.parse(localStorage.getItem('main-config-cookie'))[0].id,
							{'id': server_data.data.tabulador},
							'done'
						);

						if(server_data.data.version===0 && $("#id_version_actual").length===0){
							$('#tipo-prestador').parent("div").after($("#checkbox_version").html());
							$("input[type=checkbox]").iCheck({
								checkboxClass: 'icheckbox_minimal',	
								radioClass: 'iradio_minimal',
								increaseArea: '20%'
							});
						}
						
						if(server_data.data.hasOwnProperty('elementos_dr')){
							if (server_data.data.elementos_dr.length>0){
								$.each(server_data.data.elementos_dr, function(){							
									editElement(
										'documental-req-cookie',
										this.pid,
										{'id': this.nid},
										'done'
									);
									try {			
										temp = this.nid;
										$(".table-documental-req").children("tbody").children("tr").children("td#opts").find("a#"+this.pid).each(
											function(){
												$(this).attr('id', temp);
											}
										);							
									}
									catch(err) {}
								});
							}
						}
						if(server_data.data.hasOwnProperty('elementos_ve')){
							if(server_data.data.elementos_ve.length>0)
								$.each(server_data.data.elementos_ve, function(){					
									editElement(
										'specific-values-cookie',
										this.pid,
										{'id': this.nid},
										'done'
									);
									try {			
										temp = this.nid;
										$(".table-basic-data").children("tbody").children("tr").children("td#opts").find("a#"+this.pid).each(
											function(){
												$(this).attr('id', temp);
											}
										);							
									}
									catch(err) {}
								});
						}

						if(server_data.data.hasOwnProperty('elementos_req_specific')){
							var treeaux = new Tree();
							treeaux.load(JSON.parse(localStorage.getItem('specific-req')), undefined, undefined, undefined, server_data.data.elementos_req_specific);
							localStorage.setItem('specific-req', JSON.stringify( [treeaux.render(false)] ) );
						}


						if(server_data.data.hasOwnProperty('elementos_req_basic')){
							var treeaux = new Tree();
							treeaux.load(JSON.parse(localStorage.getItem('basic-req')), undefined, undefined, undefined, server_data.data.elementos_req_basic);
							localStorage.setItem('basic-req', JSON.stringify([treeaux.render(false)]));
						}

						//Actualizar basiq-req
						editElement(
							'basic-req',
							 JSON.parse(localStorage.getItem('basic-req'))[0].id,
							{'id': server_data.data.tabulador},
							'done'
						);

						//Actualizar specific-req
						editElement(
							'specific-req',
							 JSON.parse(localStorage.getItem('specific-req'))[0].id,
							{'id': server_data.data.tabulador},
							'done'
						);
						
						$('#basic-config').attr('added-elements', server_data.data.tabulador - 1 );						
					},
					complete: function (server_data) {
						configSaved = true;
					},
					error: function(e){
						console.log(e);
					}
				});
				$(".fixed-spinner").fadeOut('slow');				
			}
		}

		// Jquery Section	

		f1 = function(){
			/*
			*
			* Add specific-values
			*
			*/
			var data =  JSON.parse(localStorage.getItem('cookies-ids'));
			// console.log("FUNK ");
			// console.log(data);
			// console.log(typeof(data.i));
			data.i += 1;
			var id = data.i;
			localStorage.setItem('cookies-ids', JSON.stringify(data));

			var val = $("#nombre-dbasic").val();
			var suministrado = $("#suministrado-dbasic").parent().hasClass('checked');
			var valor = [];

			if(!suministrado){
				$(".valor-categoria").each(function(){
					valor.push(
				   		$(this).val() != '' && $(this).val() != '-' ? parseFloat($(this).val()) : 'N/A'
					);
				});
			}

			$('.basic-data-body').append(
				_.template($("#valores-especificos-categoria").html() )({
					"name": val,
					"id": data.i,
					"suministrado": suministrado ? "Si" : "No",
					"suministrado_bool": suministrado,
					"valor": valor.length ? valor : 'N/A',
					"extra_class":''
				})
			);

			$('.table-basic-data').siblings().hide();
			$('.table-basic-data').attr('added-elements', data.i);
			$('.table-basic-data').show();

			// Add new data to cookie body 
			appendValue('specific-values-cookie', {
				'id': data.i, 
				'name': val,
				'state': 'added',
				'suministrado': suministrado ? "Si" : "No",
				'valor': valor.length ? valor : 'N/A'
			}, undefined );

			$("#modal-agregar-elemento").modal('hide');
			return true;
		}

		f2 = function(){
			/*
			*
			* Add documental-req
			*
			*/
			$('#form_id').validate();
			if($('#form_id').valid()){
				$("#modal-agregar-elemento").modal('hide');		
			
				var id  = currentCounter;
				var val = $("#nombre-documental-req").val();
				var typedoc = $("#form_id #id_tipo_documento").val();
				var typedoctext = $("#form_id #id_tipo_documento option:selected").text().trim();
				$("#form_id #id_tipo_documento").css("display","none");
				var clone_select_docstypes = $("#form_id #id_tipo_documento")[0].outerHTML;

				$('.documental-req-body').append(
					_.template('<tr class="req-documental-row">\
						<td id="name" >\
							<%= name %>\
						</td>\
						<td id="type" iddoc="<%=typedoc%>" >\
							<div id="typedoctext"><%= typedoctext %></div>\
							<%= select_types_hiden %>\
						</td>\
						<td id="opts" >\
							<a \
								id = "<%= id %>" \
								data-toggle="tooltip" \
								title = "Editar"\
								state = "normal" \
								sufix = "req-documental" \
								class="btn btn-info btn-flat editar-button" \
								data-original-title="Editar">\
								<i class="fa fa-pencil-square-o icon-white"></i>\
							</a>\
							<a \
								id = "<%= id %>" \
								data-toggle="tooltip"\
								title="Eliminar" \
								state = "normal" \
								sufix = "req-documental" \
								class="btn btn-info btn-flat delete-button" \
								data-original-title="Eliminar">\
								<i class="fa fa-trash-o icon-white"></i> \
							</a>\
						</td>\
						</tr>')({
						"name": val,
						"id": id,
						"typedoctext":typedoctext,
						"select_types_hiden": clone_select_docstypes,
						"typedoc": typedoc
					})
				);
				$('.table-documental-req').siblings().hide();
				$('.table-documental-req').attr( 'added-elements', id );
				$('.table-documental-req').show();

				// Add new data to cookie body
				appendValue('documental-req-cookie', {
				 'id': id,
				 'name': val,
				 'type': typedoc,
				 'state': 'added'
				}, undefined);
			}
			return true;
		}

		f3 = function(){
			/*
			*
			* Add fundamental-aspect
			*
			*/
            
            $("#form_id").validate();

            if($("#form_id").valid()){

            	disableAddButton(".accept-modal");
				var data =  JSON.parse(localStorage.getItem('cookies-ids'));
				var state = $("#mutable-form-container").attr("state"); 
				var name = $("#mutable-form-container").find("#id_nombre").val();
				var percent = $("#percent-number").length? $("#percent-number").val(): undefined;
				var tipo_aspecto = $("#mutable-form-container").find("#id_tipo_aspecto").val();
				var tipo_aspecto_text = $("#mutable-form-container").find("#id_tipo_aspecto option:selected").text();
				var percent_counter = parseFloat(percent) + percentAdded(state != "editing"?undefined: $("#mutable-form-container").attr("id_editing"));
				
				var af_counter = $("."+currentTab+"-body .panel[type=AF]").length+1;				

				if( (100.0 - percent_counter) < 0 )
				{
					/*
						Se realiza la validación para los casos donde una asignación
						de porcentaje sea realizada erroneamente
					*/
					$("#percent-number").parent("div").append(
						_.template($("#notification-zone").html())({
							'msg': "El porcentaje asignado no es v&aacute;lido",
							'close': true
						})
					)
				}else{

					$("#modal-agregar-elemento").modal('hide');
					$("."+currentTab+"-alert").hide();
					
					if(state != "editing"){
						data.a += 1;
						localStorage.setItem('cookies-ids', JSON.stringify(data));
						$("."+currentTab+"-body").append(
							_.template(
								$("#fundamental-aspect-template").html()
							)({
								"id": data.a,
								"name": name,
								"percent": percent !== undefined ? parseFloat(percent): undefined,
								"tipo_aspecto": tipo_aspecto,
								"color": tipo_aspecto_text.toLowerCase() == 'mantenimiento'?"#E6EFF8":"#e2e2e2", 
								"counter": af_counter
							})
						);					
						addElement(
							currentTab, 
							 JSON.parse(localStorage.getItem('main-config-cookie'))[0].id, 
							'T',
							new Tree(data.a, name, [], 'added', 'AF', {'percent': percent, 'tipo_aspecto': tipo_aspecto})				
						);			
					}else{
						// Se actualiza dentro del elemento de aspecto fundamental
						var tree = new Tree();
						tree.load(JSON.parse(localStorage.getItem(currentTab)));
						tree.editNode(
							parseInt($("#mutable-form-container").attr("id_editing")),
							"AF",
							{
								"name": name,
								"extra": {'percent': percent, 'tipo_aspecto': tipo_aspecto}
							}
						);
						localStorage.setItem(currentTab, JSON.stringify([tree.render(false)]));
					
						// Actualizar elementos de interfaz
						$("span[id="+$("#mutable-form-container").attr("id_editing")+"][type=AF].element_name").html(name);
						$("span[id="+$("#mutable-form-container").attr("id_editing")+"][type=AF].percent").html(percent);
						$(".panel[id="+$("#mutable-form-container").attr("id_editing")+"][type=AF]").children(".panel-heading").css("background-color",tipo_aspecto_text.toLowerCase() == 'mantenimiento'?"#E6EFF8":"#e2e2e2");
					}

					$('input').iCheck({
					    checkboxClass: 'icheckbox_minimal',
					    radioClass: 'iradio_minimal',
					    increaseArea: '20%'
					});
				}
			}

			return true;
		}

		f4 = function(){
			/*
			*
			* Add section-element
			*
			*/
			$("#form_id").validate();

            if($("#form_id").valid()){
            	
            	disableAddButton(".accept-modal");
				var val = $("#mutable-form-container").find("#id_nombre").val();
				var data =  JSON.parse(localStorage.getItem('cookies-ids'));
				var state = $("#mutable-form-container").attr("state");
				var s_counter = undefined;
				var parent_counter = "";

            	$("#modal-agregar-elemento").modal('hide');	

            	if(state != "editing"){
					$('.zone-selector').each(function(){
						if($(this).parent().hasClass('checked')){					
							data.s+=1;
							localStorage.setItem('cookies-ids', JSON.stringify(data));					
							var id = $(this).parents("div[type]").attr('id');
							var type = $(this).parents("div[type]").attr('type');

							s_counter = $("."+currentTab+"-body .panel[id="+id+"][type="+type+"]").find(".panel-body").eq(0).children(".panel[type=SS],.panel[type=S]").length+1;
							// s_counter = $("."+currentTab+"-body .panel[id="+id+"][type="+type+"] .panel[type=SS]").length + $("."+currentTab+"-body .panel[id="+id+"][type="+type+"] .panel[type=S]").length+1;
							// s_counter = $("."+currentTab+"-body .panel[id="+id+"][type="+type+"] .panel[type=S]").length+1;
							parent_counter = $("[id="+id+"][type="+type+"]").attr("element_fisical_idenfitier");

							$("[id="+id+"][type="+type+"] .panel-body").eq(0).append(
								_.template( $("#section-template").html() )({
									"name": val,
									"id": data.s,
									"parent_counter": parent_counter,
									"counter": s_counter
								})
							);

							addElement(
								currentTab,
								id,
								type,
								new Tree( data.s, val, [], 'added', 'S', {} )
							);					
						}
					});
            	}else{
            		// Se actualiza dentro del elemento seccion
            		var tree = new Tree();
            		tree.load(JSON.parse(localStorage.getItem(currentTab)));
            		tree.editNode(
            			parseInt($("#mutable-form-container").attr("id_editing")), 
            			"S",
            			{
            				"name": val
            			}
            		);
            		localStorage.setItem(currentTab, JSON.stringify([tree.render(false)]));

            		// Actualizar elementos de interfaz
            		$("span[id="+$("#mutable-form-container").attr("id_editing")+"][type=S]").html(val);
            	}

				$('input').iCheck({
				    checkboxClass: 'icheckbox_minimal',
				    radioClass: 'iradio_minimal',
				    increaseArea: '20%'
				});
			}

			return true;	
		}

		f5 = function(){
			/*
			*
			* Add subsection element using dual
			*
			*/
			var numero =0;
			var cond = true;
        	$.each($('.select_form'),function(){
        		if($(this).val() != "" && $(this).val() != undefined){
        			numero+=1;
        		}
        	});

        	if(numero!=2){
        		cond = false
        	}
			$("#form_id").validate({
				invalidHandler: function(event, validator){
		        	if(numero!=2){
		        	}
		        }
			});
            if($("#form_id").valid() && cond == true){

            	disableAddButton(".accept-modal");

            	if($("#mutable-form-container").attr('flag')!='true'){
            		$("#modal-agregar-elemento").modal('hide');
            	}

				var array = [];
				var relevance = getRelevanceByCategory();
				var data =  JSON.parse(localStorage.getItem('cookies-ids'));
				var val = $("#mutable-form-container").find("#id_enunciado").val();
				var state = $("#mutable-form-container").attr("state");
				var ss_counter = undefined;
				var parent_counter = "";
				
				var i = 0;
				$.each($('.select_form'),function(){
					if(i == 0){			
						array.push($('#id_valor_respuesta').val());
						array.push($('#id_valor_respuesta option:selected').text());
					}else{
						array.push($('#id_valor_respuesta'+i).val());
						array.push($('#id_valor_respuesta'+i+' option:selected').text());						
					}
					i+=1;
				});
				var booleano = false;

				if(state != "editing"){

					$('.zone-selector').each(function(){
						if($(this).parent().hasClass('checked')){
							data.ss+=1;
							localStorage.setItem('cookies-ids', JSON.stringify(data));					
							var id = $(this).parents("div[type]").attr('id');
							var type = $(this).parents("div[type]").attr('type');

							if ($('#mutable-form-container').attr('flag') != 'true'){

								// ss_counter = $("."+currentTab+"-body .panel[id="+id+"][type="+type+"] .panel[type=SS]").length + $("."+currentTab+"-body .panel[id="+id+"][type="+type+"] .panel[type=S]").length+1;
								ss_counter = $("."+currentTab+"-body .panel[id="+id+"][type="+type+"]").find(".panel-body").eq(0).children(".panel[type=SS],.panel[type=S]").length+1;
								parent_counter = $("[id="+id+"][type="+type+"]").attr("element_fisical_idenfitier");

								$("[id="+id+"][type="+type+"] .panel-body").eq(0).append(
									_.template( $("#subseccion-template").html() )({
										"condicion":"",
										"name": val,
										"id": data.ss,
										"body": array,
										"tipo": 'D',
										"parent_counter": parent_counter,
										"counter": ss_counter,
										"identifier": _.uniqueId('radio')
									})
								);
								addElement(
									currentTab,
									id,
									type,
									new Tree( data.ss, val, {'options':[ array[0], array[2] ],'options_val':[array[1], array[3]], 'relevance': relevance}, 'added', 'SS', {'subtype': 'D'} )
								);
								$(".panel_subsec[id="+data.ss+"][type='SS'] .panel_body_subsec input").iCheck({
								    radioClass: 'iradio_minimal',
								    increaseArea: '20%'
								})
							}else{
								if(booleano != true){
									$('#mutable-form-container').html(globaldef.pop());

									if(!globaldef.length){
										$('#mutable-form-container').attr('flag', 'false');
									}

									var aux = selectid.pop().replace('_-','');
								}
								
								enableAddButton(".accept-modal");
								booleano = true;
								var tree = new Tree(data.ss, val, {'options':[ array[0], array[2] ],'options_val':[ array[1], array[3]], 'relevance': relevance}, 'added', 'SS', {'subtype': 'D'})
								assignConditional(tree,val,'add-dual',array,aux);							
							}

						}
					});
				}else{
					// Se actualiza dentro del arbol la subseccion dual
					var tree = new Tree();
					tree.load(JSON.parse(localStorage.getItem(currentTab)));
					tree.editNode(
						parseInt($("#mutable-form-container").attr("id_editing")),
						"SS",
						{
							"name": val,
							"content": {
								'options':[ array[0], array[2] ],
								'options_val':[array[1], array[3]], 
								'relevance': relevance
							},
							"extra": {
                        		"subtype": "D"
                        	}
						}
					);
					localStorage.setItem(currentTab, JSON.stringify([tree.render(false)]));

					$("[id="+$("#mutable-form-container").attr("id_editing")+"][type=SS]").find(".dual-name").html(val);
					$("[id="+$("#mutable-form-container").attr("id_editing")+"][type=SS]").find(".dual-radio-text").eq(0).html(array[1]);
					$("[id="+$("#mutable-form-container").attr("id_editing")+"][type=SS]").find(".dual-radio-text").eq(1).html(array[3]);
				}

				$('#mutable-form-container input').iCheck({
				    checkboxClass: 'icheckbox_minimal',
				    radioClass: 'iradio_minimal',
				    increaseArea: '20%'
				});

			}else{
				if(numero!=2){
					$('#id_valor_respuesta').before('<div role="alert" class="alert alert-ajustado alert-warning alert-dismissible error" id="id_valor_respuesta-error"><button data-dismiss="alert" class="close" type="button"><span aria-hidden="true">×</span><span class="sr-only">Close</span></button><li>Deben haber 2 valores de respuestas en este elemento</li></div>')
	        	}	
			}
			

			return true;
		}

		f6 = function(){
			/*
			*
			* Add subsection element using scale
			*
			*/

			var numero =0;
			var cond = true;
        	
        	$.each($('.select_form'),function(){
        		if($(this).val() != "" && $(this).val() != undefined){
        			numero+=1;
        		}
        	});
        	
     		cond = numero == 3;

			$("#form_id").validate({
				invalidHandler: function(event, validator){
		        	if(numero!=3){
		        	}
		        }
			});
            if($("#form_id").valid() && cond == true){

            	disableAddButton(".accept-modal");

            	if($("#mutable-form-container").attr('flag')!='true'){
            		$("#modal-agregar-elemento").modal('hide');
            	}

				var array = [];
				var val = $("#mutable-form-container").find("#id_enunciado").val();
				var i = 0;
				var relevance = getRelevanceByCategory();

				$.each($('.select_form'),function(){
					if(i == 0){
						array.push($('#id_valor_respuesta').val());
						array.push($('#id_valor_respuesta option:selected').text());
					}else{
						array.push($('#id_valor_respuesta'+i).val())
						array.push($('#id_valor_respuesta'+i+' option:selected').text())						
					}
					i+=1;
				});
				var data =  JSON.parse(localStorage.getItem('cookies-ids'));
				var state = $("#mutable-form-container").attr("state");
				var booleano = false;
				var ss_counter = undefined;
				var parent_counter = "";

				if(state!="editing")
				{
					$('.zone-selector').each(function(){		
						if($(this).parent().hasClass('checked')){										
							data.ss+=1;
							localStorage.setItem('cookies-ids', JSON.stringify(data));					
							var id = $(this).parents("div[type]").attr('id');
							var type = $(this).parents("div[type]").attr('type');

							ss_counter = $("."+currentTab+"-body .panel[id="+id+"][type="+type+"]").find(".panel-body").eq(0).children(".panel[type=SS],.panel[type=S]").length+1;
							// ss_counter = $("."+currentTab+"-body .panel[id="+id+"][type="+type+"] .panel[type=SS]").length + $("."+currentTab+"-body .panel[id="+id+"][type="+type+"] .panel[type=S]").length+1;
							// ss_counter = $("."+currentTab+"-body .panel[id="+id+"][type="+type+"] .panel[type=SS]").length+1;
							parent_counter = $("[id="+id+"][type="+type+"]").attr("element_fisical_idenfitier");
							
							if ($('#mutable-form-container').attr('flag') != 'true'){				
								$("[id="+id+"][type="+type+"] .panel-body").eq(0).append(
									_.template( $("#subseccion-template").html() )({
										"condicion":"",
										"name": val,
										"id": data.ss,
										"body": array,
										"tipo": 'E',
										"parent_counter": parent_counter,
										"counter": ss_counter,
										"identifier": _.uniqueId('radio')
									})
								);
								addElement(
									currentTab,
									id,
									type,
									new Tree( 
										data.ss, 
										val, 
										{
											'options':[ array[0], array[2], array[4] ],
											'options_val':[array[1], array[3], array[5]],
											'relevance': relevance
										}, 'added', 'SS', {'subtype': 'E'}
									)
								);
								$(".panel_subsec[id="+data.ss+"][type='SS'] .panel_body_subsec input").iCheck({
									checkboxClass: 'icheckbox_minimal',
								    radioClass: 'iradio_minimal',
								    increaseArea: '20%'
								})
							}else{
								if(!booleano){
									$('#mutable-form-container').html(globaldef.pop());
									
									if(!globaldef.length){
										$('#mutable-form-container').attr('flag', 'false');
									}

									var aux = selectid.pop().replace('_-','');
								}

								enableAddButton(".accept-modal");
								booleano = true;
								var tree = new Tree(data.ss, val, {'options':[ array[0], array[2], array[4] ], 'options_val':[array[1], array[3], array[5]], 'relevance': relevance}, 'added', 'SS', {'subtype': 'E'})
								assignConditional(tree,val,'add-escala',array,aux);
							}
						}
					});
				}else{
					// Se actualiza dentro del arbol la subseccion dual
					var tree = new Tree();
					tree.load(JSON.parse(localStorage.getItem(currentTab)));
					tree.editNode(
						parseInt($("#mutable-form-container").attr("id_editing")),
						"SS",
						{
							"name": val,
							"content": {'options':[ array[0], array[2], array[4] ],'options_val':[array[1], array[3], array[5]], 'relevance': relevance},
							"extra": {
	                    		"subtype": "E"
	                    	}
						}
					);
					localStorage.setItem(currentTab, JSON.stringify([tree.render(false)]));

					$("[id="+$("#mutable-form-container").attr("id_editing")+"][type=SS]").find(".dual-name").html(val);
					$("[id="+$("#mutable-form-container").attr("id_editing")+"][type=SS]").find(".dual-radio-text").eq(0).html(array[1]);
					$("[id="+$("#mutable-form-container").attr("id_editing")+"][type=SS]").find(".dual-radio-text").eq(1).html(array[3]);
					$("[id="+$("#mutable-form-container").attr("id_editing")+"][type=SS]").find(".dual-radio-text").eq(2).html(array[5]);
				}			

				$('#mutable-form-container input').iCheck({
				    checkboxClass: 'icheckbox_minimal',
				    radioClass: 'iradio_minimal',
				    increaseArea: '20%'
				});
			}else{
				if(numero!=3){	
					$('#id_valor_respuesta').before('<div role="alert" class="alert alert-ajustado alert-warning alert-dismissible error" id="id_valor_respuesta-error"><button data-dismiss="alert" class="close" type="button"><span aria-hidden="true">×</span><span class="sr-only">Close</span></button><li>Deben haber 3 valores de respuestas en este elemento</li></div>')
        		}
			}
			return true;
		}

		f7 = function(){
			/*
			*
			* Add subsection element using range-value measure
			*
			*/
			var cond = true;
			var relevance = getRelevanceByCategoryLimited();

			if($('.select_unidad').val() == "" || $('.select_unidad').val() == undefined){
				cond = false
			}
			$("#form_id").validate({
				invalidHandler: function(event, validator){
					if($('.select_unidad').val() == "" || $('.select_unidad').val() == undefined){
					}
				}
			});

            if($("#form_id").valid() && cond == true && relevance !== false){

            	disableAddButton(".accept-modal");
            	
            	if($("#mutable-form-container").attr('flag')!='true'){
            		$("#modal-agregar-elemento").modal('hide');
            	}

				var data =  JSON.parse(localStorage.getItem('cookies-ids'));
				var val = $("#mutable-form-container").find("#id_enunciado").val();
				var placeholder = $('#id_unidad_o_medida option:selected');
				var state = $("#mutable-form-container").attr("state");
				var booleano = false;
				var ss_counter = undefined;
				var parent_counter = "";

				if(state != "editing")
				{
					$('.zone-selector').each(function(){
						if($(this).parent().hasClass('checked')){
							console.log("selectid = "+selectid.length)
							data.ss+=1;
							localStorage.setItem('cookies-ids', JSON.stringify(data));
							var id = $(this).parents("div[type]").attr('id');
							var type = $(this).parents("div[type]").attr('type');

							ss_counter = $("."+currentTab+"-body .panel[id="+id+"][type="+type+"]").find(".panel-body").eq(0).children(".panel[type=SS],.panel[type=S]").length+1;
							parent_counter = $("[id="+id+"][type="+type+"]").attr("element_fisical_idenfitier");

							if ($('#mutable-form-container').attr('flag') != 'true'){
								$("[id="+id+"][type="+type+"] .panel-body").eq(0).append(
									_.template( $("#subseccion-rango-template").html() )({
										"condicion":"",
										"name": val,
										"id": data.ss,
										"placeholder": $(placeholder).text(),
										"tipo": 'R',
										"parent_counter": parent_counter,
										"counter": ss_counter
									})
								);
								addElement(
									currentTab,
									id,
									type,
									new Tree( 
										data.ss, 
										val, 
										{
											'unit': $(placeholder).val(),							
											'relevance_value': relevance
										}
										, 'added', 'SS', {'subtype': 'R'}
									)
								);
							}else{
								if(booleano != true){
									$('#mutable-form-container').html(globaldef.pop());

									if(!globaldef.length){
										$('#mutable-form-container').attr('flag', 'false');
									}

									var aux = selectid.pop().replace('_-','');
								}
								
								enableAddButton(".accept-modal");
								booleano = true;
								var tree = new Tree(data.ss, val, {'unit': $(placeholder).val(), 'unit_val': $(placeholder).text(), 'relevance_value': relevance}, 'added', 'SS', {'subtype': 'R'})
								assignConditional(tree,val,'add-rango',[$(placeholder).text()],aux);
							}
						}
					});
				}else{
					// Se actualiza dentro del arbol la subseccion dual
					var tree = new Tree();
					tree.load(JSON.parse(localStorage.getItem(currentTab)));

					// id, name, content, state, type, extra
					tree.editNode(
						parseInt($("#mutable-form-container").attr("id_editing")),
						"SS",
						{
							"name": val,
							"content": {'unit': $(placeholder).text(), 'relevance_value': relevance},
							"extra": {
	                    		"subtype": "R"
	                    	}
						}
					);
					localStorage.setItem(currentTab, JSON.stringify([tree.render(false)]));
					$("[id="+$("#mutable-form-container").attr("id_editing")+"][type=SS]").find(".scale-name").html(val);
					$("[id="+$("#mutable-form-container").attr("id_editing")+"][type=SS]").find(".scale-input").eq(0).attr("placeholder", $(placeholder).val());
				}

				$('#mutable-form-container input').iCheck({
				    checkboxClass: 'icheckbox_minimal',
				    radioClass: 'iradio_minimal',
				    increaseArea: '20%'
				});
			}else{
				if(cond==false){
					$('#id_unidad_o_medida').after('<div role="alert" class="alert alert-ajustado alert-warning alert-dismissible error" id="id_valor_respuesta-error"><button data-dismiss="alert" class="close" type="button"><span aria-hidden="true">×</span><span class="sr-only">Close</span></button><ul><li>Este campo es obligatorio</li></ul></div>');
				}

				if(relevance==false){
					$(".stars_table").before('<div role="alert" class="alert alert-ajustado alert-warning alert-dismissible error" id="id_valor_respuesta-error"><button data-dismiss="alert" class="close" type="button"><span aria-hidden="true">×</span><span class="sr-only">Close</span></button><ul><li>Existen errores referentes a los valores colocados como l&iacute;mites</li></ul></div>');
				}
			}
			return true;
		}

		f8 = function(){
			/*
			*
			* Add subsection element using repetitive answer type
			*
			*/
			var repetition = getRepetitionByCategory();
			
			$("#form_id").validate();
            if($("#form_id").valid() && repetition){
            	disableAddButton(".accept-modal");

            	if($("#mutable-form-container").attr('flag')!='true'){
            		$("#modal-agregar-elemento").modal('hide');
            	}
				var val = $("#mutable-form-container").find("#id_enunciado").val();
				var data =  JSON.parse(localStorage.getItem('cookies-ids'));
				var id;
				var type;
				var star;
				var aux ="";
				var state = $("#mutable-form-container").attr("state");
				var booleano = false;
				var ss_counter = undefined;
				var parent_counter = "";

				if(state != "editing")
				{
					$('.zone-selector').each(function(){
						if($(this).parent().hasClass('checked')){					
							data.ss+=1;
							localStorage.setItem('cookies-ids', JSON.stringify(data));					
							id = $(this).parents("div[type]").attr('id');
							type = $(this).parents("div[type]").attr('type');
							
							ss_counter = $("."+currentTab+"-body .panel[id="+id+"][type="+type+"]").find(".panel-body").eq(0).children(".panel[type=SS],.panel[type=S]").length+1;
							parent_counter = $("[id="+id+"][type="+type+"]").attr("element_fisical_idenfitier");

							star=[];
							$.each($('.star'), function(){
								aux ="";
								$.each($(this).children('label'), function(){
									var aux5 = $(this).html();
									aux5 = aux5.replace(/"/g,"\'");
									aux+= aux5;
								});
								star.push(aux);
								star.push($(this).siblings('td').find('input').val());
							});

							if ($('#mutable-form-container').attr('flag') != 'true'){
								$("[id="+id+"][type="+type+"] .panel-body").eq(0).append(
									_.template( $("#subseccion-repetitive-template").html() )({
										"condicion":"",
										"name": val,
										"id": data.ss,
										"ul_body": _.template($("#repetitive-relevance-ul").html())({
											"categorias":star											
										}),
										"parent_counter": parent_counter,
										"counter": ss_counter
									})
								);
								addElement(
									currentTab,
									id,
									type,
									new Tree( 
										data.ss, 
										val, 
										{'repetition': repetition}
										, 'added', 'SS', {'subtype': 'REP'}
									)
								);
							}else{
								for(var e in star){
									if(e%2 == 0){
										star[e] = star[e].toString().replace(/"/g,"&th");
									}
								}
								if(booleano != true){
									$('#mutable-form-container').html(globaldef.pop());

									if(!globaldef.length){
										$('#mutable-form-container').attr('flag', 'false');
									}

									var aux = selectid.pop().replace('_-','');
								}
								
								enableAddButton(".accept-modal");
								booleano = true;
								var tree = new Tree(data.ss, val, {'repetition': repetition, 'repetition_star': star}, 'added', 'SS', {'subtype': 'REP'})
								assignConditional(tree,val,'add-repetitive',star,aux);
							}
							$("[id="+data.ss+"][type=SS] input").iCheck({
							    checkboxClass: 'icheckbox_minimal',			   
							    increaseArea: '20%'
							});
						}
					});
				}else{
					// Se actualiza dentro del arbol la subseccion repetitiva
					var tree = new Tree();
					var aux = aux5 = "";
					tree.load(JSON.parse(localStorage.getItem(currentTab)));
					// id, name, content, state, type, extra
					tree.editNode(
						parseInt($("#mutable-form-container").attr("id_editing")),
						"SS",
						{
							"name": val,
							"content": {'repetition': repetition},
							"extra": {
	                    		"subtype": "REP"
	                    	}
						}
					);
					localStorage.setItem(currentTab, JSON.stringify([tree.render(false)]));

					star=[];
					$.each($('.star'), function(){
						aux ="";
						$.each($(this).children('label'), function(){
							aux5 = $(this).html();
							aux5 = aux5.replace(/"/g,"\'");
							aux+= aux5;
						});
						star.push(aux);
						star.push($(this).siblings('td').find('input').val());
					});

					$("span[id="+$("#mutable-form-container").attr("id_editing")+"][type=SS].element_name").html(val);
					$("[id="+$("#mutable-form-container").attr("id_editing")+"][type=SS]").find(".relevance_body").html(
						_.template($("#repetitive-relevance-ul").html())({
							"categorias":star										
						})
					);
				}
			}else if(repetition==false){				
				$(".stars_table").before('<div role="alert" class="alert alert-ajustado alert-warning alert-dismissible error" id="id_valor_respuesta-error"><button data-dismiss="alert" class="close" type="button"><span aria-hidden="true">×</span><span class="sr-only">Close</span></button><ul><li>Existen errores referentes a los valores de repetici&oacute;n colocados.</li></ul></div>');
			}
			return true;
		}

		f9 = function(){
			/*
			*
			*	Handles conditional elements agregation
			*
			*/

			var val = $("#mutable-form-container").find("#id_enunciado").val();
			var state = $("#mutable-form-container").attr("state");
			var numero = 0;
			var cond = true
        	
        	if(state != "editing")
        	{
	        	$.each($('.select_form_val'),function(){
	        		if($(this).val() != "" && $(this).val() != undefined){
	        			numero+=1;
	        		}
	        	});

	        	if(numero!=2){
	        		cond = false
	        	}

				$("#form_id").validate({
					invalidHandler: function(event, validator){
			        	if(numero!=2){}
		        	}
				});        		
        	}else{
        		cond = val !== "";
        	}

            if($("#form_id").valid() && cond == true){
            	disableAddButton(".accept-modal");

            	if($("#mutable-form-container").attr('flag')!='true'){
            		$("#modal-agregar-elemento").modal('hide');
            	}

				var i = 0;
				var iter = 0;
				var booleano = false;
				var json = [];
				var array = [];
				var array_pos = [];
				var array_neg = [];
				var data =  JSON.parse(localStorage.getItem('cookies-ids'));

				localStorage.setItem('cookies-ids', JSON.stringify(data));
				data.ss+=1;

				if(state != "editing")
				{
					$.each($('.select_form_val'),function(){
						if(i == 0){
							array.push($('#id_valor_respuesta').val());
							array.push($('#id_valor_respuesta option:selected').text());
						}else{
							array.push($('#id_valor_respuesta'+i).val());
							array.push($('#id_valor_respuesta'+i+' option:selected').text());
						}
						i+=1;
					});

					$.each($('.select_form'), function(){
						if($(this).val() != ""){
							var dict ={};
							var element_extra = $(this).find('[selected=selected]').attr('data-valextra');
							var element = $(this).val();
							dict['element'] = element.toString();
							if(element_extra!=undefined){
								element_extra = element_extra.split(",");
							}
							dict['element_extra'] = element_extra;
							array_pos.push(dict);
						}
					});

					$.each($('.select_form1'), function(){
						if($(this).val() != ""){
							var dict ={};
							var element_extra = $(this).find('[selected=selected]').attr('data-valextra');
							var element = $(this).val();
							dict['element'] = element.toString();
							if(element_extra!=undefined){
								element_extra = element_extra.split(",");
							}
							dict['element_extra'] = element_extra;
							array_neg.push(dict);
						}
					});

					tree = new Tree(data.ss, val, {'extra':[array_pos.length,array_neg.length], 'options':[ array[0], array[2] ], 'options_val': [array[1], array[3]]}, 'added', 'SS', {'subtype': 'C'})
					for(var e in array_pos){
						json = array_pos[e]['element'].replace(/&th/g, "\"");
						array_pos[e]['element'] = json;
						json = JSON.parse(json);
						data.ss+=1;
						localStorage.setItem('cookies-ids', JSON.stringify(data));
						json.id=data.ss;
						var repl = new Tree();
						repl.load(json);
						repl.content = json.content
						tree.addChildByIndex(tree.id,tree.type,repl);
					}
					for(var e in array_neg){
						json = array_neg[e]['element'].replace(/&th/g, "\"");
						array_neg[e]['element'] = json;
						json = JSON.parse(json);
						data.ss+=1;
						localStorage.setItem('cookies-ids', JSON.stringify(data));
						json.id=data.ss;
						var repl = new Tree();
						repl.load(json);
						repl.content = json.content
						tree.addChildByIndex(tree.id,tree.type,repl);
					}

					$('.zone-selector').each(function(){

						if($(this).parent().hasClass('checked')){
						
							id = $(this).parents("div[type]").attr('id');
							type = $(this).parents("div[type]").attr('type');
							if ($('#mutable-form-container').attr('flag') != 'true'){
								if(iter==0){
									tree.conditionalTree(tree.render(false),id,type,undefined,0,currentTab,true);
									addElement(currentTab, id, type, tree);
								}else{
									tree.conditionalTree(tree.render(false),id,type,undefined,0,currentTab,false);
									addElement(currentTab, id, type, tree);
								}
								iter+=1;
							}else{
								if(!booleano){
									$('#mutable-form-container').html(globaldef.pop());

									if(!globaldef.length){
										$('#mutable-form-container').attr('flag', 'false');
									}

									var aux = selectid.pop().replace('_-','');
								}
								
								enableAddButton(".accept-modal");
								booleano = true;
								assignConditional(tree,val,'add-conditional',array,aux);


								idtree = $("#mutable-form-container").attr("idtree");
								console.log(moves_tree.getElementByIdType(idtree, 'node'));
							}
						}
					});
				}else{
					// Se actualiza dentro del arbol la subseccion condicional
					var tree = new Tree();
					tree.load(JSON.parse(localStorage.getItem(currentTab)));
					tree.editNode(
						parseInt($("#mutable-form-container").attr("id_editing")),
						"SS",
						{
							"name": val,
							undefined,
							"extra": {
	                    		"subtype": "C"
	                    	}
						}
					);
					localStorage.setItem(currentTab, JSON.stringify([tree.render(false)]));
					$("span[id="+$("#mutable-form-container").attr("id_editing")+"][type=SS].element_name").html(val);
				}
			}else{
				if(numero!=2){
					$('#id_valor_respuesta').before('<div role="alert" class="alert alert-ajustado alert-warning alert-dismissible error" id="id_valor_respuesta-error"><button data-dismiss="alert" class="close" type="button"><span aria-hidden="true">×</span><span class="sr-only">Close</span></button><li>Deben haber 2 valores de respuestas en este elemento</li></div>')
        		}
			}
		}

		percentAdded = function(id_excluded){
			var acum = 0;
			var list = $(".percent");
			$(list).each(function(){
			  if( (id_excluded !== undefined && $(this).attr("id") !== id_excluded) || id_excluded === undefined){
			  	acum += parseFloat( $(this).html() );			  	
			  }
			});
			return acum;
		}

		disableAddButton = function(identifier){
			$(identifier).attr("disabled", "disabled");
		}

		enableAddButton = function(identifier){
			$(identifier).removeAttr("disabled");
		}

		conditionalTemplate = function(element, id, type, entero, extra){
			ss_counter = $("."+currentTab+"-body .panel[id="+id+"][type="+type+"]").find(".panel-body").eq(0).children(".panel[type=SS],.panel[type=S]").length+1;
			//ss_counter = $("."+currentTab+"-body .panel[id="+id+"][type="+type+"] .panel[type=SS]").length+1;
			parent_counter = $("[id="+id+"][type="+type+"]").attr("element_fisical_idenfitier");

		 	if(element.extra.subtype == "D"){
		    	$("[id="+id+"][type="+type+"] .panel-body").eq(0).append(
                _.template(
                  $("#subseccion-template").html())({
                  	"condicion": entero == "P"? "Condici&oacute;n Positiva" : "Condici&oacute;n Negativa",
                    "name": element.name,
                    "id": element.id,
                    "body": extra,
                    "tipo": 'D',
                    "parent_counter": parent_counter,
                    "counter": ss_counter,
                    "identifier": _.uniqueId("radio")
                  })
                )
            }else{
                if(element.extra.subtype == "E"){
                  $("[id="+id+"][type="+type+"] .panel-body").eq(0).append(
                	_.template(
                    $("#subseccion-template").html() )({
						"condicion": entero == "P"? "Condici&oacute;n Positiva" : "Condici&oacute;n Negativa",
						"name": element.name,
						"id": element.id,
						"body": extra,
						"tipo": 'E',
						"parent_counter": parent_counter,
						"counter": ss_counter,
						"identifier": _.uniqueId("radio")
                    })
                  )
                }else{
                  	if(element.extra.subtype == "R"){
                    	$("[id="+id+"][type="+type+"] .panel-body").eq(0).append(
	                    _.template(
	                    	$("#subseccion-rango-template").html())({
		                        "condicion": entero == "P"? "Condici&oacute;n Positiva" : "Condici&oacute;n Negativa",
		                        "name": element.name,
			                    "id": element.id,
			                    "placeholder": extra,
		                        "tipo": 'R',
		                        "parent_counter": parent_counter,
		                        "counter": ss_counter
	                    	})
	                    )
                  	}else{
                      	if(element.extra.subtype == "REP"){
	                    	$("[id="+id+"][type="+type+"] .panel-body").eq(0).append(
	                    	_.template(
		                        $("#subseccion-repetitive-template").html())({
			                        "condicion": entero == "P"? "Condici&oacute;n Positiva" : "Condici&oacute;n Negativa",
			                        "name": element.name,
				                    "id": element.id,
				                    "categorias": extra,
				                    "parent_counter": parent_counter,
				                    "counter": ss_counter
		                        })
                      		)
                      		$(".panel_subsec[id="+element.id+"][type='SS'] .panel-heading").iCheck({
								checkboxClass: 'icheckbox_minimal',								   
								radioClass: 'iradio_minimal',
							    increaseArea: '20%'
							})
                    	}else if(element.extra.subtype == "F"){
                    		$("[id="+id+"][type="+type+"] .panel-body").eq(0).append(
								_.template( $("#subseccion-formula-template").html())({
									"condicion":entero == "P"? "Condici&oacute;n Positiva" : "Condici&oacute;n Negativa",
									"enunciado": element.name,
									"id": element.id,
									'strformula': extra,
									"parent_counter": parent_counter,
									"counter": ss_counter							
								})
							);
                    	}
                	}
            	}
        	}
        	$(".panel_subsec[id="+element.id+"][type='SS'] .panel_body_subsec").iCheck({
			    radioClass: 'iradio_minimal',
			    increaseArea: '20%'
			})
		}

		assignConditional= function(tree,val,code,arraynuevo,aux){

			tree = JSON.stringify(tree.render(false)).replace(/"/g, "&th");
			$('#modal-agregar-elemento-body').hide();
			$.each($('#'+aux).children(), function(){
				$(this).removeAttr('selected');
			});
			if (arraynuevo != undefined){
				$('#'+aux).append('<option class="select_option" value="'+tree+'" data-valextra="'+arraynuevo+'" selected="selected">'+val+'</option>');
				
			}else{
				$('#'+aux).append('<option class="select_option" value="'+tree+'" selected="selected">'+val+'</option>');
			}
			$('#mutable-form-container').show();
			console.log("globaldef = "+globaldef.length)
			
			/*if(globaldef.length==0){
				$('#mutable-form-container').removeAttr('flag');
				$("#modal-agregar-contenido-footer").attr('data-dismiss','modal');
			}*/

			$('.accept-modal').removeClass(code);
			$('.accept-modal').addClass('add-conditional');
			$("#modal-agregar-elemento-title").html('');
			$("#modal-agregar-elemento-title").html(
				"<i class='fa fa-plus'></i>&nbsp;Agregar Elemento&nbsp;\
				<i class='fa  fa-angle-right'></i>&nbsp;Subseccion Respuesta Condicional"
			);
		}

		$(document).on('click', '.select_option', function(){
			$.each($(this).siblings(),function(){
				$(this).removeAttr('selected');
			});
			$(this).attr('selected','selected');
		});		

		evaluarFormula = function(zone){
			/*
			*
			*
			* Evaluate complexity and validate formula sintax and semantic
			*
			*/
			var tp = '';
			var type = '';
			var valid = $(zone).children().length && true;
			var pos = 0;
			var cp = $('.componente-formula').length - 1; 
			$(zone).children().each(function(){

				console.log($(this).find('select'));
				console.log(! $(this).find('select').length );

				if( !$(this).children('select').length )
				{
					type = $(this).attr('type');
					type_n = $(this).next().attr('type');
					type_p = $(this).prev().attr('type');
					tp = $(this).text().trim();

					if( type == 'operador-formula' ) {					
						tp = (tp == '+' || tp == '-' || tp == '*' || tp == '/')*2 + (tp=='%')*1;					
						if(tp)
						{
							if(tp == 1)
							{
								valid = valid && ( (type_p != undefined && type_p == 'indice-formula' && type_n == undefined ) || ( type_p!= undefined && type_p == 'indice-formula' && type_n != undefined && type_n == 'operador-formula' ) );
							}else if(tp == 2){
								valid = valid && (pos &&  ( (type_p != undefined && type_p == 'indice-formula' && type_n != undefined && type_n=='indice-formula' ) || ( $(this).prev().text().trim() == '%' && type_n != undefined && type_n == 'indice-formula' ) ) );
							}
						}					
					}else if( type == 'indice-formula'){
						valid = valid &&  ( (!pos && ( (type_p == undefined && type_n==undefined)||(type_n != undefined && type_n == 'operador-formula')) ) || (cp == pos && (type_n == undefined && type_p != undefined && type_p == 'operador-formula'))|| ( type_n != undefined && type_p != undefined && type_p == 'operador-formula' && type_n == 'operador-formula' ) );
					}
				}else{
					valid=false;
				}
				pos++;
				return valid;c
			});
			console.log("Formula Valida: "+valid);
			return valid;
		}

		f10 = function(){
			/*
			*
			* Add subsection element using formula as answer type
			*
			*/
			$('#form_id').validate();
			var val_formula = evaluarFormula(".formula-container");
			var val_form = $('#form_id').valid();
			var ss_counter = undefined;
			var parent_counter = "";

			if(val_formula && val_form) {
				disableAddButton(".accept-modal");
				var data =  JSON.parse(localStorage.getItem('cookies-ids'));
				var val = $("#mutable-form-container textarea#id_enunciado").val();
				var strformula = strformula_normal = '';
				
				var l = [];
				var logical_per_category =  [];
				var type = '';
				
				$(".formula-container").children().each(function(){
					type = $(this).attr("type");
					if( type == "indice-formula" )
					{
						l.push({ 'type': 'operando', 'id': $(this).attr('id'), 'name': $(this).text().trim()});
					}else if( type == "operador-formula" ){
						l.push({ 'type': 'operador', 'id': $(this).attr('id'), 'name': $(this).text().trim()});
					}

					strformula += $(this).text().trim()+"&nbsp;";
					strformula_normal += $(this).text().trim()+" ";
				});
				
				$(".stars_table").find("td select").each(function(){
				  logical_per_category.push( $(this).val() );
				});

				if ($('#mutable-form-container').attr('flag') != 'true'){
					$('#modal-agregar-elemento').modal('hide');
				}

				/* Proceso normal de agregacion de elementos dentro del cookie de los requisitos */
				var state = $("#mutable-form-container").attr("state");
				var booleano = false;

				if(state != "editing"){
					$('.zone-selector').each(function(){
						
						if( $(this).parent().hasClass('checked') ){					
							data.ss+=1;
							localStorage.setItem('cookies-ids', JSON.stringify(data));					
							id = $(this).parents("div[type]").attr('id');
							type = $(this).parents("div[type]").attr('type');
							star=[];
							
							ss_counter = $("."+currentTab+"-body .panel[id="+id+"][type="+type+"]").find(".panel-body").eq(0).children(".panel[type=SS],.panel[type=S]").length+1;
							parent_counter = $("[id="+id+"][type="+type+"]").attr("element_fisical_idenfitier");

							
							if ($('#mutable-form-container').attr('flag') != 'true'){
								$("[id="+id+"][type="+type+"] .panel-body").eq(0).append(
									_.template( $("#subseccion-formula-template").html() )({
										"condicion":"",
										"enunciado": val,
										"id": data.ss,
										'strformula': strformula,
										"parent_counter": parent_counter,
										"counter": ss_counter
									})
								);
								addElement(
									currentTab,
									id,
									type,
									new Tree( 
										data.ss, 
										val, 
										{ 'formula-elements': l, 'logical_per_category': logical_per_category }
										, 'added', 'SS', {'subtype': 'F'}
									)
								);
							}else{
								if(booleano != true){
									$('#mutable-form-container').html(globaldef.pop());

									if(!globaldef.length){
										$('#mutable-form-container').attr('flag', 'false');
									}

									var aux = selectid.pop().replace('_-','');
								}
								
								enableAddButton(".accept-modal");
								booleano = true;
								var tree = new Tree(data.ss, val, { 'formula-elements': l,'formula_string': strformula, 'logical_per_category': logical_per_category }, 'added', 'SS', {'subtype': 'F'})
								assignConditional(tree,val,'add-formula',strformula,aux);
							}	

							$("[id="+data.ss+"][type=SS] input").iCheck({
							    checkboxClass: 'icheckbox_minimal',			   
							    increaseArea: '20%'
							});

							
						}
					});
				}else{
					// Se actualiza dentro del arbol la subseccion formula
					var tree = new Tree();
					tree.load(JSON.parse(localStorage.getItem(currentTab)));
					
					console.log("TREE: ");
					console.log(tree.render(false));

					tree.editNode(
						parseInt($("#mutable-form-container").attr("id_editing")),
						"SS",
						{
							"name": val,
							"content": { 'formula-elements': l, 'logical_per_category': logical_per_category },
							"extra": {
	                    		"subtype": "F"
	                    	}
						}
					);
					localStorage.setItem(currentTab, JSON.stringify([tree.render(false)]));
					$("[id="+$("#mutable-form-container").attr("id_editing")+"][type=SS]").find(".formula-name").html(val);
					$("[id="+$("#mutable-form-container").attr("id_editing")+"][type=SS]").find(".formula-input").eq(0).attr("placeholder", "Valor de evaluación "+strformula_normal);			
				}

				return true;

			}else{

				if(!val_formula){
					$(".formula-container").parent("div").prepend(
						_.template($("#notification-zone").html())(
						{
							'close': true,
							'msg': "La formula creada no posee un formato correcto, recuerde que debe ser una expresi&oacute;n matem&aacute;tica sem&aacute;ntica y sint&aacute;cticamente correcta"
						})
					);
				}
				return false;
			}
		}

		deleteConfirmationRequest = function() {
			$("#notificacion #notificacion-Label").html("Solicitud de Confirmaci&oacute;n");
			$("#notificacion #notificacion-body").html("<h4>¿Realmente desea eliminar este elemento?</h4>");
		    
		    $('#notificacion-footer').html('<div class="col-xs-6">\
	        	<a class="col-xs-12 btn btn-danger btn-flat cancel-modal" data-dismiss="modal">Cancelar</a>\
	        </div>\
	        <div class="col-xs-6">\
	        	<a class="col-xs-12 btn btn-primary btn-flat accept-modal deletion-ok" data-dismiss="modal">Aceptar</a>\
	        </div>');

		    $('#notificacion').modal({
		        keyboard: false,
		        backdrop: 'static'
		    });

		    var me = this;

		    $(".deletion-ok").click(function(){
		    	/*
		    	*
		    	* Handle elements deletion
		    	*
		    	*/
		    	var id = $(me).attr('id');
		    	var type = $(me).attr('type_delete');
		    	var aux = JSON.parse(localStorage.getItem(currentTab));
		    	var treeaux = new Tree();
		    	treeaux.load(aux);
		    	var i =0;
		    	var sl = [];
		    	var str = '';
		    	var identifier_p = [];

		    	/*
		    		Proceso de eliminacion prezosa de los elementos internos
		    		del localStorage. <<mARCADo>>
		    	*/
		    	treeaux.getElementByIdType(id,type,true,{'state':"delete"});
		    	localStorage.setItem(currentTab,JSON.stringify([treeaux.render(false)]))

		    	if(type == "AF"){
		    		$(me).parents('.panel_af').remove();
		    		
		    		// Reenumerar elementos dentro de los aspectos fundamentales
		    		$("."+currentTab+"-body .panel_af").each(function()
		    		{
						i++;

						//Se actualiza el contador actual
						$(this).attr("element_fisical_idenfitier", i);
						$(this).find(".panel-heading b span[type=AF].element_fisical_idenfitier").html(i+".");

						// Se actualia el identificador del padre
						$(this).parent().find(".panel").each(function(){
							
							str = $(this).attr("element_fisical_idenfitier");
							sl = str.split(".");
							sl[0] = i;

							$(this).attr("element_fisical_idenfitier", sl.join("."));
							$(this).find(".panel-heading b span[type=AF].element_fisical_idenfitier_super, .panel-heading b span[type=S].element_fisical_idenfitier_super, .panel-heading b span[type=SS].element_fisical_idenfitier_super").eq(0).html(sl.slice(0, sl.length>0?sl.length-1:0).join("."));
						});
		    		});

		    	}else if(type == "S"){

		    		// Enumaracion para secciones o elementos contenidos de primer nivel dentro 
		    		// de los elementos seccion		    		
		    		$(me).parents(".panel-body").eq(0).children(".panel").each(function(){
		    			if(($(this).attr("id")!==id && $(this).attr("type")===type)||$(this).attr("type")!==type)
		    			{
							i++;
							str = $(this).attr("element_fisical_idenfitier");
							sl = str.split(".");
							sl[sl.length-1] = i;
							$(this).attr("element_fisical_idenfitier", sl.join("."));
							$(this).find(".panel-heading b span[type=S].element_fisical_idenfitier, .panel-heading b span[type=SS].element_fisical_idenfitier").eq(0).html(i+".");
							
							identifier_p = sl;

							// Se actualia el identificador del padre
							$(this).parent().find(".panel").each(function(){
								
								str = $(this).attr("element_fisical_idenfitier");
								sl = str.split(".");
								
								for(var j=0;j<identifier_p.length;++j)
								{
									sl[j] = identifier_p[j];									
								}
								sl[sl.length-1] = i;									

								$(this).attr("element_fisical_idenfitier", sl.join("."));
								$(this).find(".panel-heading b span[type=S].element_fisical_idenfitier_super, .panel-heading b span[type=SS].element_fisical_idenfitier_super").eq(0).html(sl.slice(0, sl.length>0?sl.length-1:0).join("."));
							});
						}
		    		});

		    		$(me).parents('#'+id+'.panel_sec').remove();

		    	}else if(type == "SS"){

					$(me).parents(".panel-body").eq(0).children(".panel").each(function(){
						if(($(this).attr("id")!==id && $(this).attr("type")===type)||$(this).attr("type")!==type)
						{
							i++;
							str = $(this).attr("element_fisical_idenfitier");
							sl = str.split(".");
							console.log(sl);
							sl[sl.length-1] = i;
							$(this).attr("element_fisical_idenfitier", sl.join("."));
							$(this).find(".panel-heading b span[type=S].element_fisical_idenfitier, .panel-heading b span[type=SS].element_fisical_idenfitier").eq(0).html(i+".");
						
							identifier_p = sl;

							// Se actualia el identificador del padre
							$(this).parent().find(".panel").each(function(){
								
								str = $(this).attr("element_fisical_idenfitier");
								sl = str.split(".");
								
								for(var j=0;j<identifier_p.length;++j)
								{
									sl[j] = identifier_p[j];									
								}
								sl[sl.length-1] = i;									

								$(this).attr("element_fisical_idenfitier", sl.join("."));
								$(this).find(".panel-heading b span[type=S].element_fisical_idenfitier_super, .panel-heading b span[type=SS].element_fisical_idenfitier_super").eq(0).html(sl.slice(0, sl.length>0?sl.length-1:0).join("."));
							});
						}
					});

		    		$(me).parents('#'+id+'.panel_subsec').remove();
		    	}

		    	// Mostrar mensaje de alerta una vez que se han eliminado 
		    	// todos los elementos dentro de la pestanha
		    	if($("."+currentTab+"-body").children().length === 1){
		    		$("."+currentTab+"-alert").show();
		    	}

		    	$(".zone-selector").each(function(){
		    		$(this).iCheck('enable');
		    		$(this).iCheck('uncheck');
		    		$(this).iCheck('update');

		    		if($(this).hasClass("choosen-one"))
		    		{
		    			$(this).removeClass("choosen-one");
		    		}
		    	});

		    	autosave();
		    });
		}

		main_generator = function(evnt, code, tree){

			// Se limpia el contenedor de las configuraciones en casos
			// donde se detecta que se esta creando un seccion condicional
			if ($('#mutable-form-container').attr('flag') == 'true'){
				$('#mutable-form-container').html('');
			}

			$("#mutable-form-container").attr("state", "add");
			$("#mutable-form-container").attr("id_editing", -1);

			var code_element = code == undefined ? $(this).attr('id'): code;
			var data =  JSON.parse(localStorage.getItem("main-config-cookie"));

			$("#modal-agregar-elemento-body" ).hide();
			$(".modal-spinner-container-add-elment").append($("#spinner-zone").html());

			if( data != undefined ){
				$.ajax({
		       		type: 'GET',
					url: 'obtener-form-elemento',
					data:{
						'code': code_element,
						'tabulador': data[0].id,
						'current_tab': currentTab
					},
					success:function(server_data){
						
						if (code_element=="E_ASPECTOF"){
							nombre="Aspectos Fundamentales";
							accept = "add-fundamental-aspect";
						}else if (code_element=="E_SECCION"){
							nombre = "Secciones";
							accept = "add-section";
						}else if(code_element=="D"){
							nombre = "Subsecci&oacute;n Respuesta Dual"
							accept = "add-dual"
						}else if(code_element=="E"){
							nombre = "Subsecci&oacute;n Escala"
							accept = "add-escala"
						}else if(code_element=="R"){
							nombre = "Subsecci&oacute;n Respuesta Rango"
							accept = "add-rango"
						}else if(code_element=="REP"){
							nombre = "Subsecci&oacute;n Repetitiva"
							accept = "add-repetitive"
						}else if(code_element=="C"){
							nombre= " Subsecci&oacute;n Condicional"
							accept = "add-conditional"
						}else if(code_element=="F"){
							nombre= " Subsecci&oacute;n F&oacute;rmula"
							accept = "add-formula"
						}
						
						$("#modal-agregar-elemento-title").html(
							"<i class='fa fa-plus'></i>&nbsp;Agregar Elemento&nbsp;\
							<i class='fa  fa-angle-right'></i>&nbsp;"+nombre+""
						);

						$(".modal-spinner-container-add-elment .spinner-zone-realm").fadeOut("slow").remove();
						$( "#modal-agregar-elemento-body" ).hide();

						if (code_element !== "E_ASPECTOF" && code_element !== "E_SECCION"){

							var aux = '<form id="form_id" method="GET" action="" class="formulario_val">'+server_data.form+'</form>'
	               			$("#mutable-form-container").html(aux);
	               			
	               			if (code_element == "E"){

	               				var num = $('.select_form').length;
	               				//  Colocar boton de valores de respuesta (Bueno/Malo/Deficiente)
	               				label_text = $('#id_valor_respuesta').prev("label").text();
	               				$('#id_valor_respuesta').prev("label").remove();

	               				$('#id_valor_respuesta').before( 
	               					_.template($("#add_more_scale_dual_response_template").html())({
	               						'label_text': label_text,
	               						'sub': 'E',
	               						'num': num
	               					})            					
	               				);

	               			}else if (code_element == "D"){

	               				var num = $('.select_form').length;
	               				//  Colocar boton de valores de respuesta (SI/NO)
	               				label_text = $('#id_valor_respuesta').prev("label").text();
	               				$('#id_valor_respuesta').prev("label").remove();

	               				$('#id_valor_respuesta').before( 
	               					_.template($("#add_more_scale_dual_response_template").html())({
	               						'label_text': label_text,
	               						'sub': 'D',
	               						'num': num
	               					})            					
	               				);

	               			}else if (code_element == "C"){
	               				$('#id_valor_respuesta').find('option').addClass('select_option');
	               				
	               				// Instanciando la variable publica con el valor del select 
	               				// cargado de django
	               				var aux = $('#id_conjunto_de_condiciones_positiva').clone();
	               				var label_text = "";
	               				var select = undefined;
	               				aux.addClass('form-control');
	               				aux.addClass('select_form');
	               				globalselect.push(aux);

	               				//	Instanciando la variable publica con el valor del select 
	               				// cargado de django
	               				aux = $('#id_conjunto_de_condiciones_negativa').clone();
	               				aux.addClass('form-control');
	               				aux.addClass('select_form1');
	               				globalselectneg.push(aux);


	               				// Parte de renderizado de los elementos de la subseccion condicional

	               				//  Colocar boton de valores de respuesta (SI/NO)
	               				label_text = $('#id_valor_respuesta').prev("label").text();
	               				$('#id_valor_respuesta').prev("label").remove();

	               				$('#id_valor_respuesta').before( 
	               					_.template($("#add_valor_respuesta_template").html())({
	               						'label_text': label_text
	               					})               					
	               				);

	               				// Colocar el boton de nuevo elemento dentro de la seccion
	       
	               				label_text = $('#id_conjunto_de_condiciones_positiva').prev("label").text();
	               				$('#id_conjunto_de_condiciones_positiva').prev("label").remove();

	               				$('#id_conjunto_de_condiciones_positiva').before( 
	               					_.template($("#add_conjunto_de_condiciones_positiva_template").html())({
	               						'label_text': label_text
	               					})
	               				);
	               				
	               				select = $('#id_conjunto_de_condiciones_positiva');

	               				$('#id_conjunto_de_condiciones_positiva').after(
	               					_.template($("#removable_div_container_template").html())({
	               						'elemento_comportamiento': select[0].outerHTML,
	               						'remove_hidden': true,
	               						'tipo_condicion': 'positiva_-',
	               						'id': undefined
	               					})
	               				);
	               				$(select).remove();

	               				// Colocar el boton de nuevo elemento dentro de la 
	               				// seccion condicional negativa
	               				label_text = $('#id_conjunto_de_condiciones_negativa').prev("label").text();
	               				$('#id_conjunto_de_condiciones_negativa').prev("label").remove();

	               				$('#id_conjunto_de_condiciones_negativa').before( 
	               					_.template($("#add_conjunto_de_condiciones_negativa_template").html())({
	               						'label_text': label_text
	               					})               					
	               				);

	               				select = $('#id_conjunto_de_condiciones_negativa');	               				
	               				
	               				$('#id_conjunto_de_condiciones_negativa').after(
	               					_.template($("#removable_div_container_template").html())({
	               						'elemento_comportamiento': select[0].outerHTML,
	               						'remove_hidden': true,
	               						'tipo_condicion': 'negativa_-',
	               						'id': undefined
	               					})
	               				);
	               				$(select).remove();

	               			}else if(code_element == "F"){

	               				var enunciado = "<span class='col-xs-11'>"+$($("#mutable-form-container").find("input#id_enunciado")[0]).parent().html()+"</span>";
	               				$($("#mutable-form-container").find("input#id_enunciado")[0]).parent().html(
	               					"<div class='row'>"+ enunciado +"</div>"
	               				);
								
	               				var s = "<span class='col-xs-11'>"+$($("#mutable-form-container").find("select#id_operando")[0]).parent().html()+"</span>";
	               				$($("#mutable-form-container").find("select#id_operando")[0]).parent().html(
	               					"<div class='row'>"+ s + _.template($("#plus-button-template").html())({
	               						'id': 'id_operando'
	               					})+"</div>"
	               				);

	               				var s = "<span class='col-xs-11'>"+$($("#mutable-form-container").find("select#id_operador")[0]).parent().html()+"</span>";
	               				$($("#mutable-form-container").find("select#id_operador")[0]).parent().html(
	               					"<div class='row'>"+ s + _.template(
	               						$("#plus-button-template").html()
	               					)({
	               						'id': 'id_operador'
	               					})+"</div>"
	               				);

	               				// Mantenemos desactivados los aperadores como opcion por defecto
	               				$("#id_operador").prop("disabled", true);
	               				$(".id_operador").attr("disabled","disabled");

	               				$("#mutable-form-container").append( $("#formula-zone").html() );
	               			}
						}else{

							// Solo se agrega el formulario si el elemento a agregar 
							// es un AF y el porcentaje agregado es distinto a 100%
							var acum = code_element === 'E_ASPECTOF' && currentTab === "specific-req" ? percentAdded():0;
							var aux = code_element === 'E_SECCION' || (code_element === 'E_ASPECTOF' && currentTab === "basic-req") || (code_element === 'E_ASPECTOF' && currentTab === "specific-req" && (acum<100.0||(code != undefined && tree != undefined)) ) ? '<form id="form_id" method="GET" action="" class="formulario_val">'+server_data.form+'</form>': _.template($("#notification-zone").html())({'msg':"La agregación de más aspectos fundamentales no esta permitida debido a que ya el porcentaje de asignación máximo (100%) ha sido alcanzado."});

							// Colocando formulario para aspectos fundamentales
							$("#mutable-form-container").html(aux);

							if( code_element === "E_ASPECTOF" && currentTab === "specific-req" && (acum < 100.0||(code != undefined && tree != undefined))){
								
								// Colocar los aspectos fundamentales
								// Solo se agrega el controlador de porcentaje
								// en los casos donde el tipo de requisito es
								// requisito especifico de acuerdo a las especificaciones
								// de la resolucion

								acum = 0.0;
								var able = 0.0;
								var offset = tree == undefined ? 0 : tree.extra.percent;

								$(".percent").each(function(){
									acum += parseFloat( $(this).html() );
								});			

								$("#id_peso_porcentual").attr("max", 100.0 - (acum - offset));

		           				$("#form_id").append(
		           					_.template( $("#percent-zone").html() )({
		           						"percent": $("#mutable-form-container").find(
		           							"#id_peso_porcentual"
		           						).val()
		           					})
		           				);	           				

		           				$("#id_peso_porcentual").on("change, click", function(){
		           					$("#percent-number").val(
		           						parseFloat($("#mutable-form-container").find("#id_peso_porcentual").val())
		           					);
		           					if((100.0 - percentAdded() + $(this).val()) >= 0)
		           					{
		           						enableAddButton(".accept-modal");
		           					}else{
		           						disableAddButton(".accept-modal");
		           					}
		           				});

		           				$(document).on("change, mouseenter, mouseleave", "#percent-number", function(){
		           					$("#mutable-form-container").find("#id_peso_porcentual").val(
		           						parseFloat($(this).val())
		           					);
		           					if((100.0 - percentAdded() + $(this).val()) >= 0)
		           					{
		           						enableAddButton(".accept-modal");
		           					}else{
		           						disableAddButton(".accept-modal");
		           					}     					
		           				});
	           				}
						}						
						
						$("#modal-agregar-contenido-footer").html(
							"<div class='col-xs-6'><a \
							  class='col-xs-12 btn btn-danger btn-flat cancel-modal' data-dismiss='modal'>\
							  Cancelar\
							</a></div>\
							<div class='col-xs-6'><a \
							  class='col-xs-12 btn btn-primary btn-flat accept-modal "+accept+"'>\
							  "+(code != undefined && tree != undefined? 'Terminar Edici&oacuten':'Agregar')+"</a>\
							</div>"
						);

						$("#modal-agregar-contenido-footer").removeAttr('data-dismiss');

						if (code_element == "C"){
							$('.cancel-modal').addClass('cancel-modal-conditional');
							$('.cancel-modal-conditional').removeClass('cancel-modal');
						}

						if ($('#mutable-form-container').attr('flag') == 'true'){
							$("#modal-agregar-contenido-footer").removeAttr('data-dismiss');
							$.each($("#modal-agregar-contenido-footer").find('[data-dismiss=modal]'), function(){
								$(this).removeAttr('data-dismiss');
							});
						}

						// Edicion de los elementos:
						// Se tipifica el elemento y se regenera el formulario 
						// con los valores necesarios para permitir la edicion
						if( code != undefined && tree != undefined ){

							if (code == "E_ASPECTOF")
							{
								$("#mutable-form-container #id_nombre").val(tree.name);
								$("#mutable-form-container #id_tipo_aspecto").val(tree.extra.tipo_aspecto);

								if(currentTab === "specific-req" )
								{
									$("#mutable-form-container #id_peso_porcentual").val(tree.extra.percent);
									$("#mutable-form-container #percent-number").val(tree.extra.percent);									
								}
								
								// Se marca el caso dentro del formulario para dentar que el mismo
								// esta en estado de edicion
								$("#mutable-form-container").attr("state", "editing");
								$("#mutable-form-container").attr("id_editing", tree.id);

								$('#mutable-form-container input,textarea,select').each(function(){
								    $(this).addClass('form-control');
								});

							}else if(code == "E_SECCION"){
								// Se marca el caso dentro del formulario para dentar que el mismo
								// esta en estado de edicion
								$("#mutable-form-container").attr("state", "editing");
								$("#mutable-form-container").attr("id_editing", tree.id);

								$("#mutable-form-container #id_nombre").val(tree.name);
								$('#mutable-form-container input,textarea,select').each(function(){
								    $(this).addClass('form-control');
								});
							}else if(code == "D" || code == "E"){
								// Se marca el caso dentro del formulario para dentar que el mismo
								// esta en estado de edicion
								$("#mutable-form-container").attr("state", "editing");
								$("#mutable-form-container").attr("id_editing", tree.id);

								$("#mutable-form-container #id_enunciado").val(tree.name);
								var clone = last_select = undefined;

								$(".select_form").val(parseInt(tree.content.options[0]));
								
								for(var i=1; i< tree.content.options.length; i++)
								{
									last_select = $(".select_form").last();
									clone = $(last_select).clone();

									$(clone).attr("id", "id_valor_respuesta"+i);
									$(clone).val(parseInt(tree.content.options[i]));
									$(last_select).after(clone);
								}

								$('#mutable-form-container input,textarea,select').each(function(){
								    $(this).addClass('form-control');
								});

								for(var j=0; j < tree.content.relevance.length; ++j)
								{
									$('input[type=checkbox][name=star_'+j.toString()+']').prop('checked', tree.content.relevance[j]);
								}

							}else if(code == "R"){
								// Se marca el caso dentro del formulario para dentar que el mismo
								// esta en estado de edicion
								$("#mutable-form-container").attr("state", "editing");
								$("#mutable-form-container").attr("id_editing", tree.id);

								$('#mutable-form-container input,textarea,select').each(function(){
								    $(this).addClass('form-control');
								});

								$("#mutable-form-container #id_enunciado").val(tree.name);
								$("#mutable-form-container #id_unidad_o_medida").val(tree.content.unit);

								for(var i=0; i<tree.content.relevance_value.length; ++i)
								{
									$('input[type=checkbox][name=inf_aplica_'+i+']').prop('checked', tree.content.relevance_value[i].inf_aplica);
									$('input[type=checkbox][name=sup_aplica_'+i+']').prop('checked', tree.content.relevance_value[i].sup_aplica);
									$('input[type=number][name=inf_star_'+i+']').val(tree.content.relevance_value[i].inf_aplica?tree.content.relevance_value[i].inf_star:'');
									$('input[type=number][name=sup_star_'+i+']').val(tree.content.relevance_value[i].sup_aplica?tree.content.relevance_value[i].sup_star:'');	
									$('input[type=number][name=inf_star_'+i+']').prop("disabled",!tree.content.relevance_value[i].inf_aplica);
									$('input[type=number][name=sup_star_'+i+']').prop("disabled",!tree.content.relevance_value[i].sup_aplica);
								}

							}else if(code == "C"){
								// Se marca el caso dentro del formulario para dentar que el mismo
								// esta en estado de edicion
								$("#mutable-form-container").attr("state", "editing");
								$("#mutable-form-container").attr("id_editing", tree.id);
								
								var label = $("#mutable-form-container label[for=id_enunciado]");
								var enunciado = $("#mutable-form-container #id_enunciado");
								var aux = '<form id="form_id" method="GET" action="" class="formulario_val">'+label[0].outerHTML+enunciado[0].outerHTML+'</form>'
	               				$("#mutable-form-container").html(aux);
								$("#mutable-form-container #id_enunciado").val(tree.name);

								$('#mutable-form-container input,textarea,select').each(function(){
								    $(this).addClass('form-control');
								});
							}else if(code == "F"){
								// Se marca el caso dentro del formulario para dentar que el mismo
								// esta en estado de edicion
								$("#mutable-form-container").attr("state", "editing");
								$("#mutable-form-container").attr("id_editing", tree.id);

								$('#mutable-form-container input,textarea,select').each(function(){
								    $(this).addClass('form-control');
								});

								$("#mutable-form-container #id_operador").prop("disabled", false);
								$("#mutable-form-container #id_enunciado").val(tree.name);

								for(var i=0;i<tree.content.logical_per_category.length;++i)
								{
									$('select[name=star_'+i+']').val(parseInt(tree.content.logical_per_category[i]));
								}	

								for(var j=0; j< tree.content["formula-elements"].length;++j)
								{
									$(".formula-container").append(
										_.template( $("#elemento-formula").html() )({
											'id': tree.content["formula-elements"][j].id,
											'representacion':tree.content["formula-elements"][j].name,
											'value':  tree.content["formula-elements"][j].name,
											'type': tree.content["formula-elements"][j].type == "operando" ? 'indice-formula': 'operador-formula',
											'space': 2,
											'color': tree.content["formula-elements"][j].type == "operando" ? '#000': '#367fa9'
										})
									);
								}
							}else if(code == "REP"){
								// Se marca el caso dentro del formulario para dentar que el mismo
								// esta en estado de edicion
								$("#mutable-form-container").attr("state", "editing");
								$("#mutable-form-container").attr("id_editing", tree.id);

								$('#mutable-form-container input,textarea,select').each(function(){
								    $(this).addClass('form-control');
								});

								$("#mutable-form-container #id_enunciado").val(tree.name);

								for(var i=0; i<tree.content.repetition.length;++i)
								{
									$('input[type=number][name=star_'+i+']').val(parseInt(tree.content.repetition[i]));
								}
							}
						}

						$("#mutable-form-container").show();

						$('input,textarea,select').each(function(){
						  if(!$(this).is(":hidden")){
						    $(this).addClass('form-control');
						  }
						});

						$('#mutable-form-container input').iCheck({
						    checkboxClass: 'icheckbox_minimal',
						    radioClass: 'iradio_minimal',
						    increaseArea: '20%'
						});

						if( code_element == "R" )
						{
							$(".stars_table").find("tbody td input[type=checkbox]").each(function(){
							  
							  $(this).parent().on('ifUnchecked', function(){
							  	$(this).parent("td").prev().find('input').val('').attr('disabled',true);
							  });
							  
							  $(this).parent().on('ifChecked', function(){
							  	$(this).parent("td").prev().find('input').val('').attr('disabled',false);
							  });
							});
						}
						
						$("#modal-agregar-elemento").modal("show");
					},
					error: function(e){
						$(".modal-spinner-container-add-elment").html(
							_.template($("#notification-zone").html())(
								{
									'msg': "Temporalmente existen problemas de conexi&oacute;n con nuestros servidores, intenelo de nuevo m&aacute;s tarde."
								}
							)
						);
						$(".modal-spinner-container-add-elment .spinner-zone-realm").remove();
						console.log(e);
					}
		       	});
			}
		}

		$(document).on('click','.contenedor-opcion', main_generator);

		$(document).on('click', '.otro_valor_cond', function(){
			if($(this).attr('sub') == "C"){
				var num = $('.select_form_val').length;
				var select = $('#id_valor_respuesta').clone();
				select.attr('id', 'id_valor_respuesta'+num);				
				
				// Se agrega el select para el nuevo valor de respuesta
				$('#id_valor_respuesta').after(select);
				
				if(num==1){
		   			// En caso de exisitir algun componente para agregar debemos convertirlo
		   			// en un componente para eliminar elementos.
		   			$(this).attr("class", "btn btn-info btn-flat quitar_valor_cond");
		   			$(this).attr("data-original-title", "Eliminar Valor");
		   			$(this).attr("title", "Eliminar Valor")
		   			$(this).html('<i class="fa fa-minus icon-white"></i>');
				}
			}
		});

		$(document).on('click', '.quitar_valor_cond', function(){
			if($(this).attr('sub') == "C"){
				var num = $('.select_form_val').length;
				var num1 = num-1;

				if(num==2){

					// Existe elemento de eliminacion, cambiamos el icono
					// y eliminamos el componente icono del simbolo positivo de
					// suma al simbolo de resta
					$('#id_valor_respuesta'+num1).remove();
       				$(this).attr("class", "btn btn-info btn-flat otro_valor_cond");
       				$(this).attr("data-original-title", "Agregar Valor");
       				$(this).attr("title", "Agregar Valor")
       				$(this).html('<i class="fa fa-plus icon-white"></i>');
       			}
       		}
       	});		

		$(document).on('click', '.otro_valor', function(){

			if($(this).attr('sub') === "D" || $(this).attr('sub') === "E"){
				// Reutilizacion de la funcion de agregacion dinamica de elementos
				// se emplea este campo para colocar nuevos elementos en las secciones
				// que posea el icono (plus) de agregacion de nuevas subseccion

				var num = $('.select_form').length;
				var select = $('#id_valor_respuesta').clone();
				var last_element = $(".select_form").last();
				var top = $(this).attr('sub') == "D"? 2:3;

				if(num==top){
					$(last_element).remove();
					$(this).find("i").removeClass("fa-minus");
					$(this).find("i").addClass("fa-plus");	
					$(this).attr('title',"Agregar Valor");
					$(this).data('original-title', "Agregar Valor");		
				}

				if(num < top){
					select.attr('id', 'id_valor_respuesta'+num);
					$(last_element).after(select);
					num += 1;

					if(num==top){
						$(this).find("i").removeClass("fa-plus");
						$(this).find("i").addClass("fa-minus");
						$(this).attr('title',"Eliminar Valor");
						$(this).data('original-title', "Eliminar Valor");
					}
				}

			}else if($(this).attr('sub') == "C+") {

				/********************************
				*								*
				*  Parte condicional positiva	*
				*								*
				*********************************/

				// Conteo del total de subsecciones que componen la parte condicional positiva
				var num = $('.select_form').length;
				var last_element = $(".removable_div_container_positiva_-").length? $(".removable_div_container_positiva_-").last():$(".select_form").last();
				var select = $('#id_conjunto_de_condiciones_positiva').clone();			
				select.attr('id', 'id_conjunto_de_condiciones_positiva'+num);
				select.attr('name','id_conjunto_de_condiciones_positiva'+num);
				
				// Se agrega el componente despues del ultimo del mismo tipo detectado
				$(last_element).after(
					_.template($("#removable_div_container_template").html())({
						'elemento_comportamiento': select[0].outerHTML,
						'remove_hidden': false,
						'tipo_condicion': 'positiva_-',
						'id': num
					})
				);

			}else{

				/********************************
				*								*
				*  Parte condicional negativa	*
				*								*
				*********************************/

				// Conteo del total de subsecciones que componen la parte condicional positiva
				var num = $('.select_form1').length;
				var last_element = $(".removable_div_container_negativa_-").length? $(".removable_div_container_negativa_-").last():$(".select_form1").last();
				var select = $('#id_conjunto_de_condiciones_negativa').clone();			
				select.attr('id', 'id_conjunto_de_condiciones_negativa'+num);
				select.attr('name','id_conjunto_de_condiciones_negativa'+num);
				
				// Se agrega el componente despues del ultimo del mismo tipo detectado
				$(last_element).after(
					_.template($("#removable_div_container_template").html())({
						'elemento_comportamiento': select[0].outerHTML,
						'remove_hidden': false,
						'tipo_condicion': 'negativa_-',
						'id': num
					})
				);
      		}		

			// // Condicional para subsecciones dual y escala
			// if($(this).attr('sub') == "D"){
			// 	if(num==1){
			// 		$(this).after('<a data-toggle="tooltip" title="Eliminar Valor"\
			// 	 	sub="D" class="btn btn-info btn-flat quitar_valor data-original-title="Eliminar Valor">\
			//      		<i class="fa fa-minus icon-white"></i>\
			//   			</a>')
			//   			$(this).remove();
			// 	}
			// }else if($(this).attr('sub') == "E"){
			// 	if(num==2){
			// 		$(this).remove();
			// 	}else if(num==1){
			// 		$(this).after('<a data-toggle="tooltip" title="Eliminar Valor"\
			// 	 	sub="E" class="btn btn-info btn-flat quitar_valor data-original-title="Eliminar Valor">\
			//      		<i class="fa fa-minus icon-white"></i>\
			//   			</a>')
			// 	}
			// }			
		});

		$(document).on('click','.removable_trigger',function(){

			$(this).parents(".remove_container").remove();
		});

		$(document).on('click', '.otro_sub', function(){

			// Se valida que el contenido de la pila no sea
			// un solo elemento, en caso de ser asi quiere decir
			// que el elemento agregado es el formulario inicial
			// por lo que no debe ser agregado nuevamentes
			$("#id_enunciado").attr("value", $("#id_enunciado").val());
			$("#id_enunciado").html($("#id_enunciado").val());

			// Colocamos el nivel del arbol dentro de la estructura
			globaldef.push($('#mutable-form-container').html());

			if( moves_tree.isEmpty() )
			{
				// Se coloca la base del arbol de manera inicial en caso de que se desee
				// agregar una nueva subseccion condicional
				$('#mutable-form-container').attr("idtree", '0');
				moves_tree = new Tree(
					'0', 
					$("#id_enunciado").val(),
					$('#mutable-form-container').html(),
					undefined, 
					'node'
				);
			}

			selectid.push($(this).attr('id'));
			
			// Marcar que se esta trabjando con una subseccion condicional
			$('#mutable-form-container').attr('flag', 'true');

			// Se quita el boton de seccion dado que no se permite agregar una 
			// seccion dentro de una subseccion condicional
			$('div#E_SECCION').remove();

			// Esconder el formulario condicional que se muestra actualmente
			$('#mutable-form-container').hide();

			// Quitar la posibilidad de cerrar el modal de subsecciones
			$(".cancel-modal-conditional").removeAttr("data-dismiss");

			// Mostrar panel con los tipo de subseccion
			$('#modal-agregar-elemento-body').show();

		});

		$(document).on('click', '.cancel-modal', function(){

			if($('#mutable-form-container').attr('flag') == 'true'){
				$('#mutable-form-container').html('');
				$('#mutable-form-container').html(globaldef.pop());
				selectid.pop();
				$('#modal-agregar-elemento-body').hide();
				$('#mutable-form-container').show();
				if(globaldef.length==0){
					$('#modal-agregar-contenido-footer').attr('data-dismiss','modal');
				}				
			}

		});

		$(document).on('click', '.cancel-modal-conditional', function(){
			if($('#mutable-form-container').attr('flag') == 'true'){
				if(globaldef.length >= 1){
					$('#mutable-form-container').html('');
					$('#mutable-form-container').html(globaldef.pop());
					globalselect.pop();
					globalselectneg.pop();
					selectid.pop();
					$('#modal-agregar-elemento-body').hide();
					$('#mutable-form-container').show();
				}else{
					$("#modal-agregar-elemento").modal("hide");
				}
			}
		});

		$(document).on('click', '.quitar_valor', function(){
			var num = $('.select_form').length;
			var num1= num-1
			if($(this).attr('sub') == "D"){
				if(num==2){
					$('#id_valor_respuesta').after('<a data-toggle="tooltip" title="Agregar Valor"\
				 	sub="D" class="btn btn-info btn-flat otro_valor data-original-title="Agregar Valor">\
              		<i class="fa fa-plus icon-white"></i>\
           			</a>')
					$('#id_valor_respuesta'+num1).remove();
       				$(this).remove();
       			}
			}else if($(this).attr('sub') == "E"){
				if(num==3){
					$('#id_valor_respuesta'+num1).after('<a data-toggle="tooltip" title="Agregar Valor"\
				 	sub="E" class="btn btn-info btn-flat otro_valor data-original-title="Agregar Valor">\
	          		<i class="fa fa-plus icon-white"></i>\
	       			</a>');
				}else if(num==2){
					$(this).remove();
				}
				$('#id_valor_respuesta'+num1).remove();
			}else if($(this).attr('sub') == "C+"){
				if(num==2){					
					$(this).remove();
				}
				$('#id_conjunto_de_condiciones_positiva_-'+num1+'').remove();
				$('#id_conjunto_de_condiciones_positiva'+num1).remove();
			}else if($(this).attr('sub') == "C-"){
				var num_no = $('.select_form1').length;
				var num_no1 = num_no-1
				if(num_no==2){
					$(this).remove();
				}
				$('#id_conjunto_de_condiciones_negativa_-'+num_no1+'').remove();
				$('#id_conjunto_de_condiciones_negativa'+num_no1).remove();
			}
		});

		$(document).on('click','.add-basic-data', f1 );
		$(document).on('click','.add-documental-req', f2 );
		$(document).on('click','.add-fundamental-aspect', f3);
		$(document).on('click','.add-section', f4 );
		$(document).on('click','.add-dual', f5);
		$(document).on('click','.add-escala', f6);
		$(document).on('click','.add-rango', f7);
		$(document).on('click','.add-repetitive', f8);
		$(document).on('click','.add-conditional', f9);			
		$(document).on('click','.add-formula', f10);
		$(document).on('click','.delete-element', deleteConfirmationRequest);

		//	Generic listeners

		$(document).on('click', '.edit-global-button', function(){
			var data = JSON.parse(localStorage.getItem(currentTab));
			var tree = new Tree();
			tree.load(data);

			var id = parseInt($(this).attr('id'));
			var type = $(this).attr('type_edit');
			elem = tree.getElementByIdType(id, type);
			
			if( type == "AF" )
			{
				//consultar los aspectos fundamentales
				main_generator(undefined, "E_ASPECTOF", elem);

			}else if( type == "S" ){
				//consultar las secciones
				main_generator(undefined, "E_SECCION", elem);

			}else if( type == "SS" ){
				//consultar las sub seccionciones (esta parte sera interesante)
				main_generator(undefined, elem.extra.subtype, elem);
			}
		});

		$(document).on('click', '.editar-button', function(){
			var id = $(this).attr('id');
			var sufix = $(this).attr('sufix');
			var clss = $(this).parent().parent().parent().parent().attr('class').split(" ");
			var lclss = clss[clss.length - 1 ];

			if ($(this).attr('state') === "normal"){
				var val = "";

				$(this).parent().siblings().each(function(){
					
					if($(this).attr("iddoc") == undefined){
						val = $(this).html();
						if($(this).attr("id") != 'valor'){
							$(this).html( _.template(
								$(this).attr('id') != 'suministrado' ? $('#input-edicion').html() : $('#select-edicion').html()
							)({ "id": id, "val": val.trim()	})
							);
						}else if($(this).attr("id") === 'valor'){
							$(this).find("a").html("<i class='fa fa-pencil-square-o icon-white'></i>");
						}
					}else{
						$(this).find("div#typedoctext").remove();
						$(this).find("#id_tipo_documento").val(
							$(this).attr("iddoc")
						);
						$(this).find("#id_tipo_documento").show();
					}				
				});

				$(this).attr('state', 'editing');
				$(this).html('<i class="fa fa-check icon-white"></i>');

			}else if($(this).attr('state')==='editing'){

				if(lclss === 'table-documental-req'){
					lclss = 'documental-req-cookie';
				}else if(lclss === 'table-basic-data' ){
					lclss = 'specific-values-cookie';
				}else if(lclss === ''){
					lclss = 'specific-req';
				}else if(lclss === 'table-basic-data'){
					lclss = 'basic-req';
				}

				console.log(lclss);

				var alt_val, val = "";
				$(this).parent().siblings().each(function(){

					alt_val = false;
					val = $(this).find('input').val();
					idc = $(this).attr('id');

					if($(this).attr("iddoc") == undefined){

						// Cambio o edicion de cualquiera de las secciones
						// normales de alguno de los elementos de requisitos
						// documentales o valores especificos

						if( val === undefined ){
							val = $(this).find('select').val();				
						}

						if( val === undefined ){
							val = $(this).find('a').attr('data-value-per-categorie');
							if(val != undefined )
							{
								alt_val = _.template(
								'<a \
								  data-original-title="Valores_por_categoria" \
								  class="btn btn-info btn-flat valore-button" \
								  sufix="dato-especifico" \
								  title="Editar" \
								  data-toggle="tooltip" id="valor-especifico-categoria-eye"\
								  data-value-per-categorie = "<%= valor %>"\
								><i class="fa fa-eye icon-white"></i></a>')
								({
									'valor':val
								});
							}
						}

						if( val === undefined ){
							val = $(this).html().trim();
						}
						
						if( val === ''){val = '-';}									

						obj = {};					
						obj[idc] = idc === 'valor' && val != "N/A" ? val.split(",").map(parseFloat): val;
						
						editElement( lclss, id, obj, 'edited');					
						$(this).html( alt_val ? alt_val:val );
					}else{

						// Edicion de requisitos documentales, se maneja el cambio de
						// tipo de requisito documental
						
						$(this).append("<div id='typedoctext'>"+$(this).find("#id_tipo_documento option:selected").text().trim()+"</div>");
						$(this).attr("iddoc", $(this).find("#id_tipo_documento").val());
						
						obj = {};
						obj[idc] = $(this).find("#id_tipo_documento").val();
						
						editElement( lclss, id, obj , 'edited');
						$(this).find("#id_tipo_documento").hide();
					}
				});

				$(this).attr('state', 'normal');
				$(this).html('<i class="fa fa-pencil-square-o icon-white"></i>');				
			}
		});

		$(document).on('click', '.delete-button', function(){
			var id = $(this).attr('id');
			var sufix = $(this).attr('sufix');
			var clss = $(this).parent().parent().parent().parent().attr('class').split(" ");
			var lclss = clss[clss.length - 1 ];
			$(this).parent().parent().remove();

			if(!$("."+sufix+"-row").length){
				$('.'+lclss).hide();
				$('.'+lclss).siblings().show();	
			}

			if(lclss === 'table-documental-req'){
				lclss = 'documental-req-cookie';
			}else if(lclss === 'table-basic-data' ){
				lclss = 'specific-values-cookie';
			}else if(lclss === ''){
				lclss = 'specific-req';
			}else if(lclss === 'table-basic-data'){
				lclss = 'basic-req';
			}
			deleteElement(lclss, id);
		});

		$(document).on('change', 'select',function(){						
			var id = $(this).val();
			if( $(this).attr('id') == "id_operando" && $(".formula-container").find(".indice-formula").length ){
				$("#id_operador").prop("disabled", false);
				$(".id_operador").removeAttr("disabled");
			}
		});

		$(document).on('click', '.add-element-button', function(){
			var target = $(this).attr('target');			
			var select_e = $("#"+$(this).attr('id'));
			$(".alert-elemento").remove();

			if ( $( select_e ).val() != "" ){
				var add=false;
				if( $( select_e ).attr('id') == "id_operador" )
				{
					add = $(".formula-container").children().length && ( $(".formula-container").children().last().attr('type') == 'indice-formula' || $(".formula-container").children().last().text().trim() == '%' );
				}else if($( select_e ).attr('id') == "id_operando"){
					add = !$(".formula-container").children().length || ($(".formula-container").children().last().attr('type') == 'operador-formula' && $(".formula-container").children().last().text().trim() != '%');
				}
				if( add )
				{
					var name_indice = $(select_e).find('option:selected').text();

					$( target ).append(
						_.template( $("#elemento-formula").html() )({
							'id': $( select_e ).val(),
							'representacion':name_indice,
							'value':  name_indice,
							'type': $( select_e ).attr('id') == "id_operando"? 'indice-formula': 'operador-formula',
							'space': 2,
							'color': $( select_e ).attr('id') == "id_operando"? '#000': '#367fa9'
						})
					);

					if( $( select_e ).attr('id') == "id_operando" )
					{
						$("#id_operador").prop("disabled", false);
						$(".id_operador").removeAttr("disabled");
					}					
				}else{
					$(this).parents('div').first().parent().append(
						_.template($("#notification-zone").html())(
						{
							'close': true,
							'msg': "Para mantener la correctitud de la formula, esta operaci&oacute;n de agregaci&oacute;n no esta permitida"
						})
					)
				}
			}
		});

		$(document).on("mouseover",".componente-formula", function(){
			$(this).css("border", "1px solid #f56954");
		});

		$(document).on("mouseleave",".componente-formula", function(){
			$(this).css("border", "1px solid white");
		});		

		$(document).on("click",".componente-formula", function(){
			$(".add-formula").attr('disabled',true);
			if( !$(this).find("select").length ){
				var clone = $(this).attr("type") == "indice-formula" ? $("#id_operando").clone()[0] : $("#id_operador" ).clone()[0];
				$(clone).find("option:selected").remove();
				$(clone).prepend("<option class = 'eliminar-componente' value='-1' style='color:#f56954;'>Eliminar</option>");
				
				$(this).html( clone.outerHTML );
				if ( !$("#preview-label").find('#button-ready-edition').length )
				{

					$("#preview-label").append(
						_.template( $("#formula-edition-ready").html() )({
							'id': 'button-ready-edition'
						})
					)					
				}
			}
		});

		$(document).on('click', '#button-ready-edition', function(){
			$(".formula-container").children().each(function(){
				var e = $(this).find('select');
				if ( e.length && $(e).val() != -1 )
				{	
					$(this).attr('id',$(this).find('select option:selected').val() );
					$(this).attr('value', $(this).find('select option:selected').text());
					$(this).html('<b>'+$(this).find('select option:selected').text()+'</b>');
				}else if($(e).val() == -1){
					$(this).html('<b></b>');
					$(this).remove();					
				}
			});
			$('#button-ready-edition').remove();
			$(".add-formula").attr('disabled',false);
		});

		$(document).keypress(function(e) {
		    if(e.which == 13){  	
		    	if (is_modal_up === 'basic-data')f1() && $("#modal-agregar-elemento").modal("hide");
		    	if (is_modal_up === 'documental-req')f2() && $("#modal-agregar-elemento").modal("hide");
		    }
		});

		$(document).on("keypress", 'form', function (e) {
		    var code = e.keyCode || e.which;
		    if (code == 13) {
		        e.preventDefault();
		        return false;
		    }
		});

		$("#modal-agregar-elemento").on('hide.bs.modal', function (e) {			
			is_modal_up = "";
		});

		$("#modal-agregar-elemento").on('show.bs.modal', function (e) {});

		$(document).on('ifChecked', 'input', function(event){
			var local_type, local_subtype, metype, subtype, me = this;

			if( $(me).hasClass('zone-selector')){
				metype = $(this).parents(".panel").attr("type");
				subtype = $(this).parents(".panel").attr("typeaf");

				$(".zone-selector").each(function(){
					local_type = $(this).parents(".panel").attr("type");
					local_subtype = $(this).parents(".panel").attr("typeaf");

					if (this != me && ( local_type != metype || ( local_type == metype && subtype != local_subtype)))
					{					
						$(this).iCheck('uncheck');
						$(this).iCheck('disable');
						$(this).iCheck('update');
					}
				});
				$('.choosen-one').each(function(){
					$(this).removeClass('choosen-one');
				});
				$(me).addClass('choosen-one');
			}
		});

		$(document).on('ifUnchecked', '.choosen-one', function(){
			$(".zone-selector").each(function(){
				$(this).iCheck('enable');
				$(this).iCheck('uncheck');
			});
			$(this).removeClass('choosen-one');
		});

		$(document).on('ifChecked', '#suministrado-dbasic', function(){
			$(".valor-dbasic-container").hide();
		});

		$(document).on('ifUnchecked', '#suministrado-dbasic', function(){
			$("#valor-dbasic").val('');
			$(".valor-dbasic-container").show();
		});

		$(document).on('change', '.suministrado-select', function(){
			if( $(this).val() == 'Si' )
			{
				$(this).parent().attr(
					"bckp-valores",
					$(this).parent().next().find("#valor-especifico-categoria-eye").attr("data-value-per-categorie")
				);
				$(this).parent().next().html("N/A");
			}else if(  $(this).val() == 'No' ){
				var me = this;
				var categories = parseInt($("#tipo-prestador option:selected").attr("pstcategorie"));
				var valor = $(this).parent().attr("bckp-valores")!=undefined ? $(this).parent().attr("bckp-valores"): new Array(categories+1).join('0').split('').map(parseFloat);
				
				$(this).parent().next().html(
					_.template(
						'<a \
						  data-original-title="Valores_por_categoria" \
						  class="btn btn-info btn-flat valore-button" \
						  sufix="dato-especifico" \
						  title="Editar" \
						  data-toggle="tooltip" id="valor-especifico-categoria-eye"\
						  data-value-per-categorie = "<%= valor %>"\
						><i class="fa fa-eye icon-white"></i></a>'
					)({
						"valor": valor
					})
				);
			}
		});
		
		$(document).on('click', '#valor-especifico-categoria-eye', function(){			
			var button = this;
			var editable = $(this).parent().next().find("a.editar-button").attr("state") == "editing";
			var values_per_categorie = $(button).attr("data-value-per-categorie");
			
			$("#modal-valores-por-categoria-body").html(
				_.template($("#valor-por-categoria").html())({
					"categories": parseInt($("#tipo-prestador").find("option:selected").attr("pstcategorie")),
					"values": values_per_categorie.split(","),
					"extra_class": "-editing",
					"editable": editable,
					"icon": $("#tipo-prestador").find("option:selected").attr("icon")
				})
			);
			$("#modal-valores-por-categoria").modal("show");

			$(".modal-valores-por-categoria-ok").click(function(e){
				e.preventDefault();
				
				var valor = [];
				
				$(".valor-categoria-editing").each(function(){
					valor.push(
				   		$(this).val() != '' && $(this).val() != '-' ? parseFloat($(this).val()) : 'N/A'
					);
				});
				
				$(button).attr(
					"data-value-per-categorie", valor
				);

				var id = parseInt($($(button).parent().next().children('a')[0]).attr('id'));
				console.log("ID "+id+" VALOR "+valor );
				editElement("specific-values-cookie", id, {'valor': valor} , 'edited');

				$("#modal-valores-por-categoria").modal("hide");
			});
		});

		$(document).on("click", ".button-shrink", function(){
			if( $(this).hasClass("plus") ){
				$(this).html("<i class='fa fa-minus'></i>");
				$(this).removeClass("plus");
				$(this).addClass("minus");			
				$(this).parents(".panel-heading").siblings(".panel-body").show();			
			}else if($(this).hasClass("minus")){
				$(this).html("<i class='fa fa-plus'></i>");
				$(this).removeClass("minus");
				$(this).addClass("plus");
				$(this).parents(".panel-heading").siblings(".panel-body").hide();			
			}
		});

		onChangeMainconfig = function(version_state){
			currentCounter = parseInt($('#basic-config').attr('added-elements'))+1 ;
			
			if ( $('#nombre-tabulador').val() !== '' && parseInt($('#tipo-prestador').val()) !== -1 ){
			
				$('.hiden-tab').each(function(){
					$(this).removeClass('hiden-tab');
					$(this).css('display','');
				});
				
				appendValue(
					'main-config-cookie', 
					{
						'id': currentCounter,
						'name': $('#nombre-tabulador').val() ,
						'type': $('#tipo-prestador').val(),
						'state': 'edited',
						'version_actual': version_state !== undefined && version_state
					},
					undefined
				);

				appendValue(
					'basic-req', 
					{
						'id': currentCounter,
						'name': $('#nombre-tabulador').val() , 
						'type': 'T', 
						'state': 'edited',
						'content': '',
						'children': []
					},
					undefined
				);

				appendValue(
					'specific-req', 
					{
						'id': currentCounter,
						'name': $('#nombre-tabulador').val() , 
						'type': 'T', 
						'state': 'edited',
						'content': '',
						'children': []
					},
					undefined
				);
			}
		}

		$(document).on("change","#nombre-tabulador, #tipo-prestador", function(){onChangeMainconfig(false)});
		$(document).on('ifChecked', '#id_version_actual', function(){onChangeMainconfig(true)});
		$(document).on('ifUnchecked', '#id_version_actual', function(){onChangeMainconfig(false)});


		loadTabulatorAlternatives = function(p, s){
			$.ajax({
				type: "post",
				url: "/categorizacion/administrador/paginar/tabulador",
				data:{
					'p': p,
					's': s,
					csrfmiddlewaretoken: token
				},
				success: function(server_data){
					var data = server_data.data.modelo;
					var thcreated = false;
					var listvals = undefined;

					$("#pager_elements_container").attr('page', server_data.data.pagina);

					$("#table_choose_head").html('<th>No hay recursos para mostrar</th>');
					$("#cuerpo_tabla_choose").html('');
					for(var i=0;i<data.length;++i)
					{
						listvals = [];

						if(!thcreated){$("#table_choose_head").html('');}
						$.each(data[i], function(key){
							if (key!= 'url' && key != 'version_actual' && key!='elements_keys')
							{
								if(!thcreated && key!= 'id'){
									$("#table_choose_head").append('<th >'+key.replace(/^[a-z]/, function(m){ return m.toUpperCase() }) +'</th>')
								}
								listvals.push(data[i][key]);
							}
						});

						$("#cuerpo_tabla_choose").append(
							_.template($("#row_tabulador_template").html())(
								{
									'id': listvals[0],
									'nombre': listvals[1],
									'tipo_pst': listvals[2],
									'fecha': listvals[3],
									'numero_version': listvals[4],
									'label_class': data[i].version_actual?'success':'default'
								}
							)
						);
						thcreated = true;
					}
					
					$("table tbody tr").css("background-color","initial");

					if(server_data.data.num_pag == server_data.data.pagina+1)
					{
						$(".btn-next-tabulador").css("visibility","hidden");
					}else{
						$(".btn-next-tabulador").css("visibility","");
					}

					if(server_data.data.pagina == 0)
					{
						$(".btn-prev-tabulador").css("visibility","hidden");
					}else{
						$(".btn-prev-tabulador").css("visibility","");
					}
				},
				complete: function (server_data) {
					$("#modal-create-choose .modal-body #tabulator_alternatives_panel").hide();
					$("#modal-create-choose .modal-body #tabs_display_zone").show();
				},
				error: function(e){
					console.log(e);
				}
			});
		}

		$(document).on("click", "#based_on_pick", function(){
			$("#pager_elements_container").attr("page", -1);
			loadTabulatorAlternatives(-1,'+');
			$(".volver_choose_button").attr("preventhref", "true");
		});

		$(document).on("click", ".btn-prev-tabulador", function(){
			loadTabulatorAlternatives(parseInt($("#pager_elements_container").attr("page")),'-');
		});

		$(document).on("click", ".btn-next-tabulador", function(){
			loadTabulatorAlternatives(parseInt($("#pager_elements_container").attr("page")),'+');
		});

		$(document).on("click", ".volver_choose_button", function(e){
			if($(this).attr("preventhref") == "true"){	
				e.preventDefault();
				e.stopImmediatePropagation();
				$(this).attr("preventhref", "false");
				$("#modal-create-choose .modal-body #tabs_display_zone").hide();
				$("#modal-create-choose .modal-body #tabulator_alternatives_panel").show();
			}
		});

		$(document).on("click", ".row_alternative_clone", function(){
			window.location = $(this).attr("href");
		});

	}else{
		$("#notificacion #notificacion-Label").html("Problemas encontrados con su navegador");
		$("#notificacion #notificacion-body").html("<h4>Su navegador no posee soporte para almacenamiento local (localStorage) por lo que se sugiere hacer uso de una versi&oacute;n m&aacute;s actual que posea esta caracter&iacute;stica.</h4>");
	    
	    $('#notificacion-footer').html('<div class="col-xs-12">\
        	<a class="col-xs-12 btn btn-primary btn-flat" data-dismiss="modal">Aceptar</a>\
        </div>');

	    $('#notificacion').modal();
	}
})();




