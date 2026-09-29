.PHONY: dev doctor test build migrate db-shell db-start db-stop

dev:
	backend/.venv/bin/python scripts/dev.py

doctor:
	backend/.venv/bin/python scripts/doctor.py

test:
	cd backend && .venv/bin/python -m pytest

build:
	cd frontend && npm run build

migrate:
	cd backend && .venv/bin/alembic upgrade head

db-shell:
	/opt/homebrew/opt/mysql@8.4/bin/mysql --defaults-extra-file=.secrets/mysql-admin.cnf

db-start:
	brew services start mysql@8.4

db-stop:
	brew services stop mysql@8.4
