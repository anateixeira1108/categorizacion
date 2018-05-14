// Jquery ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
$(function() {
    // Some browsers (mainly IE) does not have this property, so we need to build it manually...
    if (!window.location.origin) {
      window.location.origin = (
        window.location.protocol
        + '//'
        + window.location.hostname
        + (window.location.port ? (':' + window.location.port) : '')
      );
    }

    // Gestionar los enlaces a documentos subidos
    $.each($('a[href*="/documents/"]'), function() {
        var $el = $(this);

        // Remover ruta del documento del html del link {
        var html_math = $el.html().match(/^(.+)( .*)?$/);
        if (!html_math) { return; }

        var path = html_math[1];
        var filename_start_index = path.lastIndexOf('/') + 1;
        var filename = path.slice(filename_start_index);
        var match = filename.match(/^(.+)(_\d+)(\..+)$/);
        var clean_filename = (match && match.length == 4) ? match[1] + match[3] : filename;
        $el.html(clean_filename + (html_math[2] ? html_math[2] : ''));
        // }

        // Obligar la apertura del link en una nueva pestaña {
        $el.prop('target', '_bank');
        // }
    });

    // Cambiar HTML de la opción vacía en todos los selects de la vida
    $('select option[value=""]').html('-- Seleccione --');

    // Activar datepickers
    $('.date').datepicker({
      autoclose: true,
      clearBtn: true,
      language: "es",
      startView: 1,
    });
    $('.date input').unbind('focus');

    // Custom mask
    $.extend($.inputmask.defaults.definitions, {
        'R': {
            'validator': '[jvJV]',
            'cardinality': 1,
            'casing': 'upper',
            'prevalidator': null
        },
        'r': {
            'validator': '[jgvepJGVEP]',
            'cardinality': 1,
            'casing': 'upper',
            'prevalidator': null
        },
        'c': {
            'validator': '[veVE]',
            'cardinality': 1,
            'casing': 'upper',
            'prevalidator': null
        },
        't': {
            'validator': '[a-zA-Z0-9\\-]',
            'cardinality': 1,
            'casing': 'upper',
            'prevalidator': null
        },
    });

    // Mascaras de vistas
    $('.anios-mask').inputmask('9[9][9]', {placeholder: ''});
    $('.date-mask').inputmask('dd/mm/yyyy', {placeholder: '', onBeforeMask: function(value) {
      return ($(this).attr('value') || value).trim();
    }});
    $('.decimal-mask').inputmask('9[9][9][9][9][9][9][.9[9]]', {placeholder: '', showMaskOnHover: false});
    $('.float-mask').inputmask('9[9][9][9][9][9][9][9][9][.9[9]]', {placeholder: '', showMaskOnHover: false});
    $('.iddoc-mask').inputmask('c-999999[9][9]', {placeholder: ''});
    $('.license-mask').inputmask('9[9][9][9][9][9]', {placeholder: '', showMaskOnHover: false});
    $('.rif-mask').inputmask('r-999999[9][9]-9', {placeholder: ''});
    $('.rif-strict-mask').inputmask('R-999999[9][9]-9', {placeholder: ''});
    $('.stack-mask').inputmask('9[9][9][9][9][9][9][9]', {placeholder: ''});
    $('.sunacoop-mask').inputmask('9[9][9][9][9][9][9]', {placeholder: ''});
    $('.tlf-mask').inputmask('9999-9999999');
    $('.tome-mask').inputmask('t[t][t][t][t][t]', {placeholder: ''});
    $('.tome-number-mask').inputmask('9[9][9][9][9][9][9][9]', {placeholder: ''});
    $('.zip-mask').inputmask('9999', {placeholder: ''});

    // Modal Window de concepto de pagos
    concepto_pago_modal_handler();

    // Modal Window de Resoluciones
    resoluciones_modal_handler();

    // Select de tipo de solicitudes en la vista de certificación de registros
    tipo_solicitudes_select_handler();

    // Aplicar formato a la clase 'currency'
    $('.currency').each(function(index, element) {
      var $element = $(element);
      var attr = ($element.is('input') ? 'val' : 'html');

      $element[attr](
        currencyFormatDE(Number($element[attr]().replace(',', '.')))
      )
    });
});
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


// Constantes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
var MESES = {
    Enero: '01', Febrero: '02', Marzo: '03', Abril: '04', Mayo: '05', Junio: '06',
    Julio: '07', Agosto: '08', Septiembre: '09', Octubre: '10', Noviembre: '11', Diciembre: '12'
};
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


// Funciones ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function concepto_pago_modal_handler() {
    // Modal Window de Compromisos de Pago
    $('#conceptos a[data-id!=""]').click(function() {
        var $modal = $('#conceptos-modal');

        $.ajax({
            url: window.location.origin + '/pagos/compromisos/de/pago.json/',
            method: 'GET',
            data: {
                concepto_id: $(this).attr('data-id')
            }
        }).success(function(data) {
            if (data.error == 0) {
                var fields = JSON.parse(data.result)[0].fields;

                $modal.find('#tipo').html(
                    data.attached.tipo
                );
                $modal.find('#fecha-generacion').html(
                    moment(fields.fecha_generacion).lang('es').format('DD [de] MMMM [de] YYYY [a las] hh:mm')
                );
                $modal.find('#monto').html(
                    currencyFormatDE(Number(fields.monto))
                );
                $modal.find('#estatus').html(
                    fields.estatus
                );
                $modal.find('#pago').html(
                    data.attached.pago ? data.attached.pago.numero_documento : 'No disponible'
                );

                if (data.attached.pago) {
                    $modal.find('#pago-url').attr(
                        'href', window.location.origin + '/pagos/compromisos/de/pago/pdf/' + data.attached.pago.id
                    ).show();

                } else {
                    $modal.find('#pago-url').hide();
                }

                $modal.modal('show');
            }
        });
    });

    // Generar Compromiso de Pago
    $('#generar-compromiso-pago').click(function() {
        var concepto_id_list = [];

        $('#conceptos input[name="concepto"]:checked').each(function(index) {
            concepto_id_list[index] = $(this).attr('data-pk');
        });

        if (concepto_id_list.length == 0) {
            alert('Debe seleccionar al menos un concepto de pago.');
            return;
        }

        $.ajax({
            url: window.location.origin + '/pagos/compromisos/de/pago/nuevo/',
            method: 'POST',
            data: {
                conceptos: JSON.stringify(concepto_id_list),
                csrfmiddlewaretoken: get_cookie('csrftoken'),
            }
        }).success(function(data) {
            if (data.error == 0) {
                var pago = JSON.parse(data.result)[0];

                window.location = (
                    window.location.origin + '/pagos/compromisos/de/pago/pdf/' + pago.pk
                );

                $('#conceptos input[name="concepto"]:checked').each(function() {
                    var $this = $(this);

                    $this.parents('tr').find('.pago-nro').html(pago.fields.numero_documento);

                    $this.parents('tr').find('.pago-url').attr(
                        'href', window.location.origin + '/pagos/compromisos/de/pago/pdf/' + pago.pk
                    ).show();

                    $this.iCheck('uncheck').iCheck('disable');
                })

            } else {
                alert(data.msg);
            }
        });
    });
}


function resoluciones_modal_handler() {
    // + Global cfg +++++++
    var global_all_ok = true;

    // + Eventos ++++++++++
    $('#verificacion-observaciones-modal .btn-primary').click(function() {
        registrar_observaciones('verificacion');
    });

    $('#fiscalizacion-conclusion-observaciones-modal .btn-primary').click(function() {
        registrar_observaciones('fiscalizacion');
    });

    $('.resolucion .borrar').click(function() {
        var status = $(this).parents('tr').find('.badge').html();

        if (status === 'Aprobada') {
          alert('La eliminación de esta resolución no es permitida.');
          return;
        }

        eliminar_resolucion($(this));
    });

    $('.resolucion .editar').click(function() {
        var resolucion_id = $(this).attr('data-pk');
        var $modal = $('#resoluciones-edit-modal').attr('data-pk', resolucion_id);
        var status = $(this).parents('tr').find('.badge').html();

        if (status === 'Aprobación Solicitada' || status === 'Aprobada') {
          alert('La edición de esta resolución no es permitida.');
          return;
        }

        obtener_ilicitos($modal.modal('show'), resolucion_id);
    });

    $('.resolucion .solicitar-aprobacion').click(function() {
        var status = $(this).parents('tr').find('.badge').html();

        if (status === 'Aprobada') {
          alert('Esta resolución ya ha sido aprobada.');
          return;
        }

        solicitar_aprobacion($(this));
    });

    $('.resoluciones-modal').on('hidden.bs.modal', function() {
        var $this = $(this);

        $this.find('.buscar-sancion').val('');
        $this.find('.ilicitos').html('');
        $this.find('.sanciones').html('');
    });

    $('.resoluciones-modal .buscar-sancion-btn').click(function() {
        var $modal = $(this).parents('.resoluciones-modal');

        buscar_sancion($modal, $modal.find('.buscar-sancion').val());
    });

    $('.resoluciones-modal .buscar-sancion').keypress(function(event) {
        var $this = $(this);
        var $modal = $this.parents('.resoluciones-modal');

        setTimeout(function() {
            if (event.keyCode == 13) {
                buscar_sancion($modal, $this.val());
            }
        }, 500);
    });

    $('.resoluciones-modal .agregar-sancion-btn').click(function() {
        var $modal = $(this).parents('.resoluciones-modal');
        var $ilicitos = $modal.find('.ilicitos');
        var sancion_codigo = $modal.find('.sanciones option:selected').val();
        var template = _.template($('#ilicito-template').html());
        var in_edit_mode = ($modal.find('table thead th').length == 6);

        if (!sancion_codigo) return;

        $ilicitos.append(_handle_ilicito(
            $(template({sancion_codigo: sancion_codigo, edit: in_edit_mode}))
        ));
    });

    $('#resoluciones-modal .guardar-btn').click(function() {
        guardar_nueva_resolucion($('#resoluciones-modal'));
    });

    $('#resoluciones-edit-modal .guardar-btn').click(function() {
        var $modal = $('#resoluciones-edit-modal');
        var resolucion_id = $modal.attr('data-pk');

        global_all_ok = true;
        eliminar_ilicitos($modal, resolucion_id);
        cambiar_ilicitos($modal, resolucion_id);
        agregar_ilicitos($modal, resolucion_id);

        setTimeout(function() {
            if (global_all_ok) {
                $modal.modal('hide');
            }
        }, 1500);
    });

    // + Funciones ++++++++
    function buscar_sancion($modal, query) {
        if (!query) {
            alert('Debe indicar los términos de búsqueda.');
            return;
        }

        $.ajax({
            url: window.location.origin + '/resoluciones/buscar_sancion.json',
            method: 'GET',
            data: {query: query}
        }).success(function(data) {
            if (data.error == 0) {
                var $select = $modal.find('.sanciones').html('');
                var sanciones = JSON.parse(data.result);
                var template = _.template($('#sancion-template').html());

                if (sanciones.length == 0) {
                    alert('La búsqueda no arrojó resultados.');
                    return;
                }

                for (var i = 0; i < sanciones.length; i++) {
                    $select.append(template({
                        value: sanciones[i].fields.codigo,
                        desc: '[' + sanciones[i].fields.codigo + ']' + ' ' + _parse_descripcion(sanciones[i].fields.descripcion)
                    }));
                }
            }
        });
    }

    function agregar_ilicitos($modal, resolucion_id) {
        var $ilicitos = $modal.find('.ilicitos');
        var $new_ilicitos = $ilicitos.find('.ilicito:not([data-pk])');
        var ilicito_obj_list = [];

        $new_ilicitos.each(function(index, ilicito) {
            var $ilicito = $(ilicito);

            ilicito_obj_list[index] = {
                sancion_codigo: $ilicito.find('.sancion_codigo').html(),
                periodo: _parse_date($ilicito.find('.periodo input').val()),
                fecha_limite: $ilicito.find('.fecha-limite input').val(),
                declaracion_id: $ilicito.find('.declaraciones select option:selected').val() || '',
            }
        });

        $.ajax({
            url: window.location.origin + '/resoluciones/ilicito.json',
            method: 'POST',
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", get_cookie("csrftoken"));
            },
            data: {
                resolucion_id: resolucion_id,
                ilicito_list: JSON.stringify(ilicito_obj_list),
            }
        }).success(function(data) {
            if (data.error != 0) {
                global_all_ok = false;
                alert(data.msg);

            } else {
                $new_ilicitos.attr('data-pk', 'null');
            }
        });
    }

    function cambiar_ilicitos($modal, resolucion_id) {
        var $ilicitos = $modal.find('.ilicitos');
        var $changed_ilicitos = $ilicitos.find('.ilicito.changed');
        var ilicito_obj_list = [];

        $changed_ilicitos.each(function(index, ilicito) {
            var $this = $(ilicito).removeClass('has-errors');
            var $input = $this.find('.sancion-ut input');

            if (!(+$input.attr('data-ut-min') <= +$input.val() && +$input.val() <= +$input.attr('data-ut-max'))) {
                $this.addClass('has-errors');
            }

            ilicito_obj_list[index] = {
                pk: $(this).attr('data-pk'),
                sancion_ut: $input.val(),
            }
        });

        if ($ilicitos.find('.ilicito.has-errors').length > 0) {
            global_all_ok = false;
            alert('Algunas sanciones están fuera del rango establecido.')
            return;
        }

        $.ajax({
            url: window.location.origin + '/resoluciones/ilicito.json',
            method: 'PUT',
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", get_cookie("csrftoken"));
            },
            data: {
                resolucion_id: resolucion_id,
                ilicito_obj_list: JSON.stringify(ilicito_obj_list),
            }
        }).success(function(data) {
            if (data.error != 0) {
                global_all_ok = false;
                alert(data.msg);

            } else {
                $changed_ilicitos.removeClass('changed');
            }
        });
    }

    function obtener_declaraciones($select, pst, periodo) {
        $.ajax({
            url: window.location.origin + '/declaraciones/declaraciones-periodo',
            method: 'GET',
            data: {pst: pst, periodo: periodo}
        }).success(function(data) {
            var template = _.template($('#declaracion-template').html());

            if (data.error == 0) {
                var declaracion_array = JSON.parse(data.result)

                $select.prop('disabled', false).html('').append(
                    template({pk: '', repr: '-- Seleccione --'})
                );

                if (declaracion_array.length == 0) { $select.prop('disabled', true); }

                $.each(declaracion_array, function(index, row) {
                    $select.append(template(row));
                });
            }
        });
    }

    function obtener_fecha_limite($el, periodo) {
        $.ajax({
            url: window.location.origin + '/configuracion/get_fecha_limite.json',
            method: 'GET',
            data: {periodo: periodo}
        }).success(function(data) {
            if (data.error == 0) {
                $el.val(data.result);
            }
        });
    }

    function obtener_ilicitos($modal, resolucion_id) {
        var $ilicitos = $modal.find('.ilicitos');
        var template = _.template($('#ilicito-edit-template').html());

        $.ajax({
            url: window.location.origin + '/resoluciones/ilicito.json',
            method: 'GET',
            data: {resolucion_id: resolucion_id}
        }).success(function(data) {
            if (data.error == 0) {
                var ilicito_list = JSON.parse(data.result);

                for (var i = 0; i < ilicito_list.length; i++) {
                    var new_ilicito = template({
                        declaracion: data.att[i].declaracion,
                        fecha_limite: moment(
                            ilicito_list[i].fields.fecha_limite_declaracion
                        ).format('DD/MM/YYYY'),
                        periodo: moment(
                            ilicito_list[i].fields.periodo
                        ).lang('es').format('MMM-YYYY'),
                        pk: ilicito_list[i].pk,
                        sancion_codigo: data.att[i].sancion_codigo,
                        sancion_ut: ilicito_list[i].fields.sancion_ut,
                        ut_max: data.att[i].ut_max,
                        ut_min: data.att[i].ut_min,
                    });

                    $ilicitos.append(_handle_ilicito_edit($(new_ilicito)));
                }
            }
        });
    }

    function concluir_acta(tipo) {
        $.ajax({
            url: window.location.origin + '/' + tipo + '/concluir.json',
            method: 'PUT',
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", get_cookie("csrftoken"));
            },
            data: {
                acta_id: String(window.location).match(/^.*\/(\d+)\/.*$/)[1],
            },
        }).success(function(data) {
            if (data.error == 0 || data.error == 1) {
                window.location = window.location.origin + '/' + tipo + '/';

            } else if (data.error != 1) {
                alert(data.msg);
            }
        });
    }

    function registrar_observaciones(tipo) {
        $.ajax({
            url: window.location.origin + '/' + tipo + '/registrar_observaciones.json',
            method: 'PUT',
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", get_cookie("csrftoken"));
            },
            data: {
                acta_id: String(window.location).match(/^.*\/(\d+)\/.*$/)[1],
                conclusiones: $('textarea[name=conclusiones]').val(),
                observaciones: $('textarea[name=observaciones]').val(),
            },
        }).success(function(data) {
            if (data.error == 0) {
                concluir_acta(tipo);

            } else {
                alert(data.msg);
            }
        });
    }

    function guardar_nueva_resolucion($modal) {
        var $ilicitos = $modal.find('.ilicitos tr');

        if ($ilicitos.length == 0) {
            alert('No puede crear una resolución sin ilícitos.');
            return;
        }

        $.ajax({
            url: window.location.origin + '/resoluciones/resolucion.json',
            method: 'POST',
            data: {
                csrfmiddlewaretoken: get_cookie('csrftoken'),
                ilicito_list: JSON.stringify(_crawl_ilicitos($modal.find('.ilicitos'))),
                pst_rif: $('#pst-rif span').html(),
                tipo_resolucion_id: '1',
                acta_id: String(window.location).match(/^.*\/(\d+)\/.*$/)[1],
            }
        }).success(function(data) {
            if (data.error == 0) {
                concluir_acta(
                  String(window.location).search('verificacion' >= 0) ? 'verificacion' : 'fiscalizacion'
                );

            } else {
                alert(data.msg);
            }
        });
    }

    function eliminar_ilicitos($modal, resolucion_id) {
        var $ilicitos = $modal.find('.ilicitos');
        var $hidden_ilicitos = $ilicitos.find('.ilicito:hidden');
        var ilicito_id_list = [];

        $hidden_ilicitos.each(function(index, ilicito) {
            ilicito_id_list[index] = $(this).attr('data-pk');
        });


        if ($ilicitos.find('.ilicito:not(:hidden)').length == 0) {
            global_all_ok = false;
            alert('No puede dejar una resolución vacía.')
            return;
        }

        $.ajax({
            url: window.location.origin + '/resoluciones/ilicito.json',
            method: 'DELETE',
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", get_cookie("csrftoken"));
            },
            data: {
                resolucion_id: resolucion_id,
                ilicito_id_list: JSON.stringify(ilicito_id_list),
            }
        }).success(function(data) {
            if (data.error != 0) {
                global_all_ok = false;
                alert(data.msg);

            } else {
                $hidden_ilicitos.remove();
            }
        });
    }

    function eliminar_resolucion($el) {
        $.ajax({
            url: window.location.origin + '/resoluciones/resolucion.json',
            method: 'DELETE',
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", get_cookie("csrftoken"));
            },
            data: {
                resolucion_id: $el.attr('data-pk'),
            },
        }).success(function(data) {
            if (data.error == 0) {
                window.location.reload();
            }
        });
    }

    function solicitar_aprobacion($el) {
        $.ajax({
            url: window.location.origin + '/resoluciones/solicitar_aprobacion.json',
            method: 'PUT',
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", get_cookie("csrftoken"));
            },
            data: {
                resolucion_id: $el.attr('data-pk'),
            },
        }).success(function(data) {
            if (data.error == 0) {
                var new_status = JSON.parse(data.result)[0].fields.estatus;

                $el.parents('tr').find('span.badge').html(new_status);
            }
        });
    }

    function _crawl_ilicitos($el) {
        var ilicitos = [];

        $.each($el.find('tr'), function(index, ilicito) {
            var $ilicito = $(ilicito);

            ilicitos[index] = {
                sancion_codigo: $ilicito.find('.sancion_codigo').html(),
                periodo: _parse_date($ilicito.find('.periodo input').val()),
                fecha_limite: $ilicito.find('.fecha-limite input').val(),
                declaracion_id: $ilicito.find('.declaraciones select option:selected').val() || '',
            };
        });

        return ilicitos;
    }

    function _handle_ilicito($el) {
        var $periodo = $el.find('.periodo input');

        $periodo.datepicker({
            autoclose: true, endDate: 'today', format: 'MM-yyyy', language: 'es', minViewMode: 1
        });

        $periodo.change(function() {
            var $declaraciones = $el.find('.declaraciones select').html('');

            obtener_declaraciones(
                $declaraciones, $('#pst-rif span').html(), _parse_date($(this).val())
            );

            var $fecha_limite = $el.find('.fecha-limite input').val('');

            obtener_fecha_limite(
                $fecha_limite, _parse_date($(this).val())
            );
        });

        $el.find('.eliminar button').click(function() {
            $(this).parents('tr').remove();
        });

        return $el;
    }

    function _handle_ilicito_edit($el) {
        $el.find('.btn-danger').click(function() {
            $(this).parents('.ilicito').hide();
        });

        $el.find('.sancion-ut input').inputmask(
            '9[9][9]', {placeholder: ''}).change(function() {
            $(this).parents('.ilicito').addClass('changed');
        });

        return $el;
    }

    function _parse_descripcion(descripcion) {
        if (descripcion.length > 80) {
            return descripcion.slice(0, 40) + ' ... ' + descripcion.slice(descripcion.length - 40, descripcion.length);
        }
        return descripcion;
    }

    function _parse_date(string) {
        var split = string.split('-');

        return '01' + '/' + MESES[split[0]] + '/' + split[1];
    }
}


function tipo_solicitudes_select_handler() {
  var option_index = +(get_parameter_by_name('tipo') || '3') + 1;

  $(
    '#tipo-solicitudes-select option:nth-of-type(' + option_index + ')'
  ).attr('selected', true);
}


function convertir_periodo_str_date(periodo_str) {
    var split_array = periodo_str.split('-');
    return moment(split_array[1] + '-' + MESES[split_array[0]] + '-01')
}


// http://blog.tompawlak.org/number-currency-formatting-javascript
function currencyFormatDE (num) {
    return num
       .toFixed(2) // always two decimal digits
       .replace(".", ",") // replace decimal point character with ,
       .replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1.") + " Bs." // use . as a separator
}


function get_cookie(cookie) {
    var cookie_dict = document.cookie.split('; ');

    for (var i = 0; i < cookie_dict.length; i++) {
        var key_value = cookie_dict[i].split('=');

        if (key_value[0] == cookie) {
            return key_value[1];
        }
    }
    return undefined;
}


function get_parameter_by_name(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
