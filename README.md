# JOBSITY Data Engineering Challenge

Requirements for this solution:
* Docker installed

Instructions:
* After executing git clone for this repository, run docker_mysql.sh for creating MySQL docker container;
* Update the constant 'SQL_DATABASE_SERVER' inside src/config_file.py according to the IP shown to MySQL docker contained created;
* Update 'tripsFileSourcePath' inside src/config_file.py with the path that will contain trip.csv source files;

Solution:

I'm using Python/Pandas Language and a Mysql Docker Container as my SQL Database. The engine extracts trips.csv (and all other files *.csv) inside the source directory into a Memory Pandas Data Frame, adds some technical fields like execution ID, filename, date of execution, and then appends it into Raw Zone Database. The transformation process grabs all the data from raw zone, groups duplicated data based on DateTime, origin, and destination generating the info of the number of trips. With this, the solution creates the table 'trips_detailed' into curated database and the average per week is calculated using a SQL View trips_w_average.
The user can track the status of execution querying the table 'auditlogs', inside Audit Database jobsity_DEC_AUDIT.
