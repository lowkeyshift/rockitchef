docker-compose -f docker_postgres/docker-compose.yaml down && \
docker-compose -f docker_postgres/docker-compose.yaml up --build -d && \
sleep 3 && \
python3 manage.py makemigrations && \
python3 manage.py migrate
