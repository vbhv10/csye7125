SHELL := /bin/zsh

migrate:
	flyway migrate -outputType=json -configFiles=./flyway.conf

migrate-local:
	( \
		source .venv; \
		flyway migrate -outputType=json -configFiles=./flyway.conf -locations=filesystem:./migrations/; \
	)
