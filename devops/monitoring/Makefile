REPO_ROOT := $(abspath ../..)
MONITORING_COMPOSE = -f docker-compose.yml -f devops/monitoring/compose.yml
MONITORING_PROFILE = --profile monitoring

.PHONY: monitoring-up monitoring-down monitoring-ps monitoring-logs monitoring-build kuma-bootstrap kuma-notifications

monitoring-up:
	cd $(REPO_ROOT) && COMPOSE_PROFILES=monitoring docker compose $(MONITORING_COMPOSE) up -d --build \
		dozzle glitchtip-telegram-bridge uptime-kuma prometheus loki promtail grafana cadvisor

monitoring-down:
	cd $(REPO_ROOT) && docker compose $(MONITORING_COMPOSE) $(MONITORING_PROFILE) down

monitoring-ps:
	cd $(REPO_ROOT) && docker compose $(MONITORING_COMPOSE) $(MONITORING_PROFILE) ps

monitoring-logs:
	cd $(REPO_ROOT) && \
	if [ -n "$(SVC)" ]; then docker compose $(MONITORING_COMPOSE) $(MONITORING_PROFILE) logs -f $(SVC); \
	else docker compose $(MONITORING_COMPOSE) $(MONITORING_PROFILE) logs -f; fi

monitoring-build:
	cd $(REPO_ROOT) && docker compose $(MONITORING_COMPOSE) $(MONITORING_PROFILE) build glitchtip-telegram-bridge

kuma-bootstrap:
	cd $(REPO_ROOT) && \
	set -a && [ -f .env ] && . ./.env && set +a && \
	docker run --rm --network diaai_default \
		-e KUMA_URL=http://diaai-uptime-kuma-1:3001 \
		-e KUMA_USERNAME=$${KUMA_USERNAME:-admin} \
		-e KUMA_PASSWORD=$$KUMA_PASSWORD \
		-v $(REPO_ROOT)/devops/monitoring/kuma-bootstrap.py:/app/kuma-bootstrap.py:ro \
		-v $(REPO_ROOT)/devops/monitoring/requirements-kuma.txt:/app/requirements-kuma.txt:ro \
		python:3.12-slim \
		sh -c 'pip install -q -r /app/requirements-kuma.txt && python /app/kuma-bootstrap.py'

kuma-notifications:
	cd $(REPO_ROOT) && \
	set -a && [ -f .env ] && . ./.env && set +a && \
	docker run --rm --network diaai_default \
		-e KUMA_URL=http://diaai-uptime-kuma-1:3001 \
		-e KUMA_USERNAME=$${KUMA_USERNAME:-admin} \
		-e KUMA_PASSWORD=$$KUMA_PASSWORD \
		-e KUMA_TELEGRAM_BRIDGE_URL=$${KUMA_TELEGRAM_BRIDGE_URL:-http://glitchtip-telegram-bridge:8080/webhook} \
		-v $(REPO_ROOT)/devops/monitoring/kuma-notifications.py:/app/kuma-notifications.py:ro \
		-v $(REPO_ROOT)/devops/monitoring/requirements-kuma.txt:/app/requirements-kuma.txt:ro \
		python:3.12-slim \
		sh -c 'pip install -q -r /app/requirements-kuma.txt && python /app/kuma-notifications.py'
