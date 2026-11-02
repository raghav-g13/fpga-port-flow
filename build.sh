#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE_TAG="${IMAGE_TAG:-ghcr.io/ucb-bar/chia-v80-chipyard:latest}"

docker buildx build \
    --network=host \
    -f "$SCRIPT_DIR/V80ChipyardDockerfile" \
    -t "$IMAGE_TAG" \
    "$SCRIPT_DIR"
