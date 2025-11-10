#!/bin/bash
# RStudio Container Management Script

# This script provides common operations for managing your RStudio container
# Usage: ./rstudio_ops.sh [command]
# Commands: start, stop, restart, logs, exec, status, cleanup

set -e  # Exit on any error

# Default values - these can be overridden
CONTAINER_NAME="${RSTUDIO_CONTAINER_NAME:-rstudio-server}"
COMPOSE_FILE="${RSTUDIO_COMPOSE_FILE:-docker-compose.yml}"
IMAGE_NAME="${RSTUDIO_IMAGE_NAME:-rstudio-image:latest}"

show_help() {
    echo "RStudio Container Management Script"
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  start     - Start the RStudio container"
    echo "  stop      - Stop the RStudio container"
    echo "  restart   - Restart the RStudio container"
    echo "  logs      - View container logs (follow mode)"
    echo "  logs-tail - View last 100 lines of logs"
    echo "  exec      - Execute a command in the container (default: bash shell)"
    echo "  status    - Check container status"
    echo "  cleanup   - Stop and remove container and images"
    echo "  build     - Rebuild the container"
    echo ""
    echo "Environment Variables:"
    echo "  RSTUDIO_CONTAINER_NAME - Container name (default: rstudio-server)"
    echo "  RSTUDIO_COMPOSE_FILE   - Compose file path (default: docker-compose.yml)"
    echo "  RSTUDIO_IMAGE_NAME     - Image name (default: rstudio-image:latest)"
    echo ""
}

start_container() {
    echo "Starting RStudio container..."
    if [ -f "$COMPOSE_FILE" ]; then
        docker-compose -f "$COMPOSE_FILE" up -d
    else
        echo "Compose file $COMPOSE_FILE not found!"
        exit 1
    fi
    echo "RStudio container started!"
    echo "Access at: http://localhost:8787 (or the port you configured)"
}

stop_container() {
    echo "Stopping RStudio container..."
    if [ -f "$COMPOSE_FILE" ]; then
        docker-compose -f "$COMPOSE_FILE" down
    else
        docker stop "$CONTAINER_NAME" 2>/dev/null || echo "Container not found or already stopped"
    fi
    echo "RStudio container stopped!"
}

restart_container() {
    stop_container
    sleep 2
    start_container
}

view_logs() {
    if [ -f "$COMPOSE_FILE" ]; then
        docker-compose -f "$COMPOSE_FILE" logs -f
    else
        docker logs -f "$CONTAINER_NAME"
    fi
}

view_logs_tail() {
    if [ -f "$COMPOSE_FILE" ]; then
        docker-compose -f "$COMPOSE_FILE" logs --tail=100
    else
        docker logs --tail=100 "$CONTAINER_NAME"
    fi
}

exec_container() {
    CMD="${1:-/bin/bash}"
    echo "Executing command in RStudio container: $CMD"
    docker exec -it "$CONTAINER_NAME" $CMD
}

check_status() {
    echo "Checking RStudio container status..."
    docker ps -a | grep "$CONTAINER_NAME" || echo "Container $CONTAINER_NAME not found"
}

rebuild_image() {
    echo "Rebuilding RStudio container image..."
    if [ -f "$COMPOSE_FILE" ]; then
        docker-compose -f "$COMPOSE_FILE" build --no-cache
    else
        echo "Compose file required for rebuild"
        exit 1
    fi
    echo "Image rebuilt successfully!"
}

cleanup() {
    echo "Cleaning up RStudio containers and images..."
    
    # Stop any running containers
    if [ -f "$COMPOSE_FILE" ]; then
        docker-compose -f "$COMPOSE_FILE" down
    else
        docker stop "$CONTAINER_NAME" 2>/dev/null || echo "Container not running"
    fi
    
    # Remove containers
    docker rm -f $(docker ps -aq --filter "name=$CONTAINER_NAME") 2>/dev/null || echo "No containers to remove"
    
    # Remove images (optional - comment out if you don't want to remove images)
    # docker rmi -f $(docker images --filter "reference=$IMAGE_NAME" -q) 2>/dev/null || echo "No images to remove"
    
    # Remove volumes (optional - be careful with this)
    # docker volume prune -f
    
    echo "Cleanup completed!"
}

# Main script logic
case "${1:-help}" in
    "start")
        start_container
        ;;
    "stop")
        stop_container
        ;;
    "restart")
        restart_container
        ;;
    "logs")
        view_logs
        ;;
    "logs-tail")
        view_logs_tail
        ;;
    "exec")
        exec_container "${2}"
        ;;
    "status")
        check_status
        ;;
    "cleanup")
        cleanup
        ;;
    "build")
        rebuild_image
        ;;
    "help"|"-h"|"--help"|"")
        show_help
        ;;
    *)
        echo "Unknown command: $1"
        show_help
        exit 1
        ;;
esac