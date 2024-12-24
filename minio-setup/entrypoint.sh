#!/bin/bash

until mc alias set myminio http://minio:9000 ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD}; do
    echo "Failed to set mc alias. Retrying in 5 seconds..."
    echo $?
    sleep 1
done

mc mb myminio/jokes

mc quota set myminio/jokes --size 5MB