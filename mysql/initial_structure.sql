CREATE USER IF NOT EXISTS 'jobsity'@'%' IDENTIFIED BY 'jobsitypassTest1';
CREATE DATABASE IF NOT EXISTS jobsity_DEC_RAW;
GRANT ALL PRIVILEGES ON jobsity_DEC_RAW.* TO 'jobsity'@'%';
CREATE DATABASE IF NOT EXISTS jobsity_DEC_CURATED;
GRANT ALL PRIVILEGES ON jobsity_DEC_CURATED.* TO 'jobsity'@'%';
CREATE DATABASE IF NOT EXISTS jobsity_DEC_AUDIT;
GRANT ALL PRIVILEGES ON jobsity_DEC_AUDIT.* TO 'jobsity'@'%';
USE jobsity_DEC_AUDIT;
CREATE TABLE IF NOT EXISTS auditlogs(
    logid INT NOT NULL AUTO_INCREMENT,
    execid DOUBLE NOT NULL,
    db_name varchar(100) NOT NULL,
    action_dsc varchar(100) NOT NULL,
    status_action varchar(20) NOT NULL,
    log_datetime datetime NOT NULL,
    addt_info TEXT,
    PRIMARY KEY (logid)
);