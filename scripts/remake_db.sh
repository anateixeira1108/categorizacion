#!/usr/bin/env bash

export python='/usr/bin/env python2.7'

echo "~~~~ Deleting database ~~~~"
rm -f db.sqlite3

echo -e "\n\n~~~~ synchronizing database ~~~~"
$python manage.py syncdb --noinput

echo -e "\n\n~~~~ Loading migrations ~~~~"
$python manage.py migrate

echo -e "\n\n~~~~ Loading fixtures ~~~~"
$python manage.py loaddata fixtures/*

echo -e "\n\n~~~~ Activating accounts ~~~~"
$python scripts/activate_accounts.py
