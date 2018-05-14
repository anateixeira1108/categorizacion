/* constructor.js */

/*
|
|	Modulo de reconstrucción de tabuldaores (v.1.0)
|
|	JQuery Implemetation
|
*/

(function(){


	var dummyElement =  undefined;

	resetDummy = function(){ dummyElement = document.createElement('div');}

	String.prototype.repeat = function( num )
	{
	    return new Array( num + 1 ).join( this );
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
	            if( cached_this.id == id  && cached_this.type == type )
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

	    cached_this.load = function(obj, pid, ptype){

	        if(cached_this.id === undefined)
	        {  
	        	var entity = obj;
	            cached_this.id = entity.id ;
	            cached_this.type = entity.type;
	            cached_this.name = entity.name;
	            cached_this.state = entity.state;
	            cached_this.extra = entity.extra;
	            cached_this.parent = entity.parent;

	        }else if( obj!==undefined && cached_this.getElementByIdType(obj.id, obj.type) === undefined){
	        	cached_this.addChildByIndex(pid, ptype, new Tree(
		        		obj.id,
		        		obj.name, 
		        		obj.content, 
		        		obj.state, 
		        		obj.type, 
		        		obj.extra
	        		)
	        	)
	        }
	        for (var i = 0; obj!==undefined && obj.children !==undefined && i < obj.children.length; ++i){
	        	cached_this.load(obj.children[i], obj.id, obj.type);
	        }
	    }

        cached_this.loadUpdater = function(obj, pid, ptype, uids, old_ids, parent_id){
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
                }

                cached_this.name = entity.name;
                cached_this.state = entity.state;
                cached_this.extra = entity.extra;
                if(old_ids !=undefined){
                	cached_this.state="done";
                }          
                cached_this.loadUpdater(entity.children, cached_this.id, cached_this.type,undefined,old_ids);
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
    	            				
    	            				
    	            				
    	            				
    	            				if (old_ids[f].type == "AF"){
    	            					$.each($('#'+old_ids[f].pid+'.panel_af'),function(){
    	            						if($(this).attr('changed') == undefined){
    	            							$(this).attr('changed','changed');
    	            							$(this).attr('id',old_ids[f].nid);
    	            							$(this).find($('[id='+old_ids[f].pid+'][type_delete=AF]')).attr('id',old_ids[f].nid);
    	            						}
    	            					});
    	            				}else if(old_ids[f].type == "S"){
    	            					$.each($('#'+old_ids[f].pid+'.panel_sec'),function(){
    	            						if($(this).attr('changed') == undefined){
    	            							$(this).attr('changed','changed');
    	            							$(this).attr('id',old_ids[f].nid);
    	            							$(this).find($('[id='+old_ids[f].pid+'][type_delete=S]')).attr('id',old_ids[f].nid);
    	            						}
    	            					});
    	            				}else if(old_ids[f].type == "SS"){
    	            					$.each($('#'+old_ids[f].pid+'.panel_subsec'),function(){
    	            						if($(this).attr('changed') == undefined){
    	            							$(this).attr('changed','changed');
    	            							$(this).attr('id',old_ids[f].nid);
    	            							$(this).find($('[id='+old_ids[f].pid+'][type_delete=SS]')).attr('id',old_ids[f].nid);
    	            						}
    	            					});
    	            				}

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
    	            		cached_this.loadUpdater( obj[i].children, obj[i].id, obj[i].type, undefined, old_ids, parent_id);
    	            	}else{
    	            		cached_this.loadUpdater( obj[i].children, obj[i].id, obj[i].type);	
    	            	}
                	}                   
                }
            }
        }

	    cached_this.conditionalTree = function(obj, id, type, posneg, counter, tabcurrent, conditionfirst){
    		if(obj.extra.subtype == "C"){
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
    				aux = "Condición Positiva"
    			}else if(posneg=="N"){
    				aux = "Condición Negativa"
    			}

	    		$("[id="+id+"][type="+type+"] .panel-body").eq(0).append(
					_.template($("#subseccion-conditional-template").html())({
						"condicion":aux ,
						"name": obj.name,
						"id": obj.id,
						"body": options
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
    			if( cached_this.id == id && cached_this.type == type && id!=-1)
    			{
    				if (update != undefined && update == true)
    				{
    					// Perform update operation in case of being requested
						$.each(uobj, function(k,v){
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
	}

	renderDocumentales = function(tree){

		resetDummy();
		$(dummyElement).html($("#documentals-section-template").html());
		$(dummyElement).find("#form_id #id_tipo_documento").css("display","none");
		var clone_select_docstypes = $(dummyElement).find("#form_id #id_tipo_documento")[0].outerHTML;

		for(var i =0;i< tree.length; ++i)
		{
			$(clone_select_docstypes).val(tree[i].id);
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
					"name": tree[i].name,
					"id": tree[i].id,
					"typedoctext":tree[i].extra.texttype,
					"select_types_hiden": clone_select_docstypes,
					"typedoc": tree[i].type
				})
			);			
		}
		if(tree.length > 0)
		{
			$('.table-documental-req').siblings().hide();
			$('.table-documental-req').show();
		}
	}

	renderEspecificos = function(tree){

		for(var i =0; i< tree.length;++i)
		{
			$('.basic-data-body').append(
				_.template($("#valores-especificos-categoria").html() )({
					"name": tree[i].name,
					"id": tree[i].id,
					"suministrado": tree[i].suministrado,
					"suministrado_bool": tree[i].suministrado === "Si"? true:false,
					"valor": tree[i].valor.length ? tree[i].valor : 'N/A',
					"extra_class":''
				})
			);			
		}
		if(tree.length > 0)
		{
			$('.table-basic-data').siblings().hide();
			$('.table-basic-data').show();			
		}
	}
	renderComplex = function(tree, pid, ptype, local_identifier){
		var element_id = parent_counter = undefined;
		var condicion = "";

		if(tree.type == 'AF'){
			$("."+local_identifier+"-alert").hide();
			var af_counter = $("."+local_identifier+"-body .panel[type=AF]").length+1;

			$("."+local_identifier+"-body").append(
				_.template(
					$("#fundamental-aspect-template").html()
				)({
					"id": tree.id,
					"name": tree.name,
					"percent": tree.extra.percent,
					"tipo_aspecto": tree.extra.tipo_aspecto,
					"color": tree.extra.tipo_aspecto_text.toLowerCase() == 'm'?"#E6EFF8":"#e2e2e2",
					"counter": af_counter
				})
			);
		}else if(tree.type == "S"){

			element_id = $("."+local_identifier+"-body .panel[id="+pid+"][type="+ptype+"] .panel[type=S]").length+1;
			parent_counter = $("[id="+pid+"][type="+ptype+"]").attr("element_fisical_idenfitier");

			$("[id="+pid+"][type="+ptype+"] .panel-body").eq(0).append(
				_.template( $("#section-template").html() )({
					"name": tree.name,
					"id": tree.id,
					"parent_counter": parent_counter,
					"counter": element_id
				})
			);
		}else if(tree.type == "SS"){
			if(tree.extra.subtype == "D" || tree.extra.subtype == "E"){
				if(tree.content.condicion == true)
				{	
					condicion = "Condic&oacute;n Positiva";
				}else if(tree.content.condicion == false){
					condicion = "Condic&oacute;n Negativa";
				}

				// En caso de subsecciones del subtipo Dual
				array = _.zip(tree.content.options, tree.content.options_val);
				array = _.flatten(array);
				element_id = $("."+local_identifier+"-body .panel[id="+pid+"][type="+ptype+"] .panel[type=SS]").length+1;
				parent_counter = $("[id="+pid+"][type="+ptype+"]").attr("element_fisical_idenfitier");

				$("[id="+pid+"][type="+ptype+"] .panel-body").eq(0).append(
					_.template( $("#subseccion-template").html() )({
						"condicion": condicion,
						"name": tree.name,
						"id": tree.id,
						"body": array,
						"tipo": tree.extra.subtype,
						"parent_counter": parent_counter,
						"counter": element_id,
						"identifier": _.uniqueId("radio")
					})
				);
			}else if(tree.extra.subtype == "F"){
				if(tree.content.condicion == true)
				{	
					condicion = "Condic&oacute;n Positiva";
				}else if(tree.content.condicion == false){
					condicion = "Condic&oacute;n Negativa";
				}

				var strformula = "";
				for(var m = 0; m<tree.content["formula-elements"].length;++m)
				{
					strformula += tree.content["formula-elements"][m].name;
				}

				// En caso de subseccion del subtipo Formula
				element_id = $("."+local_identifier+"-body .panel[id="+pid+"][type="+ptype+"] .panel[type=SS]").length+1;
				parent_counter = $("[id="+pid+"][type="+ptype+"]").attr("element_fisical_idenfitier");

				$("[id="+pid+"][type="+ptype+"] .panel-body").eq(0).append(
					_.template( $("#subseccion-formula-template").html() )({
						"condicion": condicion,
						"enunciado": tree.name,
						"id": tree.id,
						'strformula': strformula,
						"parent_counter": parent_counter,
						"counter": element_id
					})
				);
			}else if(tree.extra.subtype == "REP"){
				// En caso de subsecciones del subtipo Repetitiva
				if(tree.content.condicion == true)
				{	
					condicion = "Condic&oacute;n Positiva";
				}else if(tree.content.condicion == false){
					condicion = "Condic&oacute;n Negativa";
				}

				icon = "<i class='text-red fa "+$("#tipo-prestador option:selected").attr("icon")+"'></i>";
				repetition = []

				for(var m =1; m<tree.content.repetition.length+1; ++m)
				{
					repetition.push(icon.repeat(m));
					repetition.push(tree.content.repetition[m-1]);
				}

				element_id = $("."+local_identifier+"-body .panel[id="+pid+"][type="+ptype+"] .panel[type=SS]").length+1;
				parent_counter = $("[id="+pid+"][type="+ptype+"]").attr("element_fisical_idenfitier");

				$("[id="+pid+"][type="+ptype+"] .panel-body").eq(0).append(
					_.template( $("#subseccion-repetitive-template").html() )({
						"condicion": condicion,
						"name": tree.name,
						"id": tree.id,
						"parent_counter": parent_counter,
						"counter": element_id,
						"ul_body": _.template($("#repetitive-relevance-ul").html())({
							"categorias": repetition
						})
					})
				);
			}else if(tree.extra.subtype == "R"){
				// En caso de subsecciones del tipo Rango
				if(tree.content.condicion == true)
				{	
					condicion = "Condic&oacute;n Positiva";
				}else if(tree.content.condicion == false){
					condicion = "Condic&oacute;n Negativa";
				}

				element_id = $("."+local_identifier+"-body .panel[id="+pid+"][type="+ptype+"] .panel[type=SS]").length+1;
				parent_counter = $("[id="+pid+"][type="+ptype+"]").attr("element_fisical_idenfitier");

				$("[id="+pid+"][type="+ptype+"] .panel-body").eq(0).append(
					_.template( $("#subseccion-rango-template").html() )({
						"condicion": condicion,
						"name": tree.name,
						"id": tree.id,
						"placeholder": tree.content.unit_representation,
						"tipo": 'R',
						"parent_counter": parent_counter,
						"counter": element_id
					})
				);

			}else if(tree.extra.subtype == "C"){
				// En caso de subsecciones del tipo Condicional
				var condicion = "";

				if(tree.content.condicion == true)
				{	
					condicion = "Condic&oacute;n Positiva";
				}else if(tree.content.condicion == false){
					condicion = "Condic&oacute;n Negativa";
				}

				element_id = $("."+local_identifier+"-body .panel[id="+pid+"][type="+ptype+"] .panel[type=SS]").length+1;
				parent_counter = $("[id="+pid+"][type="+ptype+"]").attr("element_fisical_idenfitier");

				$("[id="+pid+"][type="+ptype+"] .panel-body").eq(0).append(
					_.template($("#subseccion-conditional-template").html())({
						"condicion": condicion,
						"name": tree.name,
						"id": tree.id,
						"body": [],	
						"parent_counter": parent_counter,					
						"counter": element_id
					})
				);
			}
		}

		for(var i =0; tree!== undefined && tree.children !== undefined && i< tree.children.length; ++i)
		{
			renderComplex(tree.children[i], tree.id, tree.type, local_identifier);
		}

		$('input').iCheck({
		    checkboxClass: 'icheckbox_minimal',
		    radioClass: 'iradio_minimal',
		    increaseArea: '20%'
		});
	}

	reconstructCookies = function(version, br, sr){
		
		var current_json = [];
		current_json = JSON.parse(localStorage.getItem("main-config-cookie"));

		// Reconstruir datos de configuracion basica para estructura inicial de arbol
		$('#nombre-tabulador').val(current_json[0].name);
		$('#tipo-prestador').val(current_json[0].type);
		if(current_json[0].version_actual || version===0) 
		{
			$('#tipo-prestador').parent("div").after($("#checkbox_version").html());
			$("input[type=checkbox]").iCheck({
				checkboxClass: 'icheckbox_minimal',	
				radioClass: 'iradio_minimal',
				increaseArea: '20%'
			});
		}

		// Reconstruir requisitos basicos
		appendValue(
			'basic-req', 
			{
				'id': current_json[0].id,
				'name': current_json[0].name, 
				'type': 'T', 
				'state': 'done',
				'content': '',
				'children': []
			},
			undefined
		);
		var tree = new Tree();
		tree.load( JSON.parse(localStorage.getItem("basic-req"))[0] );
		for (var i =0; i<br.length;++i){
			tree.load(br[i], current_json[0].id, "T");
		}
		localStorage.setItem("basic-req", JSON.stringify([tree.render(false)]));

		// Reconstruir requisitos especificos
		appendValue(
			'specific-req', 
			{
				'id': current_json[0].id,
				'name': current_json[0].name, 
				'type': 'T', 
				'state': 'done',
				'content': '',
				'children': []
			},
			undefined
		);
		var tree = new Tree();
		tree.load( JSON.parse(localStorage.getItem("specific-req"))[0] );
		for (var i =0; i<sr.length;++i){
			tree.load(sr[i], current_json[0].id, "T");
		}
		localStorage.setItem("specific-req", JSON.stringify([tree.render(false)]));		
	}

	getValue = function( cname ){		
		return   JSON.parse(localStorage.getItem(cname));
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
		var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
		
		if( isDataLoaded() )
		{
			var mcc = getValue('main-config-cookie').length > 0 && isDataEdited('main-config-cookie');
			var dqc = getValue('documental-req-cookie').length > 0 && isDataEdited( 'documental-req-cookie' );
			var svc = getValue('specific-values-cookie').length > 0 && isDataEdited('specific-values-cookie');
			var data_temp = {
					'tabulador': JSON.parse(localStorage.getItem("main-config-cookie"))[0].id,
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

			$(".fixed-spinner").fadeIn('slow');
			$.ajax({
				type: "POST",
				url: "/categorizacion/administrador/tabulador/agregar/",
				async:false,
				data:data_temp,
				success: function(server_data){
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
						treeaux.loadUpdater(JSON.parse(localStorage.getItem('specific-req')), undefined, undefined, undefined, server_data.data.elementos_req_specific);
						localStorage.setItem('specific-req', JSON.stringify( [treeaux.render(false)] ) );
					}


					if(server_data.data.hasOwnProperty('elementos_req_basic')){
						var treeaux = new Tree();
						treeaux.loadUpdater(JSON.parse(localStorage.getItem('basic-req')), undefined, undefined, undefined, server_data.data.elementos_req_basic);
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

	reconstruct = function(){
		var id_tabulador = $("#constructor_core").data("tabulador");
		var operacion = $("#constructor_core").data("clone");
		var version = 1;
		var br = undefined;
		var sr = undefined;
		var current_json = undefined;

		$.ajax({
			type: "GET",
			url: "/categorizacion/administrador/tabulador/"+id_tabulador+"/reconstruir/",
			data:{
				"clonado": operacion !== undefined
			},
			success: function(server_data){
				
				version = server_data.version;				
				
				localStorage.setItem('main-config-cookie', JSON.stringify(server_data.main_config_cookie));
				localStorage.setItem('documental-req-cookie',JSON.stringify(server_data.documental_req_cookie));
				localStorage.setItem('specific-values-cookie',JSON.stringify(server_data.specific_value_cookie));
				br = server_data.basic_req;
				sr = server_data.specific_req;

				// Colocar valores del servidor en almacenamiento local del cliente
				reconstructCookies(version, br, sr);

				// Si la operacion es colocada, quiere decir que se esta realizando una operacion
				// de clonado por lo que es necesario reiniciar los datos de almacenamiento local
				if(operacion!==undefined){
					autosave();			
				}

				// Renderizar requisitos documentales
				current_json = JSON.parse(localStorage.getItem("documental-req-cookie"));
				renderDocumentales(current_json);

				// Renderizar valores especificos
				current_json = JSON.parse(localStorage.getItem("specific-values-cookie"));
				renderEspecificos(current_json);

				// Renderizar requisitos basicos
				current_json = JSON.parse(localStorage.getItem("basic-req"))[0];
				renderComplex(current_json, undefined, undefined, "basic-req");

				// Renderizar requisitos especificos
				current_json = JSON.parse(localStorage.getItem("specific-req"))[0];
				renderComplex(current_json, undefined, undefined, "specific-req");
			},
			error: function(e){
				console.log(e);
			}
		});
	}

	reconstruct();
})();

