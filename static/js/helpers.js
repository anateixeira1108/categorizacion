$('.anular-button').click(function () {
    $('#declaracion-id').val($(this).attr('dec-id'));
});

$('.modal').on('hidden.bs.modal', function () {
    //$(this).find('form')[0].reset();
});


/**
 * Controlador utilizado para mostrar la pregunta especificada al momento de certificar documentos
 * para un pst juridico.
 */
coreApp.controller(
    'registroConclusionesCtrl',
    [
        '$scope', '$log',
        function ($scope, $log) {
            var riftur_option = angular.element('#riftur_option');
            riftur_option.hide();//por defecto se oculta la pregunta sobre generar riftur
            //agrega la respuesta "si" por defecto al localstorage
            localStorage['mintur_pregunta'] = "si";
            $scope.verificar_opcion = function (option) {
                //se verifica si la opcion es otros para mostrar el combo de respuestas
                if (option === 'otros') {
                    riftur_option.show();
                } else {
                    riftur_option.hide();
                }
                console.log(localStorage);
            };
            $scope.ingresar_conclusiones = function () {
                var ingresar_conclusiones = angular.element('#ingresar_conclusiones');
                var registrar_conclusiones = angular.element('#registrar_conclusiones');
                registrar_conclusiones.modal('hide');
                ingresar_conclusiones.modal('show');
            };

            $scope.actualizar_respuesta = function (option) {
                localStorage['mintur_pregunta'] = option;
                console.log(localStorage);
            };

        }
    ]
);


/**
 * Controlador utilizado para validar los documentos en certificacion para pst juridico
 */
coreApp.controller(
    'ValidarJuridicoCtrl',
    [
        '$scope', '$controller',
        function ($scope) {
            $scope.respuesta = localStorage['mintur_pregunta'];
            /**
             * Se configura el evento de selección de todos los documentos
             */
            var ele = angular.element("[name='todos']");
            var items = angular.element("[name='documento[]']");

            ele.on('ifChecked', function () {
                items.iCheck('check')
            });

            ele.on('ifUnchecked', function () {
                items.iCheck('uncheck');
            });

            items.on('ifChecked', function () {
                var is_all_checked = true;

                items.each(function (index, value) {
                    if (!$(this).prop('checked')) {
                        is_all_checked = false;
                    }
                });

                if (is_all_checked) {
                    ele.iCheck('check');
                }
            });

            items.on('ifUnchecked', function () {
                ele.off('ifUnchecked');

                ele.iCheck('uncheck');

                ele.on('ifUnchecked', function () {
                    items.iCheck('uncheck');
                });
            });

            //se obtienen la lista de checkbox a validar
            $scope.lista = angular.element('.validar');

            /**
             * Función a heredar para verificar si seleccionaron todos los checkbox
             * @returns {boolean}
             */
            $scope.es_valido = function () {
                //se obtiene el numero de checkboxex visibles
                var checkboxes_visibles = $scope.lista
                    .filter(function (index, value) {
                        return angular.element(value).is(':visible');
                    });
                //se obtiene el numero de checkboxex checkeados(True)
                var checkboxes_trues = $scope.lista
                    .filter(function (index, value) {
                        return angular.element(value).is(':checked');
                    });
                //se obtienen los checkboxes que son visibles pero no han sido checkeados
                var diff = angular.element(checkboxes_visibles).not(checkboxes_trues).get();
                /**
                 * se crea una lista con los nombres de documentos que faltan
                 * por checkquear para mostrar en el modal
                 */
                $scope.nombres_de_documentos = _.map(diff, function (num) {
                    return angular.element(num).data('nombre');
                });
                /**
                 * Se verifica si el numero de checkboxes visibles es igual al
                 * numero de checkboxes checkeadas
                 */
                return checkboxes_visibles.size() == checkboxes_trues.size();
            };

            /**
             * Se valida si se seleccionaron todos los documentos
             */
            $scope.validar = function () {
                if ($scope.es_valido()) {
                    //angular.element('#pregunta-modal').modal('show');
                    angular.element('#certification-modal').modal('show');
                } else {
                    angular.element('#rechazar_solicitud').modal('show');
                }
            };
        }
    ]
);

/**
 * Controlador utilizado para validar los documentos en certificacion para un pst natural
 */
coreApp.controller(
    'ValidarNaturalCtrl',
    [
        '$scope',
        '$controller',
        '$cookieStore',
        function ($scope, $controller) {
            console.log("ValidarNaturalCtrl");
            $scope.respuesta = localStorage['pregunta'];
            /**
             * Se extiende el controlador
             */
            $.extend(this,
                $controller(
                    'ValidarJuridicoCtrl',
                    {$scope: $scope}
                )
            );


            /**
             * Se valida si se seleccionaron todos los documentos
             */
            $scope.validar = function () {
                if ($scope.es_valido()) {
                    angular.element('#certification-modal').modal('show');
                } else {
                    angular.element('#rechazar_solicitud').modal('show');
                }
            };
        }
    ]
);


/**
 * Servicio utilizado para configurar datos especificos del modulo verificacion
 */
coreApp.service('VerificacionUrlService', function () {
    this.url_codigo = "/verificacion/get/codigo/ajax/";
    this.url_data = "/verificacion/get/data/ajax/";
});

/**
 * Servicio utilizado para configurar datos especificos del modulo fiscalizacion
 */
coreApp.service('FiscalizacionUrlService', function () {
    this.url_codigo = "/fiscalizacion/get/codigo/ajax/";
    this.url_data = "/fiscalizacion/get/data/ajax/";
});


/**
 * Servicio utilizado para realizar las operaciones de forma generica (Fiscalizacion y Verificacion)
 */
coreApp.service('OperacionesService', ['$cookies',
    function ($cookies) {
        /**
         * Variable utilizada para retornar los datos correspondientes a cada accion
         * @type {{}}
         */
        var $_scope = {};


        this.anular_providencia = function (codigo_providencia) {
            console.log("Codigo de providencia: ", codigo_providencia)
            $_scope.codigo_providencia = codigo_providencia;
            return $_scope;
        }

        /**
         * Funcion agregar para consultar los datos que se van a cargar el modal de creacion de acta
         * @param url
         * @param item
         * @returns {{}}
         */
        this.agregar = function (url, item) {
            var codigo_objeto = angular.element('#codigo_objeto').data('codigo');
            var request = $.ajax({
                method: "POST",
                url: url,
                async: false,
                data: {
                    'tipo_acta': item,
                    'codigo_objeto': codigo_objeto,
                    'csrfmiddlewaretoken': $cookies['csrftoken']
                }
            });
            request.success(function (data, status, headers, config) {
                console.log("Exito", status);
                if (data.success) {
                    $_scope.valido = true;
                    $_scope.codigo = data.data.codigo;
                    $_scope.codigo_tipo_acta = data.data.codigo_tipo_acta;
                    $_scope.tipo_acta = data.data.tipo_acta;
                    console.log(data.data.tipo_acta, $_scope.tipo_acta);
                    if (data.data.tiene_requisitos) {
                        $_scope.tiene_requisitos = true;
                        $_scope.requisitos = data.data.requisitos;
                        $_scope.solo_lista = $_scope.tipo_acta === "Acta de requerimiento cerrada";
                    } else {
                        //se verifica si es una cedula de hallazgo
                        $_scope.es_una_cedula_de_hallazgo = $_scope.codigo_tipo_acta == 'CH';
                        $_scope.tiene_requisitos = false;
                        $_scope.requisitos = []
                    }
                } else {
                    alert("" + data.data.msn);
                    $_scope.valido = false;
                    $_scope.codigo = "";
                    $_scope.tipo_acta = "";
                }
            });
            request.error(function (data, status, headers, config) {
                console.log("Error", status);
                $_scope.valido = false;
                $_scope.codigo = "";
                $_scope.tipo_acta = "";
            });

            return $_scope;
        };

        /**
         * Funcion editar para consultar los datos que se van a cargar el modal de edicion de acta
         * @param url
         * @param index
         * @returns {{}}
         */
        this.editar = function (url, index) {
            var $_scope = {};
            var codigo_objeto = angular.element('#codigo_objeto').data('codigo');
            var datos = angular.element("#" + index);
            var codigo = datos.data('codigo');
            var tipo = datos.data('tipo');
            var request = $.ajax({
                method: "post",
                url: url,
                async: false,
                data: {
                    'tipo_acta': tipo,
                    'codigo_acta': codigo,
                    'codigo_objeto': codigo_objeto,
                    'csrfmiddlewaretoken': $cookies['csrftoken']
                }
            });
            request.success(function (data, status, headers, config) {
                if (data.success) {
                    console.log("Exito", status);
                    $_scope.observaciones_editar = data.data.observaciones;
                    $_scope.fecha_notificacion_editar = data.data.fecha_notificacion;
                    $_scope.codigo_tipo_acta = data.data.codigo_tipo_acta;
                    console.log(data.data.tipo_acta, $_scope.tipo_acta);
                    if (data.data.tiene_requisitos) {
                        $_scope.tiene_requisitos = true;
                        $_scope.requisitos = data.data.requisitos;
                        $_scope.solo_lista = $_scope.tipo_acta === "Acta de requerimiento cerrada";
                        angular.element('#editar_acta_requisitos').modal('show')
                    } else {
                        $_scope.es_una_cedula_de_hallazgo = $_scope.codigo_tipo_acta == 'CH';
                        if ($_scope.es_una_cedula_de_hallazgo) {
                            $_scope.hallazgos_condicion = data.data.hallazgos_condicion;
                            $_scope.hallazgos_criterio = data.data.hallazgos_criterio;
                            $_scope.hallazgos_efecto = data.data.hallazgos_efecto;
                            $_scope.hallazgos_evidencia = data.data.hallazgos_evidencia;
                            $_scope.hallazgos_materia = data.data.hallazgos_materia;
                        }
                        $_scope.tiene_requisitos = false;
                        $_scope.requisitos = [];
                        angular.element('#editar_acta').modal('show')
                    }
                }

            });
            request.error(function (data, status, headers, config) {
                console.log("Error", status);
                $_scope.observaciones_editar = "";
                $_scope.fecha_notificacion_editar = "";
            });
            $_scope.codigo_editar = codigo;
            $_scope.tipo_editar = tipo;
            return $_scope;
        };

        /**
         * Funcion ver para consultar los datos que se van a cargar el modal de ver acta
         * @param url
         * @param index
         * @returns {{}}
         */
        this.ver = function (url, index) {
            var codigo_objeto = angular.element('#codigo_objeto').data('codigo');
            var datos = angular.element("#" + index);
            var codigo = datos.data('codigo');
            var tipo = datos.data('tipo');
            var $_scope = {};
            $_scope.codigo_ver = codigo;
            $_scope.tipo_ver = tipo;

            var request = $.ajax({
                method: "post",
                url: url,
                async: false,
                data: {
                    'tipo_acta': tipo,
                    'codigo_acta': codigo,
                    'codigo_objeto': codigo_objeto,
                    'csrfmiddlewaretoken': $cookies['csrftoken']
                }
            });
            request.success(function (data, status, headers, config) {
                if (data.success) {
                    console.log("Exito", status);
                    $_scope.observaciones_ver = data.data.observaciones;
                    $_scope.fecha_notificacion_ver = data.data.fecha_notificacion;
                    $_scope.codigo_tipo_acta = data.data.codigo_tipo_acta;
                    if (data.data.tiene_requisitos) {
                        $_scope.tiene_requisitos = true;
                        $_scope.requisitos = data.data.requisitos;
                        $_scope.solo_lista = $_scope.tipo_acta === "Acta de requerimiento cerrada";
                        angular.element('#ver_acta_requisitos').modal('show')
                    } else {
                        $_scope.es_una_cedula_de_hallazgo = $_scope.codigo_tipo_acta == 'CH';
                        if ($_scope.es_una_cedula_de_hallazgo) {
                            $_scope.hallazgos_condicion = data.data.hallazgos_condicion;
                            $_scope.hallazgos_criterio = data.data.hallazgos_criterio;
                            $_scope.hallazgos_efecto = data.data.hallazgos_efecto;
                            $_scope.hallazgos_evidencia = data.data.hallazgos_evidencia;
                            $_scope.hallazgos_materia = data.data.hallazgos_materia;
                        }
                        $_scope.tiene_requisitos = false;
                        $_scope.requisitos = [];
                        angular.element('#ver_acta').modal('show')
                    }
                }

            });
            request.error(function (data, status, headers, config) {
                console.log("Error", status);
                $_scope.observaciones_ver = "";
                $_scope.fecha_notificacion_ver = "";
            });
            return $_scope;
        }
    }
]);

/**
 * Servicio utilizado para especificar las operaciones a realizar en fiscalizacion
 * con su correspondiente configuracion
 */
coreApp.service('OperacionesFiscalizacionService',
    function (OperacionesService, FiscalizacionUrlService) {

        this.agregar = function (item) {
            console.log('agregar');
            return OperacionesService.agregar(FiscalizacionUrlService.url_codigo, item);
        };

        this.editar = function (index) {
            console.log('editar');
            return OperacionesService.editar(FiscalizacionUrlService.url_data, index);
        };

        this.ver = function (index) {
            console.log('ver');
            return OperacionesService.ver(FiscalizacionUrlService.url_data, index);
        };

        this.anular_providencia = function (codigo_providencia) {
            console.log('anular providencia');
            return OperacionesService.anular_providencia(codigo_providencia);
        };
    }
);


/**
 * Servicio utilizado para especificar las operaciones a realizar en verificacion
 * con su correspondiente configuracion
 */
coreApp.service('OperacionesVerificacionService',
    function (OperacionesService, VerificacionUrlService) {

        this.agregar = function (item) {
            console.log('agregar');
            return OperacionesService.agregar(VerificacionUrlService.url_codigo, item);
        };

        this.editar = function (index) {
            console.log('editar');
            return OperacionesService.editar(VerificacionUrlService.url_data, index);
        };

        this.ver = function (index) {
            console.log('ver');
            return OperacionesService.ver(VerificacionUrlService.url_data, index);
        };

        this.anular_providencia = function (codigo_providencia) {
            console.log('anular providencia');
            return OperacionesService.anular_providencia(codigo_providencia);
        };
    }
);


/**
 * Controlador mixin, contiene funciones comunes para los controladores de
 * verificacion y fiscalizacion, cuya funcion es agregar los datos procesados
 * al scope
 */
coreApp.controller('AddDataToScopeCtrl', [
        '$scope',
        function ($scope) {
            $scope.anular_providencia_put_data_to_scope = function ($data) {
                //datos del acta
                $scope.codigo_providencia = $data.codigo_providencia;
            };
            $scope.agregar_put_data_to_scope = function ($data) {
                //datos del acta
                $scope.valido = $data.valido;
                $scope.codigo = $data.codigo;
                $scope.tipo_acta = $data.tipo_acta;
                $scope.es_una_cedula_de_hallazgo = $data.es_una_cedula_de_hallazgo;
                $scope.filtro_put_data_to_scope();
            };
            $scope.editar_put_data_to_scope = function ($data) {
                //datos del acta
                $scope.codigo_editar = $data.codigo_editar;
                $scope.tipo_editar = $data.tipo_editar;
                $scope.observaciones_editar = $data.observaciones_editar;
                $scope.fecha_notificacion_editar = $data.fecha_notificacion_editar;
                $scope.es_una_cedula_de_hallazgo = $data.es_una_cedula_de_hallazgo;
                if ($scope.es_una_cedula_de_hallazgo) {
                    $scope.hallazgos_condicion = $data.hallazgos_condicion;
                    $scope.hallazgos_criterio = $data.hallazgos_criterio;
                    $scope.hallazgos_efecto = $data.hallazgos_efecto;
                    $scope.hallazgos_evidencia = $data.hallazgos_evidencia;
                    $scope.hallazgos_materia = $data.hallazgos_materia;
                }
                $scope.filtro_put_data_to_scope();
            };
            $scope.ver_put_data_to_scope = function ($data) {
                //datos del acta
                $scope.codigo_ver = $data.codigo_ver;
                $scope.tipo_ver = $data.tipo_ver;
                $scope.observaciones_ver = $data.observaciones_ver;
                $scope.fecha_notificacion_ver = $data.fecha_notificacion_ver;
                $scope.es_una_cedula_de_hallazgo = $data.es_una_cedula_de_hallazgo;
                if ($scope.es_una_cedula_de_hallazgo) {
                    $scope.hallazgos_condicion = $data.hallazgos_condicion;
                    $scope.hallazgos_criterio = $data.hallazgos_criterio;
                    $scope.hallazgos_efecto = $data.hallazgos_efecto;
                    $scope.hallazgos_evidencia = $data.hallazgos_evidencia;
                    $scope.hallazgos_materia = $data.hallazgos_materia;
                }
                $scope.filtro_put_data_to_scope();
            };
            $scope.filtro_put_data_to_scope = function () {
                //datos para filtrar tipos de actas
                /**
                 * Variable utilizada para verificar si el acta tiene requisitos
                 * @type {boolean|*}
                 */
                $scope.tiene_requisitos = $data.tiene_requisitos;
                /**
                 * Lista de requisitos, en caso de tenerlos
                 * @type {list|*}
                 */
                $scope.requisitos = $data.requisitos;
                /**
                 * Variable utilizada para verificar si los requisitos se muestran en forma de lista
                 * o en forma de checkbox
                 * @type {boolean|*}
                 */
                $scope.solo_lista = $data.solo_lista;
            };
        }
    ]
);

/**
 * Controlador utilizado para las acciones a realizar en
 * el modulo de verificacion
 * template: templates/verificacion/funcionario/verificacion.html
 */
coreApp.controller(
    'VerificacionCtrl',
    [
        '$scope',
        '$controller',
        'OperacionesVerificacionService',
        '$log',
        function ($scope, $controller, OperacionesVerificacionService, $log) {
            /**
             * Se extiende el controlador que tiene las funciones
             * para agregar datos al scope
             */
            $.extend(this,
                $controller(
                    'AddDataToScopeCtrl',
                    {$scope: $scope}
                )
            );

            $scope.agregar = function (item) {
                $data = OperacionesVerificacionService.agregar(item);
                $scope.agregar_put_data_to_scope($data);
            };

            $scope.editar = function (index) {
                $data = OperacionesVerificacionService.editar(index);
                $scope.editar_put_data_to_scope($data);
            };

            $scope.ver = function (index) {
                $data = OperacionesVerificacionService.ver(index);
                $scope.ver_put_data_to_scope($data);
            };

            $scope.anular_providencia = function (codigo_providencia) {
                $data = OperacionesVerificacionService.anular_providencia(codigo_providencia);
                $scope.anular_providencia_put_data_to_scope($data);
            };

        }
    ]
);
/**
 * Controlador utilizado para las acciones a realizar en
 * el modulo de fiscalizacion
 * template: templates/fiscalizacion/funcionario/fiscalizacion.html
 */
coreApp.controller(
    'FiscalizacionCtrl',
    [
        '$scope',
        '$controller',
        'OperacionesFiscalizacionService',
        '$log',
        function ($scope, $controller, OperacionesFiscalizacionService, $log) {
            /**
             * Se extiende el controlador que tiene las funciones
             * para agregar datos al scope
             */
            $.extend(this,
                $controller(
                    'AddDataToScopeCtrl',
                    {$scope: $scope}
                )
            );

            $scope.agregar = function (item) {
                $data = OperacionesFiscalizacionService.agregar(item);
                $scope.agregar_put_data_to_scope($data);
            };

            $scope.editar = function (index) {
                $data = OperacionesFiscalizacionService.editar(index);
                $scope.editar_put_data_to_scope($data);
            };

            $scope.ver = function (index) {
                $data = OperacionesFiscalizacionService.ver(index);
                $scope.ver_put_data_to_scope($data);
            };

            $scope.anular_providencia = function (codigo_providencia) {
                $data = OperacionesFiscalizacionService.anular_providencia(codigo_providencia);
                $scope.anular_providencia_put_data_to_scope($data);
            };
        }
    ]
);

