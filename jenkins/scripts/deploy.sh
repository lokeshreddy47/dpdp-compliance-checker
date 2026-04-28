#!/bin/bash
# Standalone deployment helper

set -e

echo "========================================"
echo "DPDP Compliance Checker - Deploy Script"
echo "========================================"

# Pull latest code
git pull origin main

# Build and start
docker compose down -v || true
docker compose up -d --build

# Wait for startup
sleep 10

# Health check
./jenkins/scripts/health-check.sh

echo ""
echo "✅ Deployment complete!"

