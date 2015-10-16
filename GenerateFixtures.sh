#!/bin/bash
APP=admtooCore
TABLES=( Country Office EmailAlert EmailAlertMessage UserClass )

for table in "${TABLES[@]}"
do 
	echo dumping table ${table}
	./manage.py dumpdata ${APP}.${table} > ${APP}/fixtures/${table}.json
done

