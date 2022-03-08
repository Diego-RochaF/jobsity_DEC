#!/bin/bash
echo 'Starting venv'
source venv/bin/activate
echo 'Starting Trips extractor'
python3 main.py
echo 'Creating View'
sudo docker exec -i mysql-container mysql -uroot -pjobsityDataEngineerChallenge < mysql/trips_average_view.sql