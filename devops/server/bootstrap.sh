#!/usr/bin/env bash
# Bootstrap diaai VPS: Docker, compose plugin, base tools, ufw, deploy user.
# Ubuntu 24.04+ · run as root · idempotent.
#
# Usage:
#   scp devops/server/bootstrap.sh root@SERVER:/tmp/
#   scp ~/.ssh/diaai-deploy.pub root@SERVER:/tmp/diaai-deploy.pub   # optional
#   ssh root@SERVER 'bash /tmp/bootstrap.sh'

set -euo pipefail

DEPLOY_USER="${DEPLOY_USER:-deploy}"
DEPLOY_PUBKEY_FILE="${DEPLOY_PUBKEY_FILE:-/tmp/diaai-deploy.pub}"
APP_DIR="${APP_DIR:-/opt/diaai}"

log() { echo "[bootstrap] $*"; }

require_root() {
  if [[ "${EUID:-$(id -u)}" -ne 0 ]]; then
    echo "Run as root" >&2
    exit 1
  fi
}

install_base_packages() {
  log "Installing base packages..."
  export DEBIAN_FRONTEND=noninteractive
  apt-get update -qq
  apt-get install -y -qq \
    ca-certificates \
    curl \
    git \
    make \
    ufw \
    gnupg \
    lsb-release
}

install_docker() {
  if command -v docker >/dev/null 2>&1; then
    log "Docker already installed: $(docker --version)"
  else
    log "Installing Docker Engine..."
    curl -fsSL https://get.docker.com | sh
  fi

  systemctl enable docker
  systemctl start docker

  if ! docker compose version >/dev/null 2>&1; then
    log "ERROR: docker compose plugin missing" >&2
    exit 1
  fi
  log "Compose: $(docker compose version)"
}

setup_deploy_user() {
  if ! id "${DEPLOY_USER}" >/dev/null 2>&1; then
    log "Creating user ${DEPLOY_USER}..."
    useradd -m -s /bin/bash "${DEPLOY_USER}"
  fi

  usermod -aG docker "${DEPLOY_USER}"

  if [[ -f "${DEPLOY_PUBKEY_FILE}" ]]; then
    log "Installing deploy SSH key for ${DEPLOY_USER}..."
    install -d -m 700 -o "${DEPLOY_USER}" -g "${DEPLOY_USER}" "/home/${DEPLOY_USER}/.ssh"
    install -m 600 -o "${DEPLOY_USER}" -g "${DEPLOY_USER}" \
      "${DEPLOY_PUBKEY_FILE}" "/home/${DEPLOY_USER}/.ssh/authorized_keys"
  else
    log "No ${DEPLOY_PUBKEY_FILE} — skip deploy authorized_keys (add manually in task 14)"
  fi
}

setup_app_dir() {
  log "Preparing ${APP_DIR}..."
  install -d -m 755 "${APP_DIR}"
  chown "${DEPLOY_USER}:${DEPLOY_USER}" "${APP_DIR}"
}

setup_ufw() {
  log "Configuring ufw (22, 3000, 8000)..."
  ufw default deny incoming
  ufw default allow outgoing
  ufw allow 22/tcp comment 'SSH'
  ufw allow 8000/tcp comment 'diaai backend'
  ufw allow 3000/tcp comment 'diaai web'
  ufw --force enable
  ufw status verbose || true
}

verify() {
  log "Verify..."
  docker --version
  docker compose version
  git --version
  curl --version | head -1
  id "${DEPLOY_USER}"
  groups "${DEPLOY_USER}"
  log "Done."
}

main() {
  require_root
  install_base_packages
  install_docker
  setup_deploy_user
  setup_app_dir
  setup_ufw
  verify
}

main "$@"
