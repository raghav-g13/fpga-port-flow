#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE_TAG="${IMAGE_TAG:-ghcr.io/ucb-bar/chia-v80-chipyard:latest}"
FIRESIM_DIR="${FIRESIM_DIR:-$SCRIPT_DIR/firesim}"

docker run --rm \
    -v "$FIRESIM_DIR":/home/ray/chipyard/sims/firesim \
    "$IMAGE_TAG" \
    "$@"
