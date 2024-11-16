#!/bin/bash
mkdir ../frontend/node_modules
touch ../frontend/yarn.lock
touch ../frontend/yarn-error.log
touch ../backend/config/django.log
touch ../backend/config/django_error.log

sudo chown -R 1001:1001 ../ ; sudo sudo chmod -R 777 ../

#sudo chown -R 1001:1001 ./postgres/
#sudo chmod -R 775 ./postgres/
#chmod 775 ../frontend/node_modules
#chmod 775 ../frontend/.yarn-error.log
#chmod 775 ../backend/config/django.log
#chmod 775 ../backend/config/django_error.log
#chmod 775 /bitnami/postgresql/data