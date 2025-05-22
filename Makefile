
default: db collectstatic clearpyc end

local: db clearpyc end

black:
	@echo "***  Black - Reformat pycode in sc_backend/ ***"
	@echo ""
	black sc_backend/

flake8:
	@echo "Running flake8"
	flake8 --show-source sc_backend/
	@echo "Finish flake8"

pytest:
	@echo "Run pytest"
	cd sc_backend &&  pytest

db: migrate

migrate:
	@echo "Running migrations"
	cd sc_backend && python manage.py migrate --run-syncdb -v 1 --traceback

collectstatic:
	@echo "Collect static"
	cd sc_backend && python manage.py collectstatic --noinput -v 1

server:
	@echo "Running local server"
	python sc_backend/manage.py runserver 8000

clearpyc:
	@echo "Delete pyc files"
	cd sc_backend && find . -type f -name '*.pyc' -Delete

end:
	@echo "Make complete ok"
