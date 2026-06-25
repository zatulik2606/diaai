#!/usr/bin/env bash
# Bootstrap Timeweb VPS for GlitchTip (Docker + ufw).
# Ubuntu 24.04+ · run as root · idempotent.
#
# Usage:
#   scp devops/glitchtip/bootstrap-timeweb.sh root@GLITCHTIP_IP:/tmp/
#   ssh root@GLITCHTIP_IP \
#     'DIAAPP_IP=201.51.4.34 ADMIN_IP=YOUR_HOME_IP bash /tmp/bootstrap-timeweb.sh'

set -euo pipefail

GLITCHTIP_DIR="${GLITCHTIP_DIR:-/opt/diaai/devops/glitchtip}"
DIAAPP_IP="${DIAAPP_IP:-201.51.4.34}"
ADMIN_IP="${ADMIN_IP:-}"
SWAP_GB="${SWAP_GB:-2}"

log() { echo "[glitchtip-bootstrap] $*"; }

require_root() {
  [[ "${EUID:-$(id -u)}" -eq 0 ]] || {
    echo "Run as root" >&2
    exit 1
  }
}

install_base_packages() {
  export DEBIAN_FRONTEND=noninteractive
  apt-get update -qq
  apt-get install -y -qq ca-certificates curl git make ufw gnupg lsb-release openssl
}

setup_swap() {
  if [[ -f /swapfile ]] || swapon --show 2>/dev/null | grep -q /swapfile; then
    return
  fi
  log "Adding ${SWAP_GB}G swap..."
  fallocate -l "${SWAP_GB}G" /swapfile
  chmod 600 /swapfile
  mkswap /swapfile
  swapon /swapfile
  grep -q '/swapfile' /etc/fstab || echo '/swapfile none swap sw 0 0' >> /etc/fstab
}

install_docker() {
  if command -v docker >/dev/null 2>&1; then
    log "Docker: $(docker --version)"
  else
    curl -fsSL https://get.docker.com | sh
  fi
  systemctl enable docker
  systemctl start docker
  docker compose version
}

setup_ufw() {
  ufw default deny incoming
  ufw default allow outgoing
  ufw allow 22/tcp comment 'SSH'
  if [[ -n "${DIAAPP_IP}" ]]; then
    ufw allow from "${DIAAPP_IP}" to any port 8000 proto tcp comment 'diaai-prod ingest'
  fi
  if [[ -n "${ADMIN_IP}" ]]; then
    ufw allow from "${ADMIN_IP}" to any port 8000 proto tcp comment 'admin UI'
  fi
  if [[ -z "${ADMIN_IP}" ]]; then
    log "WARN: ADMIN_IP unset — UI only from allowed IPs; set ADMIN_IP for browser access" >&2
  fi
  ufw --force enable
  ufw status verbose || true
}

verify() {
  free -h
  log "Next: clone /opt/diaai, configure devops/glitchtip/.env — see timeweb-deploy.md"
}

main() {
  require_root
  install_base_packages
  setup_swap
  install_docker
  setup_ufw
  verify
}

main "$@"
