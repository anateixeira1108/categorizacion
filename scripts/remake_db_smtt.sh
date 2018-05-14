#!/usr/bin/env bash

export python='/usr/bin/env python2.7'

echo "~~~~ Deleting database ~~~~"
PGPASSWORD=mintur dropdb -Umintur mintur

echo -e "\n\n~~~~ Recreate database ~~~~"
PGPASSWORD=mintur createdb -Umintur -E'UTF-8' mintur

echo -e "\n\n~~~~ Synchronizing database ~~~~"
$python manage.py syncdb --noinput --settings=settings.smtt

echo -e "\n\n~~~~ Loading migrations ~~~~"
$python manage.py migrate --settings=settings.smtt

echo -e "\n\n~~~~ Loading fixtures ~~~~"
$python manage.py loaddata fixtures/* --settings=settings.smtt

echo -e "\n\n~~~~ Activating accounts ~~~~"
$python scripts/activate_accounts.py 'settings.smtt'
