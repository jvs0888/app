include settings/.env

dep-install:
	apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npm@latest
	npm install tailwindcss

	pip install poetry
	poetry install

tailwind-build:
	npx tailwindcss -i ./static/css/tailwind.css -o ./static/css/tailwind.output.css

run-dev: tailwind-build
	uvicorn --host $(HOST) --port $(PORT) --reload --factory app.main:init_app

run-prod: tailwind-build
	gunicorn 'app.main:init_app()' --config settings/gunicorn_conf.py -b $(HOST):$(PORT)


docker-build:
	docker build -t $(IMAGE_NAME) .

docker-run:
	docker run -d --network host -e HOST=$(HOST) -e PORT=$(PORT) --name $(IMAGE_NAME)-container $(IMAGE_NAME)

docker-exec:
	docker exec -it $(IMAGE_NAME)-container bash

docker-stop:
	docker stop $(IMAGE_NAME)-container

docker-rm:
	docker rm $(IMAGE_NAME)-container

docker-rmi:
	docker rmi $(IMAGE_NAME)

.PHONY: dep-install tailwind-build run-dev run-prod docker-build docker-run docker-exec docker-stop docker-rm docker-rmi
