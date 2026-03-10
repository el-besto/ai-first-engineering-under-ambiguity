#!/usr/bin/env bash
set -euo pipefail

RD_BIN_DIR="${HOME}/.rd/bin"
DOCKER_PLUGIN_DIR="${HOME}/.docker/cli-plugins"
BUILDX_TARGET="${RD_BIN_DIR}/docker-buildx"
COMPOSE_TARGET="${RD_BIN_DIR}/docker-compose"

if ! command -v rdctl >/dev/null 2>&1; then
  echo "rdctl not found in PATH. Install/start Rancher Desktop first." >&2
  exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "docker CLI not found in PATH." >&2
  exit 1
fi

if [[ ! -x "${BUILDX_TARGET}" ]]; then
  echo "Missing Rancher Desktop plugin: ${BUILDX_TARGET}" >&2
  exit 1
fi

if [[ ! -x "${COMPOSE_TARGET}" ]]; then
  echo "Missing Rancher Desktop plugin: ${COMPOSE_TARGET}" >&2
  exit 1
fi

mkdir -p "${DOCKER_PLUGIN_DIR}"
ln -snf "${BUILDX_TARGET}" "${DOCKER_PLUGIN_DIR}/docker-buildx"
ln -snf "${COMPOSE_TARGET}" "${DOCKER_PLUGIN_DIR}/docker-compose"

echo "Docker CLI plugins updated to Rancher Desktop binaries:"
readlink "${DOCKER_PLUGIN_DIR}/docker-buildx"
readlink "${DOCKER_PLUGIN_DIR}/docker-compose"

if docker context ls --format '{{.Name}}' | grep -qx 'rancher-desktop'; then
  docker context use rancher-desktop >/dev/null
  echo "Active Docker context: $(docker context show)"
else
  echo "rancher-desktop context not found; leaving current context unchanged." >&2
fi

echo "buildx: $(docker buildx version | head -n1)"
echo "compose: $(docker compose version | head -n1)"
