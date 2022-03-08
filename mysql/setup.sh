#!/bin/bash
set -e
service mysql start
mysql < /mysql/initial_structure.sql
mysql < /mysql/trips_average_view.sql
service mysql stop