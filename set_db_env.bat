@echo off
:: Set PostgreSQL database environment variables, ref database/__init__.py

set DB_RDBM=postgresql+psycopg2
::  Specifies the dialect and driver. psycopg2 is the most common PostgreSQL driver.
set DB_USER=postgres
set DB_PASS=mydb
set DB_IP=localhost
:: or 127.0.0.1, or maybe 0.0.0.0?  
set DB_PORT=5432
set DB_HOST=%DB_IP%:%DB_PORT%
set DB_NAME=NASR

:: No quotation marks required for values
echo Environment variables set for PostgreSQL access.
pause