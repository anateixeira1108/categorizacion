#! /usr/bin/env bash

if [ -f db.sqlite3 ]
then
    echo -e "\n\n- Eliminando base de datos de desarrollo..."
    rm db.sqlite3 
    
fi


# Sinconizamos y migramos la BD
echo -e "\n\n- Sincronizando la Base de datos..."
/usr/bin/env python2.7 manage.py syncdb --noinput 

echo "- Cargando las migraciones del modelo de datos..."
/usr/bin/env python2.7 manage.py migrate 

# Cargamos la data de prueba
echo -e "\n\n- Cargando fixtures: Tipos de PST"
/usr/bin/env python2.7 manage.py loaddata fixtures/000_tipo_pst.json 

echo -e "\n\n- Cargando fixtures: Grupos"
/usr/bin/env python2.7 manage.py loaddata fixtures/016_grupos.json

echo -e "\n\n- Cargando fixtures: Cuentas de PST"
/usr/bin/env python2.7 manage.py loaddata fixtures/001_cuentas_pst.json 

echo -e "\n\n- Cargando fixtures: Registro de PST - Inicial"
/usr/bin/env python2.7 manage.py loaddata fixtures/002_registro_pst_inicial.json 

echo -e "\n\n- Cargando fixtures: Preguntas Secretas de PST"
/usr/bin/env python2.7 manage.py loaddata fixtures/003_preguntas_secretas.json 

echo -e "\n\n- Cargando fixtures: Idiomas disponibles para PST"
/usr/bin/env python2.7 manage.py loaddata fixtures/004_idiomas.json 

echo -e "\n\n- Cargando fixtures: Registros mercantiles y Circunscripciones"
/usr/bin/env python2.7 manage.py loaddata fixtures/005_mercantil_circunscripcion.json 

echo -e "\n\n- Cargando fixtures: Registros mercantiles y Circunscripciones"
/usr/bin/env python2.7 manage.py loaddata fixtures/006_tipos_declaracion.json 

echo -e "\n\n- Cargando fixtures: Registros mercantiles y Circunscripciones"
/usr/bin/env python2.7 manage.py loaddata fixtures/007_declaracion.json

echo -e "\n\n- Cargando fixtures: Tipos de conceptos"
/usr/bin/env python2.7 manage.py loaddata fixtures/008_concepto_tipo.json

echo -e "\n\n- Cargando fixtures: Procesos"
/usr/bin/env python2.7 manage.py loaddata fixtures/009_procesos.json

echo -e "\n\n- Cargando fixtures: Pagos"
/usr/bin/env python2.7 manage.py loaddata fixtures/010_pago.json

echo -e "\n\n- Cargando fixtures: Conceptos"
/usr/bin/env python2.7 manage.py loaddata fixtures/011_concepto.json

echo -e "\n\n- Cargando fixtures: Tipos de Actas"
/usr/bin/env python2.7 manage.py loaddata fixtures/012_tipos_actas.json

echo -e "\n\n- Cargando fixtures: Verificaciones"
/usr/bin/env python2.7 manage.py loaddata fixtures/013_verificaciones.json

echo -e "\n\n- Cargando fixtures: Funcionarios Verificaciones"
/usr/bin/env python2.7 manage.py loaddata fixtures/014_funcionarios_verificaciones.json

echo -e "\n\n- Cargando fixtures: Providencias de verificaciones"
/usr/bin/env python2.7 manage.py loaddata fixtures/015_providencias_actas.json

echo -e "\n\n- Cargando fixtures: Requisitos para actas de requirimientos"
/usr/bin/env python2.7 manage.py loaddata fixtures/020_requisitos.json

echo -e "\n\n- Cargando fixtures: Fiscalizaciones"
/usr/bin/env python2.7 manage.py loaddata fixtures/019_fiscalizaciones.json

echo -e "\n\n- Cargando fixtures: Funcionarios Fiscalizaciones"
/usr/bin/env python2.7 manage.py loaddata fixtures/021_funcionarios_fiscalizaciones.json

echo -e "\n\n- Activando los usuarios registrados con fixtures..."
/usr/bin/env python2.7 scripts/activate_accounts.py













