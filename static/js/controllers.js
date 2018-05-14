'use strict';

coreApp.controller('MunicipiosParroquiasCtrl',
	[
        '$scope',
        '$element', 
        '$http', 
        '$log', 
        '$cookies', 
        '$timeout', 
        'sharedService', 
        '$window', 
        function($scope, $element, $http, $log, $cookies, $timeout, sharedService, $window) {


	$scope.alerta = {mostrar: false, texto: "", htmlclass: "" };
    $scope.sucursal = {mostrar: false, texto: "", htmlclass: "" };

    $scope.$watch('estados', function() {
        if ($scope.estados != undefined  && $scope.estados != ""){
            $scope.parroquiasList = [];
    		var url = "/municipios/"+$scope.estados;
        	$scope.search(url, "municipio");
    	}

    });

    $scope.$watch('municipio', function() {
        if ( $scope.municipio != undefined && $scope.municipio != "" ){
    		var url = "/parroquias/"+$scope.municipio.id;
        	$scope.search(url, "parroquia");
    	}
    });

    $scope.$watch('parroquia', function() {
        angular.element('#id_parroquia').val($scope.parroquia)
    });

    $scope.search = function(url, type) {
    	$http({
          url: url,
          method: "GET",
          dataType: "json",
      	}).success(function (response, status) {
      		if (response.success = true){
      			if(type == "municipio"){
                    $scope.municipiosList = response.municipios;
                    angular.element('#id_municipio').val($scope.estados)
                }
      			if(type == "parroquia"){
                    $scope.parroquiasList = response.parroquias;
                    angular.element('#id_parroquia').val($scope.parroquias)
                }
                $scope.change=false;

            }else{ $log.error(response.error); }
      	}).error(function (response, status){
        	   $log.error("Error Status code:"+status+", al obtener la lista de valores");
      	});
   	};

   	$scope.deleteItem = function(sucursalId){
    	var token = $cookies['csrftoken'];
        var htclass; var sec;
        $http({
          url: "../../eliminar_sucursal",
          method: "POST",
          dataType: "json",
          data: {id: sucursalId, csrfmiddlewaretoken: token },
        }).success(function (response, status) {
            if (response.success == true){
                $scope.removeItem(sucursalId);
                htclass = "alert-success";
                sec = 1;
            }else{
                htclass = "alert-danger";
                sec = 0;
            }
            $scope.sucursal = {mostrar: true, texto: response.message, htmlclass: htclass, seconds: sec };

        }).error(function (response, status){
               $log.error("Error Status code:"+status+", al obtener la lista de valores");
        });
    };

    $scope.removeItem = function(id){
        angular.element("#branch-office-"+id).remove();
    };

    $scope.informar = function(mostrar, texto, htmlclass, seconds){
        $scope.alerta.texto = texto;
        $scope.alerta.htmlclass = htmlclass;
        $scope.alerta.mostrar = mostrar;
        if ((mostrar) && (seconds != 0)){
            $timeout(function() {
                $scope.alerta.mostrar = false;
            }, seconds * 1000);
        }
    };

    $scope.$on('broadcastHandler', function(event, data, type) {
        if(type == "sucursales"){
            $scope.informar(data.mostrar, data.mensaje, data.class_alert, data.segundos);
            if (data.exito == true){
                $scope.reloadRoute();
            }
        }
    });

    $scope.informar = function(mostrar, texto, htmlclass, seconds){
        $scope.alerta.texto = texto;
        $scope.alerta.htmlclass = htmlclass;
        $scope.alerta.mostrar = mostrar;
        if ((mostrar) && (seconds != 0)){
            $timeout(function() {
                $scope.alerta.mostrar = false;
            }, seconds * 1000);
        }
    };

    $scope.reloadRoute = function() {
        var seconds = 1;
        $timeout(function() {
            $window.location.reload();
        }, seconds * 1000);
    };

}]);

coreApp.controller('RegistrarSucursalCtrl',
	['$scope', '$http', '$log', '$window', '$timeout', '$rootScope', 'sharedService', function($scope, $http, $log, $window, $timeout, $rootScope,sharedService ) {

    $scope.alerta = {mostrar: false, texto: "", htmlclass: "" };
	$scope.patternPostal = $rootScope.patterns['postal'];
    $scope.$watch('sucursalEstado', function() {
        if ($scope.sucursalEstado != undefined  && $scope.sucursalEstado != ""){
    		var url = "/municipios/"+$scope.sucursalEstado;
        	$scope.search(url, "municipio");
    	}
    });

    $scope.$watch('sucursalMunicipio', function() {
        if ($scope.sucursalMunicipio != undefined && $scope.sucursalMunicipio != "" ){
    		var url = "/parroquias/"+$scope.sucursalMunicipio.id;
        	$scope.search(url, "parroquia");
    	}
    });

    $scope.search = function(url, type) {
    	$http({
          url: url,
          method: "GET",
          dataType: "json",
      	}).success(function (response, status) {
      		if (response.success = true){
      			if(type == "municipio"){ $scope.municipiosList = response.municipios; }
      			if(type == "parroquia"){ $scope.parroquiasList = response.parroquias; }
                $scope.change = false;
            }else{ $log.error(response.error); }
      	}).error(function (response, status){
        	   $log.error("Error Status code:"+status+", al obtener la lista de valores");
      	});
   	};

   	$scope.validate = function(form, event){
   		event.preventDefault();
      	$scope.submitted = true;
      	if (form.$invalid) {
	          return;
	    }
	    $scope.guardarSucursal()
    };

    $scope.guardarSucursal = function(){
    	var form = angular.element("[name='formSucursales']");
        var res = {}
    	$http({
          url: form.attr('action'),
          method: "POST",
          dataType: "json",
          data: form.serialize()
	    }).success(function (response, status) {
	    	if (response.success == true){
	    		angular.element('#sucursales-modal').modal('hide');
                res = {mostrar: true, class_alert: "alert-success", segundos: 0, mensaje: response.message, exito:true}
	    	}else{
                res = {mostrar: true, class_alert: "alert-danger", segundos: 0, mensaje: response.message, exito:false}
            }
            sharedService.broadcast(res, "sucursales");

	    }).error(function (response, status){
	        $log.error("error"+response);
	    });
    };

    $scope.reloadRoute = function() {
        var seconds = 1;
        $timeout(function() {
            $window.location.reload();
        }, seconds * 1000);
    };

    $scope.informar = function(mostrar, texto, htmlclass, seconds){
        $scope.alerta.texto = texto;
        $scope.alerta.htmlclass = htmlclass;
        $scope.alerta.mostrar = mostrar;
        if ((mostrar) && (seconds != 0)){
            $timeout(function() {
                $scope.alerta.mostrar = false;
            }, seconds * 1000);
        }
    };

}]);

coreApp.controller('modificacionActaCtrl',
    ['$scope', '$element', '$http', '$log','$timeout', '$window', '$cookies', 'safeApply', function($scope, $element, $http, $log, $timeout, $window, $cookies, safeApply) {
    $scope.alerta = {mostrar: false, texto: "", htmlclass: "" };
    $scope.tipoModificacionesList=[
        { name: 'Junta Directiva', id: 1 },
        { name: 'Objetivo Social', id: 2 },
        { name: 'Domicilio Fiscal', id: 3 },
        { name: 'Acciones', id: 4 },
        { name: 'Capital', id: 5 },
        { name: 'Otros', id: 6 }
    ];

    $scope.file_constitutiva = false;

    $scope.startUploading = function() {
        $log.info('Cargando Archivo....');
    };

    angular.element('#modificacion-acta').on('hidden.bs.modal', function() {
      $(this).find('[name=_archivo_acta_constitutiva]').val('');
    });

    $scope.is_valid_path = function(fpath) {
        if (fpath !== undefined) {
            return (fpath.search(/^(?:[0-9a-fA-F]{4}[\/\\]){10}/) == 0);
        }
        return false;
    };

    $scope.validate = function(form){
      $scope.submitted = true;
      if (form.$invalid) {
          return;
      }
      angular.element("[name='formModificacionActa']").submit();
      return true;
    };

    $scope.uploadComplete = function (response) {
        if (response.success == true){
            $scope.informar(true, response.message, "alert-success", 1);
            angular.element('#modificacion-acta').modal('hide');
            $scope.reloadRoute();
        }else{
            $scope.informar(true, response.message, "alert-danger", 2);
            angular.element('#modificacion-acta').modal('hide');
        }
    }

    $scope.informar = function(mostrar, texto, htmlclass, seconds){
        $scope.alerta.texto = texto;
        $scope.alerta.htmlclass = htmlclass;
        $scope.alerta.mostrar = mostrar;
        if ((mostrar) && (seconds != 0)){
            $timeout(function() {
                $scope.alerta.mostrar = false;
            }, seconds * 1000);
        }
    };

    $scope.reloadRoute = function() {
        var seconds = 1;
        $timeout(function() {
            $window.location.reload();
        }, seconds * 1000);
    };

    $scope.deleteItem = function(actaId){
        var token = $cookies['csrftoken'];
        $http({
          url: "./../../eliminar_modificacion_acta",
          method: "post",
          dataType: "json",
          data: {id: actaId, csrfmiddlewaretoken: token },
        }).success(function (response, status) {
            if (response.success == true){
                $scope.informar(true, response.message, "alert-success", 0);
                $scope.removeItem(actaId);
            }else{
                $scope.informar(true, response.message, "alert-danger", 0);
            }
        }).error(function (response, status){
               $log.error("Error Status code:"+status+", al obtener la lista de valores");
        });
    };

    $scope.getItem = function(actaId){
        $http.get("../../obtener_acta/"+actaId).success( function( response, status){
            if (response.success == true){
                safeApply($scope, function() {
                    $scope.iniciarVariables(response.data, $scope.url_edicion);
                });

            }else{
                $scope.informar(true, response.message, "alert-danger", 0);
            }
        });
    };

    $scope.iniciarVariables = function(data, url){
        $scope.submitted = false;
        $scope.form = {
            circunscripcion: data.circuito_circunscripcion,
            mercantil: data.registro_mercantil,
            tomo: data.tomo,
            numero_tomo: data.numero_tomo,
            registro: data.fecha_registro,
            asamblea: data.fecha_ultima_asamblea,
            constitutiva: data.archivo_acta_constitutiva,
            objetivo_modificacion: {id: parseInt(data.objetivo_modificacion)},
            motivo_modificacion: data.motivo_modificacion,
            nombre_archivo: data.nombre_archivo_acta,
            pk_element: data.pk
        }
        if (data.constitutiva){
            $scope.file_constitutiva = true;
        }
        $scope.url_action = url;
        angular.element("#modificacion-acta").modal('show');
    };

    $scope.agregar_acta = function(){
        var data = {
            circuito_circunscripcion: "", registro_mercantil: "",
            tomo: "", numero_tomo: "", fecha_registro: "", pk_element: "",
            fecha_ultima_asamblea: "", archivo_acta_constitutiva: "",
            objetivo_modificacion: "", motivo_modificacion: "",
            nombre_archivo: ""
        }
        $scope.iniciarVariables(data, $scope.url_registro);
        angular.element("#modificacion-acta").modal('show');
    };

    $scope.removeItem = function(id){
        angular.element("#modificacion-"+id).remove();
    };

    $scope.$watch('fecha_registro', function() {
        var fecha = angular.element('[name="fecha_registro"]').val()
        $scope.fecha_registro = fecha;
    });

    $scope.$watch('objetivo_modificacion', function() {
        if ($scope.objetivo_modificacion){
            toogle_motivo($scope.objetivo_modificacion)
        }
    });

    function toogle_motivo(obj){
        var objMotivo = angular.element('#motivo')
        var input = angular.element('[name="_motivo_modificacion"]');
        if (obj.id == 6){
            objMotivo.show();
            input.prop('required', true);

        }else{
            objMotivo.hide();
            input.prop('required', false);
            $scope.motivoModificacion ="";
        }
    }

}]);

coreApp.controller('registroAccionistaCtrl',
    ['$scope', '$http', '$log', '$rootScope', '$timeout', '$window', '$cookies', 'safeApply', function($scope, $http, $log, $rootScope, $timeout, $window, $cookies, safeApply){
    var token = $cookies['csrftoken'];
    $scope.alerta = {mostrar: false, texto: "", htmlclass: "" };
    $scope.patternRif = $rootScope.patterns['rif'];
    $scope.patternCedula = $rootScope.patterns['cedula'];
    $scope.url_action = "";
    $scope.ACUTED_CHARACTERS = {
      'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u', 'ñ': 'n'
    };
    $scope.NOMBRES_APELLIDOS_REGEX = /^[^\W\d_]+(?:\s+[^\W\d_]+)*$/;

    $scope.escape_acute_characters = function(str) {
        $.each($scope.ACUTED_CHARACTERS, function(key, value) {
          str = str.replace(key, value);
        });
        return str;
    };

    angular.element("#add-partner").on('hidden.bs.modal', function() {
      $(this).find('[name=archivo_cedula]').val('');
      $(this).find('[name=archivo_rif]').val('');
    });

    $scope.startUploading = function() {
        $log.info('Cargando Archivo....');
    };

    $scope.validate = function(form){
        $scope.submitted = true;
        if (form.$invalid) {
             return;
        }
        angular.element("[name='formAccionista']").submit();
        return true;
    };

    $scope.validar_rif = function (){
        var url = "/validar_rif";
        if ($scope.rif != "" && $scope.rif != undefined){
            var data = {rif: $scope.rif, csrfmiddlewaretoken: token };
            $scope.http_validacion(url, data);
        }
    };

    $scope.validar_cedula = function (){
        var url = "/validar_cedula";
        if ($scope.cedula != "" && $scope.cedula != undefined){
            var data = {cedula: $scope.cedula, csrfmiddlewaretoken: token };
            $scope.http_validacion(url, data);
        }
    };

    $scope.validar_nombres = function() {
        var nombres = (angular.element('input[name=nombre]').val() || '').trim();
        $scope.invalidNombres = (
            nombres && !$scope.escape_acute_characters(nombres).match($scope.NOMBRES_APELLIDOS_REGEX)
        );

        if (nombres && $scope.invalidNombres) {
            $scope.msgNombres = 'Solo se permiten caracteres alfabéticos.';

        } else {
            $scope.msgNombres = '';
        }
    };

    $scope.validar_apellidos = function() {
        var apellidos = (angular.element('input[name=apellido]').val() || '').trim();
        $scope.invalidApellidos = (
            apellidos && !$scope.escape_acute_characters(apellidos).match($scope.NOMBRES_APELLIDOS_REGEX)
        );

        if ($scope.invalidApellidos) {
            $scope.msgApellidos = 'Solo se permiten caracteres alfabéticos.';

        } else {
            $scope.msgApellidos = '';
        }
    };

    $scope.uploadComplete = function (response) {
        if (response.success == true){
            angular.element('#add-partner').modal('hide');
            $scope.informar(true, response.message, "alert-success", 1);
            $scope.reloadRoute();
        }else{
            angular.element('#add-partner').modal('hide');
            $scope.informar(true, response.message, "alert-danger", 2);
            $log.error(response)
        }
    };

    $scope.informar = function(mostrar, texto, htmlclass, seconds){
        $scope.alerta.texto = texto;
        $scope.alerta.htmlclass = htmlclass;
        $scope.alerta.mostrar = mostrar;
        if ((mostrar) && (seconds != 0)){
            $timeout(function() {
                $scope.alerta.mostrar = false;
            }, seconds * 1000);
        }
        return;
    };

    $scope.reloadRoute = function() {
        var seconds = 1;
        $timeout(function() {
            $window.location.reload();
        }, seconds * 1000);
    };

    $scope.deleteItem = function(accionistaId){
        $http({
          url: "../../eliminar_accionista",
          method: "POST",
          dataType: "json",
          data: {id: accionistaId, csrfmiddlewaretoken: token },
        }).success(function (response, status) {
            if (response.success == true){
                $scope.informar(true, response.message, "alert-success", 0);
                $scope.removeItem(accionistaId);
            }else{
                $scope.informar(true, response.message, "alert-danger", 0);
            }
        }).error(function (response, status){
               $log.error("Error Status code:"+status+", al obtener la lista de valores");
        });
    };


    $scope.getItem = function(accionistaId){
        $http.get("../../editar_accionista/"+accionistaId).success( function( response, status){
            if (response.success == true){
                safeApply($scope, function() {
                    $scope.iniciarVariables(response.data, $scope.url_edicion);
                });

            }else{
                $scope.informar(true, response.message, "alert-danger", 0);
            }
        });
    };


    $scope.iniciarVariables = function(data, url){
        $scope.submitted = false;
        $scope.invalidNombres = false;
        $scope.pk_element = data.pk;
        $scope.rif = data.rif;
        $scope.cedula = data.cedula;
        $scope.nombre = data.nombres;
        $scope.director = data.director;
        $scope.apellido = data.apellidos;
        $scope.numero_acciones = data.numero_acciones;
        $scope.fecha_incorporacion = data.fecha_incorporacion;
        $scope.archivo_rif = data.archivo_rif;
        $scope.archivo_cedula = data.archivo_cedula;
        $scope.nombre_archivo_cedula = data.nombre_archivo_cedula;
        $scope.nombre_archivo_rif = data.nombre_archivo_rif;
        $scope.url_action = url;
        angular.element("[name='director']").iCheck('uncheck');
        if ($scope.director == true) {
            angular.element("[name='director']").iCheck('check');
        }

        angular.element("#add-partner").modal('show');
    };
    $scope.agregarAccionista = function(){
        var data = {
            pk : "", rif : "", cedula : "", nombres : "", apellidos : "",
            director : "", numero_acciones : "", fecha_incorporacion : "",
            archivo_rif : "", archivo_cedula : "",
            nombre_archivo_rif: "", nombre_archivo_cedula: ""
        }

        $scope.iniciarVariables(data, $scope.url_registro);
        angular.element("#add-partner").modal('show');
    };

    $scope.removeItem = function(id){
        angular.element("#shareholder-"+id).remove();
    };

    $scope.http_validacion = function (url, data){
        var data_response = "";
        $http({
          url: url,
          method: "POST",
          dataType: "json",
          data: data,
        }).success(function (response, status) {
            $scope.mesgValidacion(response);
        }).error(function (response, status){
            $log.error("Error Status code:"+status+", al obtener la lista de valores");
        });

    };

    $scope.mesgValidacion = function (response){
        var rif = angular.element("[name='rif']");
        var cedula = angular.element("[name='cedula']");

        if (response.success == false){
            if (response.item == "rif"){
                $scope.invalidRif = true;
                $scope.msgRif = response.message;
                rif.val('');
                rif.focus();

            }else{
                $scope.invalidCedula = true;
                $scope.msgCedula = response.message;
                cedula.val('');
                cedula.focus()
            }

        }else{
            if (response.item == "rif"){
                $scope.invalidRif = false;
                $scope.msgRif = "";
            }else{
                $scope.invalidCedula = false;
                $scope.msgCedula = "";
            }
        }
    };

    $scope.is_valid_path = function(fpath) {
        if (fpath !== undefined) {
            return (fpath.search(/^(?:[0-9a-fA-F]{4}[\/\\]){10}/) == 0);
        }
        return false;
    };

}]);

coreApp.controller('ActividadTuristicaCtrl',
    ['$scope', '$log', '$cookies', '$http', '$timeout', '$cookieStore', function($scope, $log, $cookies, $http, $timeout, $cookieStore) {
    $scope.alerta = {mostrar: false, texto: "", htmlclass: "" };

    $scope.agregar_actividad = function (){
        if(($scope.secundario === undefined || $scope.secundario=="")){
           $scope.informar(true, "La actividad es un campo requerido", "error", 3);
           return;
        }

        var data = {
            csrfmiddlewaretoken: $cookies['csrftoken'],
            actividad: $scope.secundario,
            licencia: $scope.licencia
        };
        $scope.send("/registro/agregar_actividad", data, "add");
    };

    $scope.eliminar_actividad = function (actividad){
        var data = {
            csrfmiddlewaretoken: $cookies['csrftoken'],
            actividad_id: actividad
        };
        $scope.send("/registro/eliminar_actividad", data, "delete");
    };

    $scope.send = function(url, data, action) {
        $http({
          url: url,
          method: "POST",
          dataType: "json",
          data: data,
        }).success(function (response, status) {
            if (response.success==true){
                $scope.agregar_elemento(response.data, action);
                $scope.informar(true, response.message, "success", 0);
            }else{
                $scope.informar(true, response.message, "error", 2);
            }
        }).error(function (response, status){
            $log.error("Error Status code:"+status+", al obtener la lista de valores");
        });
    };

    $scope.agregar_elemento = function(data, action){
        if(action == "add"){ $scope.secundarias.push(data); }
        if(action == "delete"){
            var indexes = $.map($scope.secundarias, function(obj, k) {
                if(obj.id == data.id) {
                    return k;
                }
            });
            $scope.secundarias.splice(indexes[0], 1)
        }
        $scope.actualizar_actividades();
    }

    $scope.actualizar_actividades = function(){
        var list_seleccionados = [];
        $scope.secundario = "";
        $scope.licencia = "";

        if ($scope.actividad_primaria){

            var primaria = _.find($scope.todas_actividades, function(obj, k){
                return obj.id == $scope.actividad_primaria.id;
            });

            list_seleccionados.push({ 
                id: primaria.id, 
                nombre: primaria.nombre, 
                group: primaria.group 
            });
        }

        _.each($scope.secundarias, function(obj, k){
            list_seleccionados.push({ 
                id: obj.actividad_id, 
                nombre: obj.nombre, 
                group: obj.group 
            });
        });
        var reject = _.filter($scope.todas_actividades, function(obj){
            return !_.findWhere(list_seleccionados, obj);
        });

      $log.info("primaria", primaria)
      $scope.actividades_comerciales = reject;
    }

    $scope.$watch('secundarias', function(){
        $scope.actualizar_actividades();
    });

    $scope.$watch('actividad_primaria', function() {
        $scope.actualizar_actividades();
    });

    $scope.informar = function(mostrar, texto, htmlclass, seconds){
        $scope.alerta.texto = texto;
        $scope.alerta.htmlclass = htmlclass;
        $scope.alerta.mostrar = mostrar;
        if ((mostrar) && (seconds != 0)){
            $timeout(function() {
                $scope.alerta.mostrar = false;
            }, seconds * 1000);
        }
    };

}]);

coreApp.controller('DeclaracionesModalCtrl',
    ['$scope', '$element', '$log', 'windowLocationOrigin', function($scope, $element, $log, windowLocationOrigin) {

    $scope.tipos_declaracion = [
        {id: 1, nombre: 'Declaración Definitiva'},
        {id: 2, nombre: 'Declaración Sustitutiva'},
    ];

    $scope.getDeclaraciones = function() {
        if (typeof $scope.periodo != 'undefined' && $scope.periodo) {
            $.ajax({
                url: windowLocationOrigin + '/declaraciones/declaraciones-periodo',
                method: 'GET',
                data: {
                  'periodo': convertir_periodo_str_date($scope.periodo).format('DD/MM/YYYY')
                }
            }).success(function(data) {
                $scope.error = data.error ? data.msg : null;

                if (!data.result || data.result.length > 0) {
                    $scope.$apply(function() {
                        $scope.tipo_declaracion = $scope.tipos_declaracion[1];
                        $scope.dummy_tipo_declaracion = $scope.tipos_declaracion[1].nombre;
                    });

                } else {
                    $scope.$apply(function() {
                        $scope.tipo_declaracion = $scope.tipos_declaracion[0];
                        $scope.dummy_tipo_declaracion = $scope.tipos_declaracion[0].nombre;
                    });
                }
            });
        }
    };

    $scope.onConfirmar = function() {
        if (!$scope.periodo) {
            alert('Debe indicar el periodo que va a declarar.');
            return;
        }

        if ($scope.error) {
            alert($scope.error);
            return;
        }

        window.location = '/declaraciones/pst/declaracion/formulario/?' + $.param({
            periodo: $scope.periodo
        });
    };

}]);

coreApp.controller('DeclaracionesCtrl',
    ['$scope', '$element', '$log', 'windowLocationOrigin', function($scope, $element, $log, windowLocationOrigin) {

    $scope.fecha_presentacion = moment().format('DD/MM/YYYY');

    $scope.init = function(periodo) {
        $scope.periodo = convertir_periodo_str_date(periodo);
        $scope.dummy_periodo = periodo;
        $scope.calcDates();
    };

    $scope.calcDates = function() {
        if (typeof $scope.periodo != 'undefined' && $scope.periodo) {
            $scope.fecha_desde = $scope.periodo.startOf('month').format('DD/MM/YYYY');
            $scope.fecha_hasta = $scope.periodo.endOf('month').format('DD/MM/YYYY');
            $scope.model_periodo = $scope.periodo.startOf('month').format('DD/MM/YYYY');
            $scope.getDeclaraciones();
        }
    };

    $scope.getDeclaraciones = function() {
        $.ajax({
            url: windowLocationOrigin + '/declaraciones/declaraciones-periodo',
            method: 'GET',
            data: {'periodo': $scope.periodo.format('DD/MM/YYYY')}
        }).success(function(data) {
            if (data.error == 0 && data.result.length > 0) {
                $scope.$apply(function() { $scope.tipo_declaracion = 2 });
            } else {
                $scope.$apply(function() { $scope.tipo_declaracion = 1 });
            }
            $('#dummy_tipo_declaracion').val(
                $('#id_tipo_declaracion option[value=' + $scope.tipo_declaracion + ']').html()
            );
        });
    };

    $scope.calcVentasTerritoriales = function() {
        $scope.total_ventas_territorial = 0;
        $scope.total_ventas_territorial += parseFloat($scope.ventas_propias) || 0;
        $scope.total_ventas_territorial += parseFloat($scope.ventas_exportacion) || 0;
        $scope.total_ventas_territorial += parseFloat($scope.ventas_internas_general) || 0;
        $scope.total_ventas_territorial += parseFloat($scope.ventas_internas_adicional) || 0;
        $scope.total_ventas_territorial += parseFloat($scope.ventas_internas_reducida) || 0;
        $scope.total_ventas_territorial = $scope.total_ventas_territorial.toFixed(2);

        $scope.calcTotalVentasMenosAnticipo();
    };

    $scope.calcTotalVentasMenosAnticipo = function() {
        $scope.total_ventas_menos_anticipo = $scope.total_ventas_territorial;
        $scope.total_ventas_menos_anticipo -= $scope.total_anticipo_declaracion || 0;

        $scope.calcCED();
    };

    $scope.calcAnticipoDeclaracion = function() {
        $.ajax({
            url: windowLocationOrigin + '/declaraciones/declaraciones-periodo',
            method: 'GET',
            data: {
                'id': $scope.anticipo_declaracion || -1
            }
        }).success(function(data) {
            $scope.$apply(function() {
                if (data.error == 0 && data.result.length > 0) {
                    $scope.total_anticipo_declaracion = data.result[0].fields.total_ventas_menos_anticipo;
                } else {
                    $scope.total_anticipo_declaracion = 0;
                }
                $scope.calcTotalVentasMenosAnticipo();
            });
        });
    };

    $scope.calcCED = function() {
        $scope.contribucion_especial_determinada = parseFloat($scope.total_ventas_menos_anticipo) || 0;
        $scope.contribucion_especial_determinada *=  0.01;
        $scope.contribucion_especial_determinada = $scope.contribucion_especial_determinada.toFixed(2);
        $scope.calcTotalPagar();
    };

    $scope.calcTotalPagar = function() {
        $scope.total_pagar = 0;
        $scope.total_pagar += parseFloat($scope.contribucion_especial_determinada) || 0;
        $scope.total_pagar -= parseFloat($scope.total_compensacion) || 0;
        $scope.total_pagar = $scope.total_pagar.toFixed(2);
    };

	$scope.choices = [{id: 'archivo-1'}];

	$scope.addNewChoice = function($event) {
	  var newItemNo = $scope.choices.length+1;
	  $scope.choices.push({'id':'archivo-'+newItemNo});
	  $event.preventDefault();
	};

	$scope.showAddChoice = function(choice) {
	  return choice.id === $scope.choices[$scope.choices.length-1].id;
	};

    function parse_value(value) {
        if (value && typeof value == 'string' && value.search(/^\d{4}-\d{2}-\d{2}.*$/) != -1) {
            return moment(value).format('DD/MM/YYYY');
        }
        return value;
    }

}]);

coreApp.controller('FirmaPersonalCtrl',
    ['$scope', '$element', '$log', '$cookies', 'windowLocationOrigin', function($scope, $element, $log, $cookies, windowLocationOrigin) {

    $scope.select_options = [
        {id: 1, desc: 'No', boolean_value: false},
        {id: 2, desc: 'Sí', boolean_value: true}
    ];

    $scope.selectInitValue = function() {
        $.ajax({
            url: windowLocationOrigin + '/registro/natural/firma_personal/tiene',
            method: 'GET'
        }).success(function(data) {
            $scope.tiene_firma_personal = data.tiene_firma_personal == false ? 1 : 2;
            $scope.$apply();
            $scope.setSelectDisplay();
        });
    };

    $scope.updateServerValue = function() {
        $.ajax({
            url: windowLocationOrigin + '/registro/natural/firma_personal/tiene',
            method: 'POST',
            data: {
                csrfmiddlewaretoken: $cookies['csrftoken'],
                tiene_firma_personal: $scope.tiene_firma_personal == 1 ? false : true
            }
        });
        $scope.setSelectDisplay();
    };

    $scope.setSelectDisplay = function() {
        var visibility = $scope.tiene_firma_personal == 1 ? 'hide' : 'show';

        $.each(angular.element("#persona-natural .row"), function(index) {
            if (index >= 2) {
                $(this)[visibility]();
            }
        });

        if (visibility == 'hide') {
            $('.footer .row button:last-of-type').attr('type', 'button');
            $('.footer .row button:last-of-type').attr(
                'onClick', 'javascript:window.location = ' + '"/registro/natural/paso/4/"'
            );
        } else {
            $('.footer .row button:last-of-type').attr('type', 'submit');
            $('.footer .row button:last-of-type').removeAttr('onClick');
        }
    };

}]);

coreApp.controller('RegistroContactoCtrl', ['$scope', '$log', function($scope, $log) {
	angular.element("#option_si  ins.iCheck-helper").bind('click', function(){
        $scope.show_hide("Si")
	});

	angular.element("#option_no  ins.iCheck-helper").bind('click', function(){
        $scope.show_hide("No")

	});

    $scope.show_hide = function(seleccion) {
 		if (seleccion == "Si"){ angular.element(".form_contacto").slideUp(); }
 		if (seleccion == "No"){ angular.element(".form_contacto").slideDown(); }
    };

    var es_representante = angular.element('input[name=optionsRadios]:checked').val();
    $scope.show_hide(es_representante)

}]);

coreApp.controller('BuscarCandidatosCtrl',
    ['$scope', '$http', '$log', '$cookies', '$rootScope', 'sharedService', function($scope, $http, $log, $cookies, $rootScope, sharedService) {

    $scope.patternRif = $rootScope.patterns['rif'];
    $scope.resultado = false;
    $scope.candidatos = [];
    $scope.estadosList = []
    $scope.alerta = {mostrar: false, texto: "", htmlclass: "" };
 
    var ele = angular.element("[name='todos']");
    ele.on('ifChecked', function(){
        angular.element("[name='candidato[]']").prop('checked', true);
    });
    ele.on('ifUnchecked', function(){
        angular.element("[name='candidato[]']").prop('checked', false);
    });

    angular.element("#periodo_desde").datepicker({
        language: "es",
        autoclose: true,
        clearBtn: 'Limpiar',
    });
    var token = $cookies['csrftoken'];

    $scope.busquedaBasica = function(){
        if ($scope.rif == "--"){ $scope.rif=""}
        var data = {rif: $scope.rif, csrfmiddlewaretoken: token, busqueda: "basica" };
        $scope.search(data);
    };

    $scope.busquedaAvanzada = function(event) {
        event.preventDefault();
        var formData = angular.element('[name="fromCandidatos"]').serializeArray();
        var data = {};
        _.each(formData, function(obj, k){
            var data_name = formData[k].name;
            var data_value = formData[k].value;
            if ((data_value !== "") && (data_value !== ".")) {
                data[data_name] = data_value;
            }
        });
        data['busqueda']='avanzada';
        $scope.search(data);
    };

    $scope.$watch('estado', function() {
        if ($scope.estado != undefined  && $scope.estado != ""){
            var url = "/municipios/"+$scope.estado.id;
            $scope.parroquiasList = [];
            $scope.buscar_ubicacion(url, "municipio");
        }

    });

    $scope.limite_fecha = function(){
        var date = $scope.periodo_desde.split("-");
        var dia = 1;
        var mes = $rootScope.MESES[_.str.chop(date[0], 3)[0]];
        var anio = date[1];
        date = _.str.sprintf("%s-%s-%s", dia, mes, anio)
        var d = moment(date, "DD-MM-YYYY").add('months', 1);
        var ele = angular.element("#periodo_hasta");
        ele.datepicker("remove");
        ele.datepicker({
            language: "es",
            autoclose: true,
            startDate: d.format("MM-YYYY"),
            clearBtn: 'Limpiar',
        });
    };

    $scope.$watch('municipio', function() {
        if ( $scope.municipio != undefined && $scope.municipio != "" ){
            var url = "/parroquias/"+$scope.municipio.id;
            $scope.buscar_ubicacion(url, "parroquia");
        }
    });


    $scope.buscar_ubicacion = function(url, type) {
        $http({
          url: url,
          method: "GET",
          dataType: "json",
        }).success(function (response, status) {
            if (response.success = true){
                if(type == "municipio"){ $scope.municipiosList = response.municipios; }
                if(type == "parroquia"){ $scope.parroquiasList = response.parroquias; }
            }else{ $log.error(response.error); }
        }).error(function (response, status){
               $log.error("Error Status code:"+status+", al obtener la lista de valores");
        });
    };


    $scope.search = function(data, url) {
        $http({
          url: "../buscar_candidatos/",
          method: "POST",
          dataType: "json",
          data: data,
        }).success(function (response, status) {
            $scope.candidatosList(response);
        }).error(function (response, status){
            $log.error("Error Status code:"+status+", al obtener la lista de valores");
        });
    };


    $scope.candidatosList = function(objects){
        $scope.alerta = {mostrar: false, texto: "", htmlclass: "" };
        $scope.candidatos = [];
        _.each(objects.data, function(obj, k){
            obj.criterio = objects.criterio;
        });
        if (objects.success == true && _.size(objects.data) > 0){
            $scope.resultado = true;
            $scope.initPagination(objects.data, 5);
            $scope.candidatos = $scope.allItems[0]; // primeros candidatos para la cantidad solicitada
        }else{
            $scope.alerta = {mostrar: true, texto: objects.message, htmlclass: "alert-danger" };
        }
    };

    $scope.submit = function(event){
        event.preventDefault();
        var data = []
        var candidatos = angular.element('[name="candidato[]"]');
        candidatos = _.filter(candidatos, function(obj, k){
            return angular.element(obj).is(':checked') == true;
        });
        if( _.size(candidatos) > 0 ){
            $scope.listarCandidatos(candidatos)
        }
    };

    $scope.listarCandidatos = function (seleccionados){
        var seleccionadoslist = [];
        _.each(seleccionados, function(elem, k){
            seleccionadoslist.push(
                _.find($scope.candidatos, function(obj, list){ return obj.pk == elem.value; })
            );
        });

        sharedService.broadcast(seleccionadoslist, "candidatos");
        angular.element("#nueva-verificacion").modal('hide');
    };

    /*############# Inicio confifiguracion paginacion #############*/
    $scope.$watch('currentPage', function(newValue, oldValue) {
        if (($scope.currentPage != undefined && oldValue != undefined) && (newValue != oldValue )){
            $scope.candidatos = $scope.allItems[newValue-1]
        }
    });

    $scope.initPagination = function (items, itemsPerPage){
        function splitArray(arr, n) {
            return arr.reduce(function(p, cur, i) {
                (p[i/n|0] = p[i/n|0] || []).push(cur);
                return p;
            },[]);
        }

        $scope.itemsInAllPages = _.size(items); // numero total de items en todas las paginas
        $scope.itemsPerPage = itemsPerPage // items por pagina
        $scope.allItems = splitArray(items, itemsPerPage); //lista de todos los objetos
        $scope.currentPage = 1; // pagina actual
    };

    /*############# Fin confifiguracio paginacion #############*/

}]);

coreApp.controller('BuscarFuncionariosCtrl',
    ['$scope', '$http', '$log', '$cookies', '$rootScope', 'sharedService', '$timeout', 'windowLocationOrigin', '$cookieStore',
    function($scope, $http, $log, $cookies, $rootScope, sharedService, $timeout, windowLocationOrigin, $cookieStore) {
    var token = $cookies['csrftoken'];
    $scope.patternCedula = $rootScope.patterns['cedula'];
    $scope.funcionarios = [];
    $scope.candidato_id = "";
    $scope.alerta = {mostrar: false, texto: "", htmlclass: "" };
    $scope.funcionariosSeleccionados = [];
    $scope.funcionarioDeApoyo;
    $scope.funcionariosListados = [];
    $cookieStore.put('cookie_funcionarios', []);

    $scope.buscarFuncionario = function(form) {
        $scope.submitted = true;
        if (form.$invalid) {
             return;
        }
        var data = {cedula: $scope.cedula, csrfmiddlewaretoken: token };
        $scope.search(data);
    };

    $scope.search = function(data) {
        $http({
            url: windowLocationOrigin + "/inteligencia_tributaria/buscar_funcionario/",
            method: "POST",
            dataType: "json",
            data: data,
        }).success(function (response, status) {
            if (response.success==true){
                response.clean = true
                $scope.nuevoFuncionario(response);
            }
        }).error(function (response, status){
            $log.error("Error Status code:"+status+" al consulltar el servicio");
        });
    };

    $scope.nuevoFuncionario = function(objects){
        var items;
        if (objects.success == true && _.size(objects.data) > 0){
            $scope.resultado=true;
            if(objects.clean == false){
                $scope.funcionarios.push(objects.data[0]);
                items = $scope.funcionarios;

            }
            if(objects.clean == true){
                items = objects.data
            }
            $scope.iniciar_cookie(items);
            $scope.initPagination(items, 5);
            $scope.funcionarios = $scope.allItems[0]; // primeros candidatos para la cantidad solicitada
        }
    };

    $scope.$watch('funcionarios', function(newValue, oldValue) {
        _.each($scope.funcionarios, function(obj, k){
            if (obj.role == 4){
                angular.element('#apoyo-'+obj.pk).iCheck('check');
                angular.element('#apoyo-'+obj.pk).iCheck('disable');
            }
        });
        $scope.selected_cookies();
    });

    $scope.submit = function(event){
        var data = [];
        var coordinador, mensaje, coord_seleccionado = false;
        var cookie_list = $cookieStore.get('cookie_funcionarios');
        var listCoordinadores = angular.element('[name="coordinador[]"]');
        $scope.informar(false, "", "", 0);

        /* Obtenemos coordinadores seleccionados previamente*/
        if ($scope.funcionariosSeleccionados != undefined){
            coord_seleccionado = _.some($scope.funcionariosSeleccionados, function(obj, key){
                return obj.coordinador == true;
            });
        }

        /* Obtenemos la lista completa de los funcionarios seleccionados*/
        cookie_list=_.filter(cookie_list, function(obj, k){ return obj.es_seleccionado == true; });
         if (_.size(cookie_list) == 0){
            mensaje = "Debe elegir al menos un funcionario";
            $scope.informar(true, mensaje, "alert-danger", 2);
            return;
        }

        /* Obtenemos los coordinadores seleccionados */
        coordinador=_.filter(cookie_list, function(obj, k){ return obj.es_coordinador == true; });
        if ((_.size(coordinador)!=1) && (coord_seleccionado==false)){
            mensaje = "Debe seleccionar un único supervisor";
            $scope.informar(true, mensaje, "alert-danger", 2);
            return;
        }

        /* Validamos que no se haya seleccionado un supervisor y ya tenga uno asignado al candidato */
        if ((_.size(coordinador)) && (coord_seleccionado)){
            mensaje = "Ya se ha asignado un supervisor para este candidato";
            $scope.informar(true, mensaje, "alert-danger", 2);
            return;
        }

        /* Agregamos los funcionarios seleccionados a un arreglo nuevo para el main */
        if (_.size(cookie_list) > 0){
            _.each(cookie_list, function(obj, k){
                if (obj.es_seleccionado){
                    data.push({
                        coordinador: obj.es_coordinador,
                        apoyo: obj.es_apoyo,
                        analista: obj.pk
                    });
                }
            });
        }

        if (_.size(data)){
            $scope.listarFuncionarios(data)
        }
    };

    $scope.$on('broadcastHandler', function(event, data, type) {
        if(type == "candidato_id"){ $scope.candidato_id = data; }
        if(type == "reinicio_funcionario"){ $scope.funcionarios = data; }
        if(type == "funcionarios_seleccionados"){ $scope.funcionariosSeleccionados = data; }
        if(type == "funcionario_apoyo_creados"){
            var f = {success: true, data: [data], clean: false};
            $scope.nuevoFuncionario(f); }
    });

    $scope.listarFuncionarios = function (seleccionados){
        var seleccionadoslist = [];
        var existe;
        var storage = JSON.parse(localStorage.getItem("storage_funcionarios"));

        _.each(seleccionados, function(k, list){
            seleccionadoslist.push({
                data:_.find(storage, function(obj, list){ return obj.pk == k.analista; }),
                coordinador: k.coordinador,
                apoyo: k.apoyo
            });
        });
        var data = [$scope.candidato_id, seleccionadoslist]
        /* Si hay registros asignados anteriormente le hacemos un push a los elementos anteriores */
        if ($scope.funcionariosSeleccionados != undefined){
            _.each(seleccionadoslist, function(obj, k){
                existe = _.some($scope.funcionariosSeleccionados, function(elem, key){
                    return elem.data.pk == obj.data.pk
                });

                if (existe == false){ $scope.funcionariosSeleccionados.push(obj); }
            });

            data = [$scope.candidato_id, $scope.funcionariosSeleccionados]
        }

        sharedService.broadcast(data, "funcionarios");
        angular.element("#modalFuncionario").modal('hide');
    };

    $scope.informar = function(mostrar, texto, htmlclass, seconds){
        $scope.alerta.texto = texto;
        $scope.alerta.htmlclass = htmlclass;
        $scope.alerta.mostrar = mostrar;
        if ((mostrar) && (seconds != 0)){
            $timeout(function() {
                $scope.alerta.mostrar = false;
            }, seconds * 1000);
        }
    };

    /*############# Inicio confifiguracion paginacion #############*/
    $scope.$watch('currentPage', function(newValue, oldValue) {
        $scope.actualizar_cookie();
        /* ################## Paginación ###################### */
        if (_.size($scope.funcionarios)==0){
            $scope.currentPage=undefined
        }
        if (($scope.currentPage != undefined && oldValue != undefined) && (newValue != oldValue )){
            $scope.funcionarios = $scope.allItems[newValue-1]
        }
    });

    $scope.iniciar_cookie = function(objects){
        $cookieStore.remove('cookie_funcionarios');
        localStorage.removeItem("storage_funcionarios");
        localStorage.setItem("storage_funcionarios", JSON.stringify(objects) );
        var object=[];
        var seleccionado=false;
        var elem={};

        _.each(objects, function(obj, k){
            elem = {
                es_seleccionado: seleccionado,
                es_coordinador: false,
                es_apoyo: false,
                pk: obj.pk
            }
            object.push(elem);
        });
        $cookieStore.put('cookie_funcionarios', object);
    };


    $scope.selected_cookies = function(){
        var cookie_list = $cookieStore.get('cookie_funcionarios');
        _.each(cookie_list, function(obj, k){
            if (obj.es_seleccionado){
                angular.element('#funcionario-'+obj.pk).iCheck('check');
                if (obj.es_coordinador){ angular.element('#coordinador-'+obj.pk).iCheck('check'); }
                if (obj.es_apoyo){ angular.element('#apoyo-'+obj.pk).iCheck('check'); }
            }

        });
    };

    $scope.actualizar_cookie = function(){
        // metodo para actualizar la cookie del funcionario
        var listFuncionarios = angular.element('[name="funcionarios[]"]');
        var cookie_list = $cookieStore.get('cookie_funcionarios');
        var es_coordinador;
        var es_apoyo;
        var cookie_element;

        _.each(listFuncionarios, function(obj, k){
            es_coordinador = false;
            es_apoyo = false;
            if (angular.element('#coordinador-'+obj.value).is(':checked') == true){ es_coordinador = true; }
            if (angular.element('#apoyo-'+obj.value).is(':checked') == true){ es_apoyo = true; }
            cookie_element = _.find(cookie_list, function(elem, k){ return elem.pk == obj.value; });
            if (cookie_element){
                cookie_element.es_coordinador=es_coordinador;
                cookie_element.es_apoyo=es_apoyo;
                cookie_element.es_seleccionado=$(obj).is(':checked');
            }
        });
        $cookieStore.remove('cookie_funcionarios');
        $cookieStore.put('cookie_funcionarios', cookie_list);
        cookie_list = $cookieStore.get('cookie_funcionarios');

    };

    $scope.initPagination = function (items, itemsPerPage){
        function splitArray(arr, n) {
            return arr.reduce(function(p, cur, i) {
                (p[i/n|0] = p[i/n|0] || []).push(cur);
                return p;
            },[]);
        }

        $scope.itemsInAllPages = _.size(items); // numero total de items en todas las paginas
        $scope.itemsPerPage = itemsPerPage // items por pagina
        $scope.allItems = splitArray(items, itemsPerPage); //lista de todos los objetos
        $scope.currentPage = 1; // pagina actual
    };
    /*############# Fin confifiguracio paginacion #############*/

    $scope.funcionarioApoyo = function(){
        angular.element("#modalFuncionarioApoyo").modal('show');
        sharedService.broadcast(true, "apoyo_modal");
    }

}]);

coreApp.controller('MainCandidatosCtrl',
    ['$scope', '$http', '$log', 'sharedService', '$timeout', '$rootScope', function($scope, $http, $log, sharedService, $timeout, $rootScope) {

    $scope.candidatosSeleccionados = [];
    $scope.funcionariosSeleccionados = [];
    $scope.funcionariosDeApoyo = [];
    $scope.solicitud = [];
    $scope.verificacion = [];
    $scope.verificacionSelect= [];
    $scope.fechaInicio = [];
    $scope.fechaFin = [];
    $scope.alerta = {mostrar: false, texto: "", htmlclass: "" };
    $scope.limite_fecha_hasta = [];
    var existe;
    $scope.tipo_verificacion = [
        {value: 0, name: 'En sede administrativa'},
        {value: 1, name: 'En domicilio fiscal'},
    ]

    $scope.tipo_solicitud = [
        {value: 0, name: 'Verificación'},
        {value: 1, name: 'Fiscalización'},
        {value: 2, name: 'Verificación y Fiscalización'},
    ];

    $scope.seleccion_solicitud = function(id){
        if ($scope.solicitud[id] != undefined){
            $scope.verificacionSelect[id] = false;
            /* mostramos selecect  automatico cundo es verificacion*/
            if ($scope.solicitud[id].value == $scope.tipo_solicitud[0]['value']){
                $scope.verificacionSelect[id] = true;
            }
        }
    };

    $scope.$on('broadcastHandler', function(event, data, type) {
        if(type == "candidatos"){
            _.each(data, function(obj, k){
                existe = _.some($scope.candidatosSeleccionados, function(element, key){
                    return element.pk == obj.pk;
                });

                if (existe==false){ $scope.candidatosSeleccionados.push(data[k]);}
            });

        }
        if(type == "funcionarios"){
            $scope.funcionariosSeleccionados[data[0]] = data[1];
        }
        if(type == "funcionario_apoyo"){
            var fapoyo = [];
            if (_.size($scope.funcionariosDeApoyo[data[0]]) > 0){
                _.each($scope.funcionariosDeApoyo[data[0]], function(obj, k){
                    fapoyo.push(obj)
                });
            }
            fapoyo.push(data[1])
            $scope.funcionariosDeApoyo[data[0]] = fapoyo;
        }

    });

    $scope.limite_fecha = function(id){
        var date = $scope.fechaInicio[id].split("-");
        var dia = 1;
        var mes = $rootScope.MESES[_.str.chop(date[0], 3)[0]];
        var anio = date[1];
        date = _.str.sprintf("%s-%s-%s", dia, mes, anio)
        var d = moment(date, "DD-MM-YYYY").add('months', 1);
        var ele = angular.element("#fecha-fin-"+id);
        ele.datepicker("remove");
        ele.datepicker({
            language: "es",
            autoclose: true,
            startDate: d.format("MM-YYYY"),
            clearBtn: 'Limpiar',
        });
    };

    $scope.submit = function(event){
        event.preventDefault();
        var form = angular.element('[name="formCrearSolicitud"]')
        var solicitud_valida = $scope.validar_solicitud();
        if (solicitud_valida[0] == false){
            $scope.informar(true, solicitud_valida[1], "error", 2);
            return;
        }
        $scope.informar(true, solicitud_valida[1], "successAgregarFuncionariosApoyoCtrl", 3);
        form.submit();
    };

    $scope.validar_solicitud = function(){
        var status = true;
        var exist = "";

        if (_.size($scope.candidatosSeleccionados) == 0){
            return [false, "Debe seleccionar al menos un candidato"];
        }

        if (_.size($scope.solicitud) != _.size($scope.candidatosSeleccionados)){
            return [false, "Todos los tipos de solicitud son requeridos"];
        }

        if (_.size($scope.solicitud) > 0){
            _.each($scope.solicitud, function(obj, k){
                if ((obj.value == $scope.tipo_solicitud[0]['value']) && ($scope.verificacion[k] == undefined)){
                    exist = "Todos los tipos de verificacion son requeridos";
                }
            });
            if (exist != ""){
                return [false, exist];
            }
        }

        if (_.size($scope.candidatosSeleccionados) != _.size($scope.fechaInicio)){
            return [false, "Todos los periodos de solicitud son rqueridos"];
        }

        if (_.size($scope.candidatosSeleccionados) != _.size($scope.fechaFin)){
            return [false, "Todos los periodos de solicitud son rqueridos"];
        }

        if (_.size($scope.candidatosSeleccionados) != _.size($scope.funcionariosSeleccionados)){
            return [false, "Debe asignar al menos un funcionario para todos las solicitudes"];
        }

        return [true, "La información fue enviada para su aprobación"];
    };

    $scope.eliminar_candidato = function(id){
        $scope.candidatosSeleccionados.splice(id, 1);
        $scope.solicitud.splice(id, 1);
        $scope.fechaInicio.splice(id, 1);
        $scope.fechaFin.splice(id, 1);
        $scope.funcionariosSeleccionados.splice(id, 1);
    };

    $scope.modal_funcionario = function(id){
        angular.element("[name='coordinador[]']").iCheck('uncheck');
        angular.element("[name='funcionarios[]']").iCheck('uncheck');
        sharedService.broadcast($scope.funcionariosSeleccionados[id], "funcionarios_seleccionados");
        sharedService.broadcast(id, "candidato_id");
        sharedService.broadcast([], "reinicio_funcionario");
        angular.element('#modalFuncionario').modal('show');
    };

    $scope.informar = function(mostrar, texto, htmlclass, seconds){
        $scope.alerta.texto = texto;
        $scope.alerta.htmlclass = htmlclass;
        $scope.alerta.mostrar = mostrar;
        if ((mostrar) && (seconds != 0)){
            $timeout(function() {
                $scope.alerta.mostrar = false;
            }, seconds * 1000);
        }
    };

    $scope.eliminar_funcionario = function(arrayId, idFuncionario){
        var objEliminar = $scope.funcionariosSeleccionados[arrayId][idFuncionario];
        var nuevo_array = _.without($scope.funcionariosSeleccionados[arrayId], objEliminar);
        $scope.funcionariosSeleccionados[arrayId] = nuevo_array;
    };

    $scope.eliminar_funcionario_apoyo = function(arrayId, idFuncionarioApoyo){
        var objEliminar = $scope.funcionariosDeApoyo[arrayId][idFuncionarioApoyo];
        var nuevo_array = _.without($scope.funcionariosDeApoyo[arrayId], objEliminar);
        $scope.funcionariosDeApoyo[arrayId] = nuevo_array;
    };

}]);

coreApp.controller('IdiomasModalCtrl',
    ['$scope', '$element', '$log', '$cookies', 'windowLocationOrigin', function($scope, $element, $log, $cookies, windowLocationOrigin) {

    var template = _.template(
          '<tr>'
        + '  <td><%= nombre %></td>'
        + '  <td><span class="fa fa-<% if (lee){ %>check-<% } %>square"></span></td>'
        + '  <td><span class="fa fa-<% if (habla){ %>check-<% } %>square"></span></td>'
        + '  <td><span class="fa fa-<% if (escribe){ %>check-<% } %>square"></span></td>'
        + '  <td><a class="fa fa-trash-o" href="#" data-id="<%= pk %>"></a></td>'
        + '</tr>'
    );

    $.ajax({
        url: windowLocationOrigin + '/registro/natural/idiomas',
        method: 'GET',
    }).success(function(data) {
        if (data.error == 0) {
            $scope.$apply(function() {
                $scope.idiomas = JSON.parse(data.result);
            });
        }
    });

    $.ajax({
        url: windowLocationOrigin + '/registro/natural/idiomas/pst',
        method: 'GET',
    }).success(function(data) {
        if (data.error == 0) {
            var idiomas_pst = JSON.parse(data.result);
            var idiomas_nombres = data.attached;

            for (var i = 0; i < idiomas_pst.length; i++) {
                $scope.addIdiomaPst({
                    pk: idiomas_pst[i].pk,
                    nombre: idiomas_nombres[i],
                    lee: idiomas_pst[i].fields.lee,
                    habla: idiomas_pst[i].fields.habla,
                    escribe: idiomas_pst[i].fields.escribe,
                });
            }
        }
    });

    angular.element('#idiomas-modal').on('show.bs.modal', function() {
        var $el = $(this);

        $el.find('select option:first-of-type').prop('selected', true);
        $el.find('input[type="checkbox"]').iCheck('uncheck');
    });

    $scope.onClick = function() {
        var $el = $('#idiomas-modal');
        var is_empty = true;

        $el.find('input[type="checkbox"]').each(function() {
            if ($(this).prop('checked')) is_empty = false;
        });

        if (is_empty) {
            alert('Debe indicar alguna destreza para este idioma');
            return;
        }

        $scope.postIdiomaPst($el);
    };

    $scope.postIdiomaPst = function($modal) {
        $.ajax({
            url: windowLocationOrigin + '/registro/natural/idiomas/pst',
            method: 'POST',
            data: {
                idioma_id: $modal.find('select option:selected').val(),
                lee: $modal.find('input[value="lee"]').prop('checked'),
                habla: $modal.find('input[value="habla"]').prop('checked'),
                escribe: $modal.find('input[value="escribe"]').prop('checked'),
                csrfmiddlewaretoken: $cookies['csrftoken'],
            }
        }).success(function(data) {
            if (data.error == 0) {
                var idioma_pst = JSON.parse(data.result)[0];

                $scope.addIdiomaPst({
                    pk: idioma_pst.pk,
                    nombre: data.attached,
                    lee: idioma_pst.fields.lee,
                    habla: idioma_pst.fields.habla,
                    escribe: idioma_pst.fields.escribe,
                });
                $modal.modal('hide');
            } else {
                alert(data.msg);
            }
        });
    };

    $scope.addIdiomaPst = function(obj) {
        var $el = $(template(obj))
        $el.find('a').click($scope.delIdiomaPst);
        angular.element('#idiomas-body').append($el);
    };

    $scope.delIdiomaPst = function() {
        var $el = $(this);

        $.ajax({
            url: windowLocationOrigin + '/registro/natural/idiomas/pst/del',
            method: 'POST',
            data: {
                idioma_pst_id: $el.attr('data-id'),
                csrfmiddlewaretoken: $cookies['csrftoken'],
            }
        }).success(function(data) {
            if (data.error == 0) $el.parents('tr').remove();
        });
    };

}]);

coreApp.controller('FiltrarReportesCtrl',
    ['$scope', '$http', '$log', '$cookies', '$rootScope', 'sharedService', function($scope, $http, $log, $cookies, $rootScope, sharedService) {

	$scope.patternRif = $rootScope.patterns['rif'];
    $scope.resultado = false;
    $scope.candidatos = [];
    $scope.estadosList = []
    $scope.alerta = {mostrar: false, texto: "", htmlclass: "" };
    var token = $cookies['csrftoken'];

	$scope.busquedaRapida = function(event) {
		event.preventDefault();
		var data = angular.element('[name="fromCandidatos"]').serialize()+"&busqueda=avanzada";
        //$scope.search(data);
		$scope.submit_all(data);
	};

    $scope.busquedaAvanzada = function(event) {
        event.preventDefault();
        var data = angular.element('[name="fromCandidatos"]').serialize()+"&busqueda=avanzada";
        $scope.search(data);
    };

    $scope.$watch('estado', function() {
        if ($scope.estado != undefined  && $scope.estado != ""){
            var url = "/municipios/"+$scope.estado.id;
            $scope.parroquiasList = [];
            $scope.buscar_ubicacion(url, "municipio");
        }

    });

    $scope.$watch('municipio', function() {
        if ( $scope.municipio != undefined && $scope.municipio != "" ){
            var url = "/parroquias/"+$scope.municipio.id;
            $scope.buscar_ubicacion(url, "parroquia");
        }
    });


    $scope.buscar_ubicacion = function(url, type) {
        $http({
          url: url,
          method: "GET",
          dataType: "json",
        }).success(function (response, status) {
            if (response.success = true){
                if(type == "municipio"){ $scope.municipiosList = response.municipios; }
                if(type == "parroquia"){ $scope.parroquiasList = response.parroquias; }
            }else{ $log.error(response.error); }
        }).error(function (response, status){
               $log.error("Error Status code:"+status+", al obtener la lista de valores");
        });
    };


    $scope.search = function(data, url) {
		var filtros = data;
        $http({
          url: "./filtrar_reportes/",
          method: "POST",
          dataType: "json",
          data: data,
        }).success(function (response, status) {
            $scope.candidatosList(response);
			$('.reporte_lista_form_filtros').val(data);
        }).error(function (response, status){
            $log.error("Error Status code:"+status+", al obtener la lista de valores");
        });
    };

    /*############# Inicio confifiguracion paginacion #############*/
    $scope.$watch('currentPage', function(newValue, oldValue) {
        if (($scope.currentPage != undefined && oldValue != undefined) && (newValue != oldValue )){
            $scope.candidatos = $scope.allItems[newValue-1]
        }
    });

    $scope.initPagination = function (items, itemsPerPage){
        function splitArray(arr, n) {
            return arr.reduce(function(p, cur, i) {
                (p[i/n|0] = p[i/n|0] || []).push(cur);
                return p;
            },[]);
        }

        $scope.itemsInAllPages = _.size(items); // numero total de items en todas las paginas
        $scope.itemsPerPage = itemsPerPage // items por pagina
        $scope.allItems = splitArray(items, itemsPerPage); //lista de todos los objetos
        $scope.currentPage = 1; // pagina actual
    };
    /*############# Fin confifiguracio paginacion #############*/

    $scope.candidatosList = function(objects){
        $scope.candidatos = [];
        if (objects.success == true && _.size(objects.data) > 0){
            $scope.resultado = true;
            $scope.initPagination(objects.data, 5);
            $scope.candidatos = $scope.allItems[0]; // primeros candidatos para la cantidad solicitada
            $scope.alerta = {mostrar: true, texto: "Se Encontraron Candidatos", htmlclass: "alert-success" };
        }
    };

    $scope.submit = function(event){
        event.preventDefault();
		var ids = [];
        var data = [];
        var candidatos = angular.element('[name="candidato[]"]');
        _.each(candidatos, function(elem, k, list){
            if (angular.element(elem).is(':checked')==true){
                data.push(elem.value);
				ids.push(elem.value);
            }
        });

        if( _.size(data) > 0 ){
            $scope.listarCandidatos(data)
			$('.reporte_lista_form_ids').val(ids);
        }
    };

	$scope.submit_all = function(data){

		$http({
          url: "./filtrar_reportes/",
          method: "POST",
          dataType: "json",
          data: data,
        }).success(function (objects, status) {
			var psts = objects.data;
			var ids = [];
			$scope.candidatos = objects.data;
			_.each(psts, function(elem) {
				ids.push(elem.pk.toString());
			});
			$scope.listarCandidatos(ids);
			angular.element('.reporte_lista_form_ids').val(ids);
			angular.element('.reporte_lista_form_filtros').val(data);
        }).error(function (response, status){
            $log.error("Error Status code:"+status+", al obtener la lista de valores");
        });
    };

    $scope.listarCandidatos = function (seleccionados){
        $scope.candidatosSeleccionados = [];
        var seleccionadoslist = [];
        _.each(seleccionados, function(pk){
            seleccionadoslist.push(
                _.find($scope.candidatos, function(obj, list){ return obj.pk == pk; })
            );
        });

        sharedService.broadcast(seleccionadoslist, "candidatos");
        angular.element("#filtro-modal").modal('hide');
    };

}]);

coreApp.controller('editarSolicitudCtrl',
    ['$scope', '$http', '$log', '$cookies', 'sharedService', function($scope, $http, $log, $cookies, sharedService) {
    $scope.funcionariosList = [];
    $scope.alerta = {mostrar: false, texto: "", htmlclass: "" };
    $scope.submit = function(formName, event){
        event.preventDefault();
        $scope.submitted = true;
        if (formName.$invalid) { return; }
        if(_.size($scope.funcionariosList) == 0){
            $scope.informar(true, "Debe asignar al menos un Funcionario para guardar la solicitud", "alert-danger", 0);
            return;
        };

        var form = angular.element("[name='formEditarSolicitud']");
        form.submit();
    };

    $scope.$on('broadcastHandler', function(event, data, type) {
        var existe, asignacion, datos = {};
        if(type == "funcionarios"){
            _.each(data[1], function(obj, list){
                existe = _.some($scope.funcionariosList, function(objList, list){
                    return objList.usuario_id == obj.data.pk;
                });

               if (existe==false){
                    datos = {
                        usuario_id: obj.data.pk,
                        nombres: obj.data.nombres,
                        apellidos: obj.data.apellidos,
                        rif: obj.data.rif,
                        es_coordinador: obj.coordinador,
                    }
                    $scope.funcionariosList.push(datos);
               }
            });
        }
    });


    $scope.eliminar_funcionario = function(id){
       $scope.funcionariosList.pop(id);
    };

    $scope.informar = function(mostrar, texto, htmlclass, seconds){
        $scope.alerta.texto = texto;
        $scope.alerta.htmlclass = htmlclass;
        $scope.alerta.mostrar = mostrar;
        if ((mostrar) && (seconds != 0)){
            $timeout(function() {
                $scope.alerta.mostrar = false;
            }, seconds * 1000);
        }
    };

}]);

coreApp.controller('VerificacionGerenteCtrl',
    ['$scope', '$http', '$log', '$timeout', '$cookies', '$window', function($scope, $http, $log, $timeout, $cookies, $window) {

    var form = angular.element("[name='formAprobacionSolicitud']");
    var solicitudes = angular.element("[name='solicitud[]']");
    var token = $cookies['csrftoken'];
    var ele = angular.element("[name='todos']");
    var items = angular.element("[name='solicitud[]']");

    $scope.alerta = {mostrar: false, texto: "", htmlclass: "" };

    ele.on('ifChecked', function(){  items.iCheck('check') });
    ele.on('ifUnchecked', function(){ items.iCheck('uncheck'); });

    $scope.aprobar = function(event){
        $scope.informar(false, "", "", 0);
        event.preventDefault();
        var ids = []
        var seleccionados = _.filter(solicitudes, function(obj, k){
            return angular.element(obj).is(':checked') == true;
        });

        if(_.size(seleccionados) == 0){
            $scope.informar(true, "Debe al menos seleccionar una solicitud", "alert-danger", 2);
            return;
        }

        _.each(seleccionados, function(obj, k){
            if (obj.value != undefined){
                ids.push(obj.value)
            }
        });
        $scope.informar(true, "Procesando. Por favor espere...", "alert-info", 0);
        angular.element(".cancelar").attr('disabled','disabled');
        angular.element(".aceptar").attr('disabled','disabled');

        $http({
          url: form.attr('action'),
          method: "POST",
          dataType: "json",
          data: {solicitud: ids, csrfmiddlewaretoken: token, tipo: "aprobar" },
        }).success(function (response, status) {

            if (response.success==true){
                $scope.informar(true, response.message, "alert-success", 2);
                $timeout(function() {
                    angular.element('#aprobar_seleccionados').modal('hide');
                }, 2000);

                $scope.reloadRoute();
            }else{
                $scope.informar(true, response.message, "alert-danger", 2);
            }

        }).error(function (response, status){
            $log.error("Error Status code:"+status+", al obtener la lista de valores");
        });
    };

    $scope.informar = function(mostrar, texto, htmlclass, seconds){
        $scope.alerta.texto = texto;
        $scope.alerta.htmlclass = htmlclass;
        $scope.alerta.mostrar = mostrar;
        if ((mostrar) && (seconds != 0)){
            $timeout(function() {
                $scope.alerta.mostrar = false;
            }, seconds * 1000);
        }
    };

    $scope.reloadRoute = function() {
            var seconds = 1;
            $timeout(function() {
                $window.location.reload();
            }, seconds * 1000);
    };

    $scope.rechazar = function(event) {
        $scope.informar(false, "", "", 0);
        event.preventDefault();
        var ids = [];
        var seleccionados = _.filter(solicitudes, function(obj, k){
            return angular.element(obj).is(':checked') == true;
        });

        if(_.size(seleccionados) == 0){
            $scope.informar(true, "Debe al menos seleccionar una solicitud", "alert-danger", 2);
            return;
        }

        if($scope.comentarios == "" || $scope.comentarios == undefined){
            $scope.informar(true, "Las razones de rechazo son requeridas", "alert-danger", 2);
            return;
        }

        _.each(seleccionados, function(obj, k){
            if (obj.value != undefined){
                ids.push(obj.value)
            }
        });

        $http({
            url: form.attr('action'),
            method: "POST",
            dataType: "json",
            data: {solicitud: ids,
                   csrfmiddlewaretoken: token,
                   tipo: "rechazar",
                   comentarios: $scope.comentarios
               },
        }).success(function (response, status) {
            if (response.success==true){
                $scope.informar(true, response.message, "alert-success", 2);
                $timeout(function() {
                    angular.element('#rechazar_seleccionados').modal('hide');
                }, 2000);

                $scope.reloadRoute();
            }else{
                $scope.informar(true, response.message, "alert-danger", 2);
            }

        }).error(function (response, status){
            $log.error("Error Status code:"+status+", al obtener la lista de valores");
        });

        angular.element(".cancelar").attr('disabled','disabled');
        angular.element(".aceptar").attr('disabled','disabled');

    };

}]);

coreApp.controller('FactibilidadCtrl',
    ['$scope', '$http', '$log', '$timeout', '$cookies', '$window', function($scope, $http, $log, $timeout, $cookies, $window) {

    var token = $cookies['csrftoken'];
    $scope.tipo_solicitud = [];
    $scope.tipo_actividad = [];
    $scope.submitted = false;
    $scope.alerta = {mostrar: false, texto: "", htmlclass: "" };
    $scope.alerta.eliminar = {mostrar: true, texto: "HOla mundo", htmlclass: "alert-success" };

    $scope.nueva_factibilidad = function(event, form) {
        event.preventDefault();
        var form_obj = angular.element("[name='formCrearFactibilidad']")
        $scope.submitted = true;
        if (form.$invalid) {
            return;
        }

        $scope.alerta = {mostrar: true, texto: "Creando la factibilidad por favor espere..", htmlclass: "alert-info" };

        $http.post( form_obj.attr('action'), form_obj.serialize()).success(function(response, status){
            if(response.success == true){
                $scope.alerta = {mostrar: true, texto: response.message, htmlclass: "alert-success" };
                $window.location.href = response.url;
            }else{
                $scope.alerta = {mostrar: true, texto: response.message, htmlclass: "alert-danger" };
            }
        });
    };

    $scope.modal_anulacion = function(id){
        $scope.idFactibilidad = id;
        angular.element('#anular-factibilidad').modal('show');

    };

    $scope.eliminar_factibilidad = function(event, form) {
        event.preventDefault();
        var token = $cookies['csrftoken'];
        $scope.submitted = true;
        if (form.$invalid) {
            return;
        }
        var data = {
            id_factibilidad: $scope.idFactibilidad,
            justificacion: $scope.justificacion,
            csrfmiddlewaretoken: token
        }

        var objForm = angular.element("[name='"+form.$name+"']");
        $http.post(objForm.attr('action'), data).success(function(response, status) {
            if (response.sucess == true){

            }
        });
    };

    $scope.reloadRoute = function() {
        var seconds = 1;
        $timeout(function() {
            $window.location.reload();
        }, seconds * 1000);
    };

}]);

coreApp.controller('FactibilidadNuevaCtrl',
    ['$scope', '$http', '$log', '$timeout', '$cookies', '$window', function($scope, $http, $log, $timeout, $cookies, $window) {

    var token = $cookies['csrftoken'];
    $scope.submitted = false;
    $scope.indole = [];
    $scope.aspecto_social = [];
    $scope.unidad_transporte = [];
    $scope.tipo_proyecto;
    $scope.input = {tipo_proyecto: false, unidades: false, aspecto: false}


    $scope.validar_formulario = function(event, form) {
        event.preventDefault();
        var objForm = angular.element("[name='"+form.$name+"']");
        var tipo_proyecto = false;
        var unidades = false;
        var aspecto = false;
        var indole = false;

        $scope.submitted = true;
        $scope.input = {
            tipo_proyecto: false,
            unidades: false,
            aspecto: false,
            indole: false
        }

        tipo_proyecto = _.some(angular.element("[name='tipo_proyecto']"), function(obj, k){
            return $(obj).is(':checked') == true;
        });

        if (tipo_proyecto == false) {
            $scope.input.tipo_proyecto = true;
            form.$invalid = true;
        }

        unidades = _.some(angular.element("[name='unidad_transporte[transporte]']"), function(obj, k){
            return $(obj).is(':checked') == true;
        });

        if (unidades == false) {
            $scope.input.unidades = true;
            form.$invalid = true;
        }

        aspecto = _.some(angular.element("[name='tipo_aspecto[aspecto]']"), function(obj, k){
            return $(obj).is(':checked') == true;
        });

        if (aspecto == false) {
            $scope.input.aspecto = true;
            form.$invalid = true;
        }

        indole = _.some(angular.element("[name='tipo_indole[indole]']"), function(obj, k){
            return $(obj).is(':checked') == true;
        });

        if (indole == false) {
            $scope.input.indole = true;
            form.$invalid = true;
        }

        if (form.$invalid) {
            return;
        }

        objForm.submit();
    };

    $scope.$watch('indole', function() {
        _.each($scope.indole, function(obj, k){
            angular.element('#indole-'+obj.tipo).iCheck('check');
        });
    });

    $scope.$watch('aspecto_social', function() {
        _.each($scope.aspecto_social, function(obj, k){
            angular.element('#aspecto-'+obj.tipo).iCheck('check');
        });
    });

    $scope.$watch('unidad_transporte', function() {
        _.each($scope.unidad_transporte, function(obj, k){
            angular.element('#transporte-'+obj.tipo).iCheck('check');
        });
    });

    $scope.$watch('tipo_proyecto', function() {
        angular.element('#tipo-'+$scope.tipo_proyecto).iCheck('check');
    });

}]);

coreApp.controller('FactibilidadPasoDosCtrl',
    ['$scope', '$http', '$log', '$timeout', '$cookies', '$window', function($scope, $http, $log, $timeout, $cookies, $window) {

    var token = $cookies['csrftoken'];
    $scope.submitted = false;
    $scope.estadosList = [];
    $scope.municipiosList = [];
    $scope.parroquiasList = [];
    $scope.required = {vialidad: false, topografia: false, servicio_basico: false };
    $scope.$watch('estado', function() {
        if ($scope.estado != undefined  && $scope.estado != ""){
            $scope.parroquiasList = [];
            var url = "/municipios/"+$scope.estado.id;
            $scope.search(url, "municipio");
        }

    });

    $scope.$watch('municipio', function() {
        if ( $scope.municipio != undefined && $scope.municipio != "" ){
            var url = "/parroquias/"+$scope.municipio.id;
            $scope.search(url, "parroquia");
        }
    });

    $scope.$watch('tipografia', function() {
        angular.element('#tipografia-'+$scope.tipografia).iCheck('check');
    });

    $scope.$watch('vialidad', function() {
        angular.element('#vialidad-'+$scope.vialidad).iCheck('check');
    });

    $scope.$watch('servicios', function() {
        _.each($scope.servicios, function(obj, k){
            angular.element('#servicio-'+obj.servicio).iCheck('check');
        });
    });

    $scope.search = function(url, type) {
        $http({
          url: url,
          method: "GET",
          dataType: "json",
        }).success(function (response, status) {
            if (response.success = true){
                if(type == "municipio"){
                    $scope.municipiosList = response.municipios;
                    angular.element('#id_municipio').val($scope.estados)
                }
                if(type == "parroquia"){
                    $scope.parroquiasList = response.parroquias;
                    angular.element('#id_parroquia').val($scope.parroquias)
                }
                $scope.change=false;

            }else{ $log.error(response.error); }
        }).error(function (response, status){
               $log.error("Error Status code:"+status+", al obtener la lista de valores");
        });
    };

    $scope.validar_formulario = function(event, form) {
        event.preventDefault();
        var objForm = angular.element("[name='"+form.$name+"']");
        $scope.submitted = true;
        var vialidad = false;
        var servicio = false;
        var tipografia = false;
        $scope.required = {vialidad: false, tipografia: false, servicio_basico: false };

        vialidad = _.some(angular.element("[name='vialidad']"), function(obj, k){
            return $(obj).is(':checked') == true;
        });
        if (vialidad == false) {
            $scope.required.vialidad = true;
            form.$invalid = true;
        }

        servicio = _.some(angular.element("[name='servicio[tipo]']"), function(obj, k){
            return $(obj).is(':checked') == true;
        });
        if (servicio == false) {
            $scope.required.servicio_basico = true;
            form.$invalid = true;
        }

        tipografia = _.some(angular.element("[name='tipografia']"), function(obj, k){
            return $(obj).is(':checked') == true;
        });
        if (tipografia == false) {
            $scope.required.tipografia = true;
            form.$invalid = true;
        }



        if (form.$invalid) {
            return;
        }
        objForm.submit();
    };

}]);

coreApp.controller('FactibilidadPasoTresCtrl',
    ['$scope', '$http', '$log', '$timeout', '$cookies', '$window', function($scope, $http, $log, $timeout, $cookies, $window) {
    $scope.submitted = false;


    $scope.$watch('hotel', function() {
        angular.element('#hotel-'+$scope.hotel).iCheck('check');
    });

    $scope.$watch('hotel_residencia', function() {
        angular.element('#residencia-'+$scope.hotel_residencia).iCheck('check');
    });

    $scope.$watch('posada', function() {
        angular.element('#posada-'+$scope.posada).iCheck('check');
    });

    $scope.$watch('campamentos_estancias', function() {
        angular.element('#campamentos-'+$scope.campamentos_estancias).iCheck('check');
    });

    $scope.$watch('parador', function() {
        angular.element('#parador-'+$scope.parador).iCheck('check');
    });

    $scope.$watch('balneario', function() {
        angular.element('#balneario-'+$scope.balneario).iCheck('check');
    });

    $scope.$watch('posada_familiar', function() {
        angular.element('#posada_familiar-'+$scope.posada_familiar).iCheck('check');
    });

    $scope.validar_formulario = function(event, form) {
        event.preventDefault();
        var objForm = angular.element("[name='"+form.$name+"']");
        $scope.submitted = true;
        if (form.$invalid) {
            return;
        }
        objForm.submit();
    };

}]);

coreApp.controller('AgregarFuncionariosApoyoCtrl',
    ['$scope', '$http', '$log', '$timeout', 'sharedService', '$rootScope', '$cookieStore',
    function($scope, $http, $log, $timeout, sharedService, $rootScope, $cookieStore) {
    $scope.submitted = false;
    $scope.alerta = {mostrar: false, texto: "", htmlclass: "" };
    $scope.patternRif = $rootScope.patterns['rif'];
    $scope.patternCedula = $rootScope.patterns['cedula'];

    $scope.submit = function(event, form){
        $scope.submitted = true;
        if (form.$invalid) {
             return;
        }
        var objForm = angular.element("[name='"+form.$name+"']");
        $http.post(objForm.attr('action'), objForm.serialize()).success(function(response, status) {
            if (response.success == true){
                sharedService.broadcast(response.data, "funcionario_apoyo_creados");
                $scope.informar(true, response.message, 'success', 0);
                $timeout(function() {
                    angular.element("#modalFuncionarioApoyo").modal('hide');
                }, 2000);

            }else{
                $scope.informar(true, response.message, 'error error-margin', 0)
            }
        });
    };
    $scope.$on('broadcastHandler', function(event, data, type) {
        if(type == "apoyo_modal"){
            if(data){
                $scope.submitted = false;
                $scope.funcionario_apoyo = {
                    nombres: "",
                    apellidos: "",
                    cedula: "",
                    rif: ""
                }
            };
        }
    });

    $scope.informar = function(mostrar, texto, htmlclass, seconds){
        $scope.alerta.texto = texto;
        $scope.alerta.htmlclass = htmlclass;
        $scope.alerta.mostrar = mostrar;
        if ((mostrar) && (seconds != 0)){
            $timeout(function() {
                $scope.alerta.mostrar = false;
            }, seconds * 1000);
        }
    };


}]);

coreApp.controller('ResolucionesAprobacionCtrl',
    ['$scope', '$element', '$cookies', '$window', 'windowLocationOrigin', function($scope, $element, $cookies, $window, windowLocationOrigin) {

    angular.element('#toggle-check-all').on('ifChecked', function() {
        angular.element('table td input[type=checkbox]').iCheck('check');
    });

    angular.element('#toggle-check-all').on('ifUnchecked', function() {
        angular.element('table td input[type=checkbox]').iCheck('uncheck');
    });

    $scope.get_resolucion_id_list = function() {
        var resolucion_id_list = [];

        angular.element('table td input[type=checkbox]:checked').each(function(index) {
            resolucion_id_list[index] = $(this).attr('data-pk');
        });

        return resolucion_id_list;
    };

    $scope.aprobar_resoluciones = function() {
        var resolucion_id_list = $scope.get_resolucion_id_list();

        if (resolucion_id_list.length === 0) {
            alert('No ha seleccionado resolución alguna');
            return;
        }

        $.ajax({
            url: windowLocationOrigin + '/resoluciones/aprobar.json',
            method: 'PUT',
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", $cookies['csrftoken']);
            },
            data: {resolucion_id_list: JSON.stringify(resolucion_id_list)}
        }).success(function(data) {
            if (data.error == 0) {
                location.reload();

            } else {
                alert(data.msg);
            }
        });
    };

    $scope.rechazar_resoluciones = function() {
        var observaciones = angular.element('#observaciones').val().trim();
        var resolucion_id_list = $scope.get_resolucion_id_list();

        if (resolucion_id_list.length === 0) {
            alert('No ha seleccionado resolución alguna.');
            return;
        }

        if (!observaciones) {
            alert('No ha proporcionado observación alguna.');
            return;
        }

        $.ajax({
            url: windowLocationOrigin + '/resoluciones/rechazar.json',
            method: 'PUT',
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", $cookies['csrftoken']);
            },
            data: {
                observaciones: observaciones,
                resolucion_id_list: JSON.stringify(resolucion_id_list),
            }
        }).success(function(data) {
            if (data.error == 0) {
                location.reload();

            } else {
                alert(data.msg);
            }
        });
    };

}]);

coreApp.controller('CambioPerfilUsuarioCtrl',
    ['$scope', '$element', '$cookies', '$window', 'windowLocationOrigin', function($scope, $element, $cookies, $window, windowLocationOrigin) {

    $scope.solicitar_cambio = function() {
        $.ajax({
            url: windowLocationOrigin + '/registro/cambio-de-perfil/solicitar.json',
            method: 'POST',
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", $cookies['csrftoken']);
            },
        }).success(function(data) {
          if (data.error == 0) {
            angular.element('.msg').html('¡Su solicitud ha sido enviada con éxito!');
            $scope.go_home();

          } else {
            angular.element('.msg').html(data.msg);
          }
        });
    };

    $scope.cancelar_solicitud = function() {
        $.ajax({
            url: windowLocationOrigin + '/registro/cambio-de-perfil/cancelar.json',
            method: 'POST',
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", $cookies['csrftoken']);
            },
        }).success(function(data) {
          if (data.error == 0) {
            angular.element('.msg').html('¡Su solicitud ha sido cancelada con éxito!');
            $scope.go_home();

          } else {
            angular.element('.msg').html(data.msg);
          }
        });
    };

    $scope.go_home = function() {
      setTimeout(function() {
        window.location.reload();
      }, 2000);
    }

}]);

coreApp.controller('FuncionarioCambioPerfilUsuarioCtrl',
    ['$scope', '$element', '$cookies', '$window', 'windowLocationOrigin', function($scope, $element, $cookies, $window, windowLocationOrigin) {

    $scope.aprobar_solicitud = function(solicitud_pk) {
        $.ajax({
            url: windowLocationOrigin + '/registro/cambio-de-perfil/aprobar.json',
            method: 'PUT',
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", $cookies['csrftoken']);
            },
            data: {solicitud_pk: solicitud_pk}
        }).success(function(data) {
          window.location.reload();
        });
    };

    $scope.rechazar_solicitud = function(solicitud_pk) {
        angular.element('#cambio-perfil-observaciones-modal').modal('show');

        angular.element('#cambio-perfil-observaciones-modal').on('hidden.bs.modal', function() {
          angular.element('#observaciones').val('');
        });

        angular.element('#cambio-perfil-observaciones-modal .btn-primary').click(function() {
            var observaciones = angular.element('#observaciones').val();
            angular.element('#observaciones').modal('hide');

            $.ajax({
                url: windowLocationOrigin + '/registro/cambio-de-perfil/rechazar.json',
                method: 'PUT',
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", $cookies['csrftoken']);
                },
                data: {solicitud_pk: solicitud_pk, observaciones: observaciones}
            }).success(function(data) {
              window.location.reload();
            });

            angular.element('#cambio-perfil-observaciones-modal').modal('hide');
        })
    };

}]);

coreApp.controller('NuevaActaReparoCtrl',
    ['$scope', '$element', '$http', '$cookies', '$window', 'windowLocationOrigin', function($scope, $element, $http, $cookies, $window, windowLocationOrigin) {

    $scope.periodos = [];
    $scope.pst_rif = angular.element('#pst-rif').html();

    $scope.populatePeriodos = function(desde, hasta) {
      desde = moment(desde);
      hasta = moment(hasta);

      do {
        var new_index = $scope.periodos.length;

        $scope.periodos[new_index] = {
          periodo: desde.lang('es').format('MMMM-YYYY'),
        };

        $scope.handlePeriodo(new_index, desde);

        desde.add(1, 'month');
      } while (desde.month() < hasta.month());
    };

    $scope.handlePeriodo = function(index, periodo) {
      $http({
        url: windowLocationOrigin + '/declaraciones/declaraciones-periodo',
        method: "GET",
        params: {
          detailed: true,
          periodo: periodo.format('DD/MM/YYYY'),
          pst: $scope.pst_rif,
        }

      }).success(function (response, status) {
        var declaraciones = JSON.parse(response.result);
        var declaracion = declaraciones[declaraciones.length - 1];

        $scope.periodos[index].readonly = (declaracion == undefined);

        $scope.periodos[index].monto_pagado_segun_declaracion = Number(
          declaracion ? declaracion.fields.total_ventas_menos_anticipo : 0
        ).toFixed(2);

        $scope.periodos[index].ingresos_brutos = (
          $scope.periodos[index].monto_pagado_segun_declaracion
        );

        $scope.$watch('periodos[' + index + '].ingresos_brutos', function() {
          $scope.periodos[index].calculo_segun_fiscalizacion = (
            $scope.periodos[index].ingresos_brutos * 0.01
          ).toFixed(2);

          $scope.periodos[index].diferencia_por_pagar = (
            $scope.periodos[index].ingresos_brutos
            - $scope.periodos[index].monto_pagado_segun_declaracion
          ).toFixed(2);
        });

      }).error(function (response, status){
        $log.error('Error Status code:' + status + ' al consultar el servicio');
      });
    };

    $scope.guardarNuevaActaReparo = function() {
      var acta_fecha_notificacion = moment(
        angular.element('[name="acta-fecha-notificacion"]').val(), 'DD/MM/YYYY'
      ).format('YYYY-MM-DD');

      if (acta_fecha_notificacion == 'Invalid date') {
        alert('Debe indicar la fecha de notificación del acta de reparo');
        return;
      }

      var acta_atributos = [];

      for (var i = 0; i < $scope.periodos.length; i++) {
        acta_atributos[i] = $.extend(true, {}, $scope.periodos[i]);

        acta_atributos[i].periodo = convertir_periodo_str_date(
          acta_atributos[i].periodo
        ).format('YYYY-MM-DD');
      }

      $http({
        url: windowLocationOrigin + '/fiscalizacion/guardar_nueva_acta_reparo.json',
        method: "POST",
        dataType: "json",
        data: {
          acta_fecha_notificacion: acta_fecha_notificacion,
          acta_atributos: acta_atributos,
          fiscalizacion_pk: String(window.location).match(/^.*\/(\d+)\/.*$/)[1],
          csrfmiddlewaretoken: $cookies['csrftoken'],
        }

      }).success(function (response, status) {
        if (response.error != 0) {
          alert(response.msg);
        }

        $scope.concluir('fiscalizacion');

      }).error(function (response, status){
        $log.error('Error Status code:' + status + ' al consultar el servicio');
      });
    };

    // Legacy
    $scope.concluir = function(tipo) {
      $.ajax({
        url: windowLocationOrigin + '/' + tipo + '/concluir.json',
        method: 'PUT',
        beforeSend: function(xhr) {
          xhr.setRequestHeader("X-CSRFToken", get_cookie("csrftoken"));
        },
        data: {
          acta_id: String(window.location).match(/^.*\/(\d+)\/.*$/)[1],
        },
      }).success(function(data) {
        if (data.error == 0 || data.error == 1) {
          window.location = windowLocationOrigin + '/' + tipo + '/';

        } else if (data.error != 1) {
          alert(data.msg);
        }
      });
    };
}]);


coreApp.controller('EditarActaReparoCtrl',
    ['$scope', '$element', '$http', '$cookies', '$window', 'windowLocationOrigin', function($scope, $element, $http, $cookies, $window, windowLocationOrigin) {

    $scope.populateActa = function(fiscalizacion_pk) {
      $http({
        url: windowLocationOrigin + '/fiscalizacion/obtener_acta_reparo.json',
        method: "GET",
        params: {fiscalizacion_pk: fiscalizacion_pk}
      }).success(function (response, status) {
        $scope.acta = JSON.parse(response.result.acta_list)[0];
        $scope.acta.atributo_list = JSON.parse(response.result.acta_atributo_list);

        $scope.acta.fields.fecha_notificacion = moment(
          $scope.acta.fields.fecha_notificacion
        ).format('DD/MM/YYYY');

        for (var index = 0; index < $scope.acta.atributo_list.length; index++) {
          $scope.handleActaAtributo(index);
        }

      }).error(function (response, status){
        $log.error('Error Status code:' + status + ' al consultar el servicio');
      });

      setTimeout(function() {
        angular.element('.decimal-mask').inputmask(
          '9[9][9][9][9][9][9][.9[9]]', {placeholder: '', showMaskOnHover: false}
        );
      }, 1000);
    };

    $scope.handleActaAtributo = function(index) {
      $scope.acta.atributo_list[index].fields.periodo = moment(
        $scope.acta.atributo_list[index].fields.periodo
      ).lang('es').format('MMMM-YYYY')

      $scope.$watch('acta.atributo_list[' + index + '].fields.ingresos_brutos', function() {
        $scope.acta.atributo_list[index].fields.calculo_segun_fiscalizacion = (
          $scope.acta.atributo_list[index].fields.ingresos_brutos * 0.01
        ).toFixed(2);

        $scope.acta.atributo_list[index].fields.diferencia_por_pagar = (
          $scope.acta.atributo_list[index].fields.ingresos_brutos
          - $scope.acta.atributo_list[index].fields.monto_pagado_segun_declaracion
        ).toFixed(2);
      });
    }

    $scope.guardarActaReparo = function() {
      var acta = $.extend(true, {}, $scope.acta);

      acta.fields.fecha_notificacion = moment(
        acta.fields.fecha_notificacion, 'DD/MM/YYYY'
      ).format('YYYY-MM-DD');

      if (acta.fields.fecha_notificacion == 'Invalid date') {
        alert('Debe indicar la fecha de notificación del acta de reparo');
        return;
      }

      for (var i = 0; i < acta.atributo_list.length; i++) {
        delete acta.atributo_list[i].fields.periodo
      }

      $.ajax({
        url: windowLocationOrigin + '/fiscalizacion/guardar_acta_reparo.json',
        method: 'PUT',
        beforeSend: function(xhr) {
          xhr.setRequestHeader("X-CSRFToken", get_cookie("csrftoken"));
        },
        data: {
          acta: acta,
          csrfmiddlewaretoken: $cookies['csrftoken'],
        }
      }).success(function(data) {
        if (data.error == 0) {
          angular.element('#editar-acta-reparo-modal').modal('hide');
          alert('Sus cambios han sido guardados exitosamente');

        } else {
          alert(data.msg);
        }
      });
    };
}]);


coreApp.controller('AprobacionActaReparoCtrl',
    ['$scope', '$element', '$cookies', 'windowLocationOrigin', function($scope, $element, $cookies, windowLocationOrigin) {

    $scope.solicitar = function($event, acta_pk) {
      $event.preventDefault();

      $.ajax({
        url: windowLocationOrigin + '/fiscalizacion/actas/solicitar-aprobacion.json',
        method: 'PUT',
        beforeSend: function(xhr) {
          xhr.setRequestHeader("X-CSRFToken", get_cookie("csrftoken"));
        },
        data: {acta_pk: acta_pk},
      }).success(function(data) {
        if (data.error == 0) {
          $(
            '[data-pk="' + acta_pk + '"] td:nth-of-type(4) small'
          ).text('Aprobación solicitada');

          $(
            '[data-pk="' + acta_pk + '"] td:nth-of-type(5) div:nth-of-type(4)'
          ).hide();

        } else {
          alert(data.msg);
        }
      });
    };
}]);
