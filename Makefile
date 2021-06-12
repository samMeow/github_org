.PHONY: test lint lint-fix run db-up

test:
	FLASK_APP=manage:app pipenv run flask test

lint:
	pylint ./app

lint-fix:
	autopep8 --in-place --aggressive ./app/**/*.py

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

.PHONY: docker-seed
docker-seed:
	docker-compose exec -d dummy-server sh -c "FLASK_APP=manage:app pipenv run flask cold_sync"
