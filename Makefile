.PHONY: tests lint lint-fix run db-up

tests:
	APP_ENV=test python manage.py test

lint:
	pylint ./app

lint-fix:
	autopep8 --in-place --aggressive --aggressive ./app/**/*.py

run:
	python manage.py run

db-up:
	FLASK_APP=manage:app pipenv run flask db upgrade

deploy:
	heroku container:push --app sammeow-instapic-backend web
	heroku container:release --app sammeow-instapic-backend web

.PHONY: docker-up
docker-up:
	docker network create dummy || true
	docker-compose up -d

all: clean install tests run
