how to get started

what we need:
- accessible redis server
- run startRedis to populate initial queue of shit
- start rockitchef server

- start runner to start worker nodes that crawl for shit


##redis cli

run redis-server to start server
redis-cli ping


###start rockitchef server

source env/bin/activate
python manage.py runserver