REPO_ROOT := ../..
MONITORING_COMPOSE = -f docker-compose.yml -f devops/monitoring/compose.yml
MONITORING_PROFILE = --profile monitoring

.PHONY: monitoring-up monitoring-down monitoring-ps monitoring-logs monitoring-build

monitoring-up:
	cd $(REPO_ROOT) && COMPOSE_PROFILES=monitoring docker compose $(MONITORING_COMPOSE) up -d --build dozzle glitchtip-telegram-bridge uptime-kuma

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
