#!/usr/bin/env bash

# Sinconizamos y migramos la BD
echo -e "\n\nSincronizando la Base de datos..."
/usr/bin/env python2.7 manage.py syncdb --noinput

echo -e "\n\nCargando las migraciones del modelo de datos"
/usr/bin/env python2.7 manage.py migrate venezuela
/usr/bin/env python2.7 manage.py migrate venezuela --fake
/usr/bin/env python2.7 manage.py migrate

# Cargamos la data de prueba
echo -e "\n\nCargando fixtures: Tipos de PST"
/usr/bin/env python2.7 manage.py loaddata fixtures/000_tipo_pst.json

echo -e "\n\nCargando fixtures: Grupos"
/usr/bin/env python2.7 manage.py loaddata fixtures/016_grupos.json

echo -e "\n\nCargando fixtures: Cuentas de PST"
/usr/bin/env python2.7 manage.py loaddata fixtures/001_cuentas_pst.json 
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0001-25032015-cuentas-minturuser.json

echo -e "\n\nCargando fixtures: Registro de PST - Inicial"
/usr/bin/env python2.7 manage.py loaddata fixtures/002_registro_pst_inicial.json 
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0004-25032015-registro-tipopst.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0002-25032015-registro-pst.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0003-25032015-registro-direccion.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0046-25032015-registro-pst-denominacion-comercial.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0047-25032015-registro-sucursales.json

echo -e "\n\nCargando fixtures: Preguntas Secretas de PST"
/usr/bin/env python2.7 manage.py loaddata fixtures/003_preguntas_secretas.json 

echo -e "\n\nCargando fixtures: Idiomas disponibles para PST"
/usr/bin/env python2.7 manage.py loaddata fixtures/004_idiomas.json 

echo -e "\n\nCargando fixtures: Registros mercantiles y Circunscripciones"
/usr/bin/env python2.7 manage.py loaddata fixtures/005_mercantil_circunscripcion.json 

echo -e "\n\nCargando fixtures: Registros mercantiles y Circunscripciones"
/usr/bin/env python2.7 manage.py loaddata fixtures/006_tipos_declaracion.json 

echo -e "\n\nCargando fixtures: Registros mercantiles y Circunscripciones"
/usr/bin/env python2.7 manage.py loaddata fixtures/007_declaracion.json

echo -e "\n\nCargando fixtures: Tipos de conceptos"
/usr/bin/env python2.7 manage.py loaddata fixtures/008_concepto_tipo.json

echo -e "\n\nCargando fixtures: Procesos"
/usr/bin/env python2.7 manage.py loaddata fixtures/009_procesos.json

echo -e "\n\nCargando fixtures: Pagos"
/usr/bin/env python2.7 manage.py loaddata fixtures/010_pago.json

echo -e "\n\nCargando fixtures: Conceptos"
/usr/bin/env python2.7 manage.py loaddata fixtures/011_concepto.json

echo -e "\n\nCargando fixtures: Tipos de Actas"
/usr/bin/env python2.7 manage.py loaddata fixtures/012_tipos_actas.json

echo -e "\n\nCargando fixtures: Verificaciones"
/usr/bin/env python2.7 manage.py loaddata fixtures/013_verificaciones.json

echo -e "\n\nCargando fixtures: Funcionarios Verificaciones"
/usr/bin/env python2.7 manage.py loaddata fixtures/014_funcionarios_verificaciones.json

echo -e "\n\nCargando fixtures: Providencias de verificaciones"
/usr/bin/env python2.7 manage.py loaddata fixtures/015_providencias_actas.json

echo -e "\n\nCargando fixtures: Requisitos para actas de requirimientos"
/usr/bin/env python2.7 manage.py loaddata fixtures/020_requisitos.json

echo -e "\n\nCargando fixtures: Fiscalizaciones"
/usr/bin/env python2.7 manage.py loaddata fixtures/019_fiscalizaciones.json

echo -e "\n\nCargando fixtures: Funcionarios Fiscalizaciones"
/usr/bin/env python2.7 manage.py loaddata fixtures/021_funcionarios_fiscalizaciones.json

echo -e "\n\nCargando fixtures: Modulo de Licencias"
/usr/bin/env python2.7 manage.py loaddata apps/licencias/fixtures/0001_initial_data.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0001-25032015-licencia-tipolicencia.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0002-25032015-licencia-estatussolicitud.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0003-25032015-licencia-solicitudlicencia.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0045-25032015-licencia-licenciaasignada.json

echo -e "\n\nCargando fixtures: Modulo de Categorizacion - DEMO AND PRELOADED DATA ONLY"
# DEMO Categorizacion
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0001-25032015-categorizacion-tipomedida.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0002-25032015-categorizacion-tiporespuesta.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0048-07042015-categorizacion-tipodocumentofundamental.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0030-25032015-categorizacion-tabulador.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0004-25032015-categorizacion-categoria.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0006-25032015-categorizacion-direccion.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0003-25032015-categorizacion-aspectofundamentalconfig.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0009-25032015-categorizacion-encuesta.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0013-25032015-categorizacion-estatussolicitudlicencia.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0015-25032015-categorizacion-lsrdigital.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0017-25032015-categorizacion-oficinaregional.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0018-25032015-categorizacion-parametroconfiguracion.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0019-25032015-categorizacion-plantilladocumento.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0023-25032015-categorizacion-respuestaconfig.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0025-25032015-categorizacion-seccionconfig.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0026-25032015-categorizacion-seccionencuesta.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0027-25032015-categorizacion-severidad.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0031-25032015-categorizacion-tipoasignacion.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0032-25032015-categorizacion-tipocomentario.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0033-25032015-categorizacion-tipodocumentocompuesto.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0034-25032015-categorizacion-tipodocumentoidentidad.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0035-25032015-categorizacion-tipoespecificacionlegal.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0036-25032015-categorizacion-tiporequisitopago.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0037-25032015-categorizacion-tiporol.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0038-25032015-categorizacion-tiposolicitud.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0039-14042015-categorizacion-tiposubseccion.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0040-25032015-categorizacion-tipovaloracion.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0041-25032015-categorizacion-turista.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0042-25032015-categorizacion-valoracion.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0043-25032015-categorizacion-operadorformula.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0044-25032015-categorizacion-valorrespuestaconfig.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0011-25032015-categorizacion-estatus.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0014-25032015-categorizacion-funcionario.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0007-25032015-categorizacion-elementoencuesta.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0008-25032015-categorizacion-elementoencuestaseccionencuesta.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0010-25032015-categorizacion-especificacionlegal.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0029-25032015-categorizacion-subseccionconfig.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0024-25032015-categorizacion-respuestavalorrespuesta.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0050-25032015-tipoaspectofundamental.json
/usr/bin/env python2.7 manage.py loaddata apps/categorizacion/fixtures/0049-12052015-categorizacion-credencialesotorgadas.json

echo -e "\n\nActivando los usuarios registrados con fixtures"
/usr/bin/env python2.7 scripts/activate_accounts.py

echo -e "Configurando procesos CRON"
crontab -r
/usr/bin/env python2.7 manage.py crontab add
