SELF_HOSTED_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/self-hosted)
SCRIPT_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/scripts)

.PHONY: sentry-install sentry-up sentry-down sentry-ps sentry-cloud-projects

sentry-install:
	@test -d "$(SELF_HOSTED_DIR)" || git clone --depth 1 https://github.com/getsentry/self-hosted.git "$(SELF_HOSTED_DIR)"
	@echo "Next: cd $(SELF_HOSTED_DIR) && ./install.sh && docker compose up -d"

sentry-up:
	@test -d "$(SELF_HOSTED_DIR)" || (echo "Run: make sentry-install" >&2; exit 1)
	cd "$(SELF_HOSTED_DIR)" && docker compose up -d

sentry-down:
	@test -d "$(SELF_HOSTED_DIR)" || exit 0
	cd "$(SELF_HOSTED_DIR)" && docker compose down

sentry-ps:
	@test -d "$(SELF_HOSTED_DIR)" || (echo "Run: make sentry-install" >&2; exit 1)
	cd "$(SELF_HOSTED_DIR)" && docker compose ps

sentry-cloud-projects:
	@test -n "$$SENTRY_AUTH_TOKEN" || (echo "Set SENTRY_AUTH_TOKEN — see README.md § sentry.io" >&2; exit 1)
	bash "$(SCRIPT_DIR)/create-projects-cloud.sh"
