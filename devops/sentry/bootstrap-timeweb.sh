#!/usr/bin/env bash
# Bootstrap Timeweb VPS for self-hosted Sentry (Docker + ufw).
# Ubuntu 24.04+ · run as root · idempotent.
#
# Usage:
#   scp devops/sentry/bootstrap-timeweb.sh root@SENTRY_IP:/tmp/
#   ssh root@SENTRY_IP 'DIAAPP_IP=201.51.4.34 ADMIN_IP=YOUR_HOME_IP bash /tmp/bootstrap-timeweb.sh'
#
# DIAAPP_IP — diaai-prod may send events to :9000
# ADMIN_IP  — your IP for Sentry UI (optional; omit to open 9000 to world — not recommended)

set -euo pipefail

SENTRY_DIR="${SENTRY_DIR:-/opt/sentry-self-hosted}"
DIAAPP_IP="${DIAAPP_IP:-}"
ADMIN_IP="${ADMIN_IP:-}"
SWAP_GB="${SWAP_GB:-4}"

log() { echo "[sentry-bootstrap] $*"; }

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
    lsb-release \
    python3
}

setup_swap() {
  if [[ -f /swapfile ]] || swapon --show | grep -q /swapfile; then
    log "Swap already configured"
    return
  fi
  log "Adding ${SWAP_GB}G swap (recommended for 8 GB RAM)..."
  fallocate -l "${SWAP_GB}G" /swapfile
  chmod 600 /swapfile
  mkswap /swapfile
  swapon /swapfile
  grep -q '/swapfile' /etc/fstab || echo '/swapfile none swap sw 0 0' >> /etc/fstab
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
  docker compose version
}

setup_sentry_dir() {
  log "Preparing ${SENTRY_DIR}..."
  install -d -m 755 "${SENTRY_DIR}"
}

setup_ufw() {
  log "Configuring ufw..."
  ufw default deny incoming
  ufw default allow outgoing
  ufw allow 22/tcp comment 'SSH'

  if [[ -n "${DIAAPP_IP}" ]]; then
    ufw allow from "${DIAAPP_IP}" to any port 9000 proto tcp comment 'diaai-prod ingest'
  fi
  if [[ -n "${ADMIN_IP}" ]]; then
    ufw allow from "${ADMIN_IP}" to any port 9000 proto tcp comment 'admin UI'
  fi
  if [[ -z "${DIAAPP_IP}" && -z "${ADMIN_IP}" ]]; then
    log "WARN: DIAAPP_IP and ADMIN_IP unset — opening 9000/tcp to all (insecure)" >&2
    ufw allow 9000/tcp comment 'Sentry UI+ingest'
  fi

  ufw --force enable
  ufw status verbose || true
}

verify() {
  docker --version
  docker compose version
  free -h
  swapon --show || true
  log "Next: clone self-hosted into ${SENTRY_DIR} — see devops/sentry/timeweb-deploy.md"
}

main() {
  require_root
  install_base_packages
  setup_swap
  install_docker
  setup_sentry_dir
  setup_ufw
  verify
}

main "$@"
