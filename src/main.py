from curses import echo
from fileinput import filename
from json.tool import main
from time import time
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
    __logrow = {'execid': execid, 'db_name': db_name, 'action_dsc': action_dsc,
                'status_action': status_action, 'log_datetime': log_datetime, 'addt_info': addt_info}
    __dfLOG = pd.DataFrame(data=__logrow, index=[0])
    __dfLOG.to_sql('auditlogs', mysqlengine_aud, if_exists='append',
                   index=False, chunksize=500)

    return


def importTripsSource(filepath):
    dfSourceTrips = pd.read_csv(filepath)
    dfSourceTrips['_filename'] = filepath  # stores filename as reference
    dfSourceTrips['_exec_time'] = executionTime
    dfSourceTrips['_execID'] = execID
    return dfSourceTrips


def main():
    # ingest all *.csv files into raw
    registerLOG(execID, config_file.RAW_DATABASE, 'EXTRACTION',
                'STARTED', datetime.now(), 'Started CSV Extraction Process')
    try:
        for filename in glob.glob(os.path.join(tripsFilePath, '*.csv')):
            # Transforms the current file into a Pandas Dataframe
            dfTripsRaw = importTripsSource(filename)
            dfTripsRaw.to_sql('trips', mysqlengine_raw, if_exists='append',
                              index=True, chunksize=1000)  # writes to trips table on rawzone

        totalRawRows = len(dfTripsRaw.index)
        registerLOG(execID, config_file.RAW_DATABASE, 'EXTRACTION', 'FINISHED', datetime.now(
        ), 'Finished CSV Extraction Process - {0} rows inserted into RAW'.format(totalRawRows))
    except Exception as err:
        registerLOG(execID, config_file.RAW_DATABASE,
                    'EXTRACTION', 'FAILED', datetime.now(), err)
        print('####ERROR : ' + str(err))

    # group data and create additional fields for Analysis
    registerLOG(execID, config_file.CURATED_DATABASE, 'TRANSFORM',
                'STARTED', datetime.now(), 'Started Trips Process')
    try:
        dfTripsCurated = pd.read_sql_query(
            'SELECT region, origin_coord, destination_coord, `datetime`, count(`index`) cnt_trips FROM jobsity_DEC_RAW.trips group by region, origin_coord, destination_coord, `datetime`', mysqlengine_raw)
        dfTripsCurated['Date'] = pd.to_datetime(
            dfTripsCurated['datetime']).dt.date
        dfTripsCurated['Year'] = pd.to_datetime(
            dfTripsCurated['datetime']).dt.year
        dfTripsCurated['Month'] = pd.to_datetime(
            dfTripsCurated['datetime']).dt.month
        dfTripsCurated['Week'] = pd.to_datetime(
            dfTripsCurated['datetime']).dt.week
        dfTripsCurated['Time'] = pd.to_datetime(
            dfTripsCurated['datetime']).dt.time

        dfTripsCurated.to_sql('trips_detailed', mysqlengine_cur,
                              if_exists='replace', index=True, chunksize=1000)
        registerLOG(execID, config_file.CURATED_DATABASE, 'TRANSFORM',
                    'FINISHED', datetime.now(), 'Finished Trips Process')
        registerLOG(execID, config_file.CURATED_DATABASE, 'PROCESS',
                    'COMPLETED', datetime.now(), 'Process Completed')

    except Exception as err:
        registerLOG(execID, config_file.CURATED_DATABASE,
                    'TRANSFORM', 'FAILED', datetime.now(), err)
        print('####ERROR : ' + str(err))


if __name__ == '__main__':
    main()
    print('#####EXTRACTION COMPLETED#####')
