#!/bin/bash

# Stop running on first error
set -e

BACKUPPATH="backups"
NOW=$(date +"%d_%m_%Y_%H_%M_%S")
# Parse arguments
while [[ $# > 0 ]]
do
    key="$1"
    case ${key} in
            -h|--help)
            echo "Creating database backup"
            echo "Usage: ./create_backup.sh [options]"
            echo "Options:"
            echo "  --backuppath=PATH                Create backup of database and save it to the specified backup directory"
            echo "  -h, --help                       Show this help message and exit"
            exit
        ;;
            --backuppath=*)
            BACKUPPATH="${key#*=}"
        ;;
        *)
            echo "Unexpected parameter! Exit."
            exit
        ;;
    esac
shift
done


# Find root directory of project and set it as current directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd ${DIR}


# Create backup of database (MySQL/PostgreSQL only)
if [ -n "${BACKUPPATH}" ]; then
    if [ ! -d ${BACKUPPATH} ]; then
        mkdir -p ${BACKUPPATH}
    fi
    docker exec -t db pg_dumpall -c -U postgres | gzip > ${DIR}/${BACKUPPATH}/dump_${NOW}.gz  # db -is docker container name
fi
