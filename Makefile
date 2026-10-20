.PHONY: check up down init fmt validate plan apply destroy

check:
	./scripts/check-prerequisites.sh

up:
	docker compose up -d

down:
	docker compose down

init:
	tofu -chdir=infra init

fmt:
	tofu -chdir=infra fmt -recursive

validate:
	tofu -chdir=infra validate

plan:
	tofu -chdir=infra plan

apply:
	tofu -chdir=infra apply

destroy:
	tofu -chdir=infra destroy
