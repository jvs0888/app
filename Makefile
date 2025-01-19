include settings/.env

tailwind-build:
	npx tailwindcss -i ./static/css/tailwind.css -o ./static/css/tailwind.output.css

run-dev:
	$(MAKE) tailwind-build
	uvicorn --host $(HOST) --port $(PORT) --reload --factory app.main:init_app

run-prod:
	$(MAKE) tailwind-build
	gunicorn 'app.main:init_app()' --config settings/gunicorn_conf.py -b $(HOST):$(PORT)


docker-build:
	docker build -t $(IMAGE_NAME) .

docker-run:
	docker run -d --network host -e HOST=$(HOST) -e PORT=$(PORT) $(IMAGE_NAME)

docker-stop:
	docker stop $$(docker ps -q --filter ancestor=$(IMAGE_NAME))

docker-rm:
	docker rm $$(docker ps -a -q --filter ancestor=$(IMAGE_NAME))

docker-rmi:
	docker rmi $(IMAGE_NAME)

.PHONY: tailwind-build run-dev run-prod docker-build docker-run docker-stop docker-rm docker-rmi
