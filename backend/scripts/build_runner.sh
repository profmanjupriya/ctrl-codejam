#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
IMAGE_NAME="codeblitz-runner:latest"

echo "Building runner image (${IMAGE_NAME}) from ${BACKEND_DIR} ..."
cd "${BACKEND_DIR}"
docker build -t "${IMAGE_NAME}" -f Dockerfile.runner .

echo "Verifying image exists..."
if ! docker images --format '{{.Repository}}:{{.Tag}}' | grep -q "^codeblitz-runner:latest$"; then
  echo "FAIL: Image ${IMAGE_NAME} not found after build."
  exit 1
fi

echo "Smoke test: run Python in container (--network none)..."
if ! docker run --rm --network none "${IMAGE_NAME}" python3 -c "print(42)"; then
  echo "FAIL: Smoke test failed."
  exit 1
fi

echo "SUCCESS: Runner image built and verified."
