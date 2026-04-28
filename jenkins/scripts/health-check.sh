#!/bin/bash
# Post-deployment health check script

BACKEND_URL="http://localhost:8000"
FRONTEND_URL="http://localhost:5173"
TIMEOUT=60
SLEEP_INTERVAL=2

wait_for_service() {
    local name=$1
    local url=$2
    local elapsed=0

    echo "Waiting for $name at $url ..."

    while [ $elapsed -lt $TIMEOUT ]; do
        if curl -sf "$url" > /dev/null 2>&1; then
            echo "✅ $name is healthy"
            return 0
        fi
        sleep $SLEEP_INTERVAL
        elapsed=$((elapsed + SLEEP_INTERVAL))
        echo "  ... ($elapsed s)"
    done

    echo "❌ $name failed to become healthy within ${TIMEOUT}s"
    return 1
}

wait_for_service "Backend" "$BACKEND_URL"
BACKEND_OK=$?

wait_for_service "Frontend" "$FRONTEND_URL"
FRONTEND_OK=$?

if [ $BACKEND_OK -eq 0 ] && [ $FRONTEND_OK -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "🎉 All services are healthy!"
    echo "Backend:  $BACKEND_URL"
    echo "Frontend: $FRONTEND_URL"
    echo "========================================"
    exit 0
else
    echo ""
    echo "========================================"
    echo "⚠️  Health check failed"
    echo "========================================"
    exit 1
fi

