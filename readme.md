# Test task

## Install
* Run project `docker-compose up -d`
* Run migrations `docker-compose exec api python manage.py migrate`
* Create superuser `docker-compose exec api python manage.py createsuperuser`

## Test
* Run command `docker-compose exec api python manage.py test tests`
