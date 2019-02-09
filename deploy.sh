#!/bin/bash

# Stop running on first error
set -e

# Default options
SERVER='prod'
CELERY=true
BACKUPPATH=""
PULL=true
CLEAN=true
DELETE=true
ENV=true
SYNCDB=true
COLLECTSTATIC=true
SUPERUSER=false

# Parse arguments
while [[ $# > 0 ]]
do
    key="$1"
    case ${key} in
            -h|--help)
            echo "Updating project and python virtual environment"
            echo "Usage: ./deploy.sh [options]"
            echo "Options:"
            echo "  --server                         Server to build on (production, staging, dev)"
            echo "  -no-celery                       Do not turn off and turn on celery during deployment"
            echo "  --backuppath=PATH                Create backup of database and save it to the specified backup directory"
            echo "  -no-pull                         Do not update source code from repository"
            echo "  -no-clean                        Do not remove Python compiled files"
            echo "  -no-delete                       Do not delete empty folders under static_content/files"
            echo "  -no-env                          Do not update Python virtual environment"
            echo "  -no-syncdb                       Do not syncronize schema of database"
            echo "  -no-collectstatic                Do not collect static files (img, css, js)"
            echo "  -superuser                       Create super user"
            echo "  -h, --help                       Show this help message and exit"
            exit
        ;;
            --server=*)
            SERVER="${key#*=}"
        ;;
            -no-celery)
            CELERY=false
        ;;
            --backuppath=*)
            BACKUPPATH="${key#*=}"
        ;;
            -no-pull)
            PULL=false
        ;;
            -no-clean)
            CLEAN=false
        ;;
            -no-delete)
            DELETE=false
        ;;
            -no-env)
            ENV=false
        ;;
            -no-syncdb)
            SYNCDB=false
        ;;
            -no-collectstatic)
            COLLECTSTATIC=false
        ;;
            -superuser)
            SUPERUSER=true
        ;;
        *)
            echo "Unexpected parameter! Exit."
            exit
        ;;
    esac
shift
done

if [ "${SERVER}" = 'production' ]; then
    BRANCH=master
else
    BRANCH=dev
fi

# Find root directory of project and set it as current directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd ${DIR}

# Stop celery worker if celery was installed
if [ "${CELERY}" = true ]; then
    docker-compose -f docker-compose.yml stop celery &&
    docker-compose -f docker-compose.yml stop celerybeat
fi

# Create backup of database (MySQL/PostgreSQL only)
#if [ -n "${BACKUPPATH}" ]; then
#    if [ -d ${BACKUPPATH} ]; then
#        ${DIR}/commands/manage.sh dbdump --destination=${BACKUPPATH} --filename=$(date +%s).sql --compress=gzip
#    fi
#fi

# Update source code from repository
if [ "${PULL}" = true ]; then
    git pull origin $BRANCH
fi

# Remove Python compiled files
if [ "${CLEAN}" = true ]; then
    find ${DIR} -name '*.pyc' -delete
fi

# Update existed and install new Python packages
if [ "${ENV}" = true ]; then
    docker-compose -f docker-compose.yml -f docker-compose-"${SERVER}".yml up -d --build
fi

# Syncronize schema of database
if [ "${SYNCDB}" = true ]; then
    docker exec -it web python manage.py migrate --traceback
fi

# Collect static files (img, css, js)
if [ "${COLLECTSTATIC}" = true ]; then
    docker exec -it web python manage.py collectstatic --noinput
fi

if [ "${SUPERUSER}" = true ]; then
    docker exec -it web python manage.py createsuperuser
fi