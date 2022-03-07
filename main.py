from curses import echo
from fileinput import filename
from json.tool import main
from unicodedata import name
import pandas as pd
import config_file
import os
import glob
from datetime import date, datetime
import sqlalchemy

tripsFilePath = config_file.tripsFileSourcePath
now = datetime.now()
executionTime = now.strftime('%Y-%m-%d %H:%M:%S')
execID = now.strftime('%Y%m%d%H%M%S')

# DATABASE CONFIG
db_user = config_file.SQL_DATABASE_USER
db_pass = config_file.SQL_DATABASE_PASSWORD
db_host = config_file.SQL_DATABASE_SERVER
db_port = config_file.SQL_DATABASE_PORT


mysqlengine_raw = sqlalchemy.create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(
    db_user, db_pass, db_host, db_port, config_file.RAW_DATABASE), echo=False)
mysqlengine_cur = sqlalchemy.create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(
    db_user, db_pass, db_host, db_port, config_file.CURATED_DATABASE), echo=False)
mysqlengine_aud = sqlalchemy.create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(
    db_user, db_pass, db_host, db_port, config_file.AUDIT_DATABASE), echo=False)


def registerLOG(execid, db_name, action_dsc, status_action, log_datetime, addt_info):

    return


def importTripsSource(filepath):
    dfSourceTrips = pd.read_csv(filepath)
    dfSourceTrips['_filename'] = filepath  # stores filename as reference
    dfSourceTrips['_exec_time'] = executionTime
    dfSourceTrips['_execID'] = execID
    return dfSourceTrips


def main():

    for filename in glob.glob(os.path.join(tripsFilePath, '*.csv')):
        dfTripsRaw = importTripsSource(filename) #Transforms the current file into a Pandas Dataframe
        dfTripsRaw.to_sql('trips',mysqlengine_raw,if_exists='append',index=True,chunksize=500) ##writes to trips table on rawzone

    print(dfTripsRaw)


if __name__ == '__main__':
    main()
