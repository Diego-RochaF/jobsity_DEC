#!/bin/bash

if [ "$EUID" -ne 0 ] 
then
    echo 'Please, run this script using SUDO / ROOT privileges'
    exit

else
    echo '#Mysql Docker Image'
    if [[ "$(docker images -q mysql-image:latest 2> /dev/null)" == "" ]]; then
    
    echo '--Creating mysql-image'
    
    docker build -t mysql-image -f mysql/Dockerfile .
    fi

    echo '#Running Mysql Docker image'
    dockid=$(docker run -d --rm --name mysql-container mysql-image)
    echo "Container ID : $dockid"
    docker inspect $dockid | grep -i IPAddress

    echo '#Creating jobsity user and databases on mysql docker container'
    sleep 120
    sudo docker exec -i mysql-container mysql -uroot -pjobsityDataEngineerChallenge < mysql/initial_structure.sql

fi