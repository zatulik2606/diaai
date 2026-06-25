COMPOSE_FILE := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/compose.yml)

.PHONY: glitchtip-up glitchtip-down glitchtip-ps glitchtip-logs glitchtip-pull

glitchtip-up:
	docker compose -f "$(COMPOSE_FILE)" up -d

glitchtip-down:
	docker compose -f "$(COMPOSE_FILE)" down

glitchtip-ps:
	docker compose -f "$(COMPOSE_FILE)" ps

glitchtip-logs:
	docker compose -f "$(COMPOSE_FILE)" logs -f --tail=100

glitchtip-pull:
	docker compose -f "$(COMPOSE_FILE)" pull
	docker compose -f "$(COMPOSE_FILE)" up -d
