up_broker:
	docker-compose -f docker-compose.message-broker.yml up -d

up:
	docker-compose \
    -f docker-compose.services.yml \
    -f docker-compose.client.yml \
    up

down: 
	docker-compose \
    -f docker-compose.message-broker.yml \
    -f docker-compose.services.yml \
    -f docker-compose.client.yml \
    down

up_with_build:
	docker-compose \
    -f docker-compose.services.yml \
    -f docker-compose.client.yml \
    up --build
