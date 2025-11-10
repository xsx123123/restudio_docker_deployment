#!/bin/bash
# RStudio Container Operations Helper
# This script provides common operations for a specific RStudio container
# Auto-generated based on the current directory's docker-compose.yml

COMPOSE_FILE="docker-compose.yml"

if [ ! -f "$COMPOSE_FILE" ]; then
    echo "Error: $COMPOSE_FILE not found in current directory!"
    echo "Make sure to run this script from the directory containing your docker-compose.yml"
    exit 1
fi

CONTAINER_NAME=$(docker-compose -f $COMPOSE_FILE config --services 2>/dev/null | head -n1 | xargs docker-compose -f $COMPOSE_FILE ps -q | xargs docker ps -a --format "table {{.Names}}" 2>/dev/null | sed -n '2p' 2>/dev/null)

if [ -z "$CONTAINER_NAME" ]; then
    # Get the container name from the compose file directly
    CONTAINER_NAME=$(grep -E "^\s*container_name:" $COMPOSE_FILE | head -n1 | sed 's/.*container_name:[[:space:]]*//' | xargs)
fi

if [ -z "$CONTAINER_NAME" ]; then
    echo "Error: Could not determine container name from $COMPOSE_FILE"
    exit 1
fi

show_help() {
    echo "RStudio Container Operations for: $CONTAINER_NAME"
    echo "==============================================="
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  start     - Start the RStudio container"
    echo "  stop      - Stop the RStudio container"
    echo "  restart   - Restart the RStudio container"
    echo "  logs      - View container logs (follow mode)"
    echo "  logs-tail - View last 100 lines of logs"
    echo "  exec      - Execute a bash shell in the container"
    echo "  exec-cmd  - Execute a specific command in the container"
    echo "  status    - Check container status"
    echo "  ports     - Show port mappings"
    echo "  shell     - Open a shell session in the container as the RStudio user"
    echo ""
    echo "Examples:"
    echo "  $0 start           # Start the container"
    echo "  $0 exec            # Open bash shell as root"
    echo "  $0 exec-cmd 'ls -la'  # Execute specific command"
    echo "  $0 shell           # Open shell as RStudio user"
    echo ""
}

start_container() {
    echo "Starting RStudio container: $CONTAINER_NAME"
    docker-compose -f "$COMPOSE_FILE" up -d
    if [ $? -eq 0 ]; then
        echo "RStudio container started successfully!"
        # Get the mapped port
        PORT=$(docker-compose -f "$COMPOSE_FILE" config | grep -A 10 "rstudio:" | grep "8787" | grep -oE '[0-9]+:[0-9]+' | cut -d':' -f1)
        if [ ! -z "$PORT" ]; then
            echo "Access RStudio at: http://localhost:$PORT"
        fi
    else
        echo "Failed to start container!"
        exit 1
    fi
}

stop_container() {
    echo "Stopping RStudio container: $CONTAINER_NAME"
    docker-compose -f "$COMPOSE_FILE" down
    echo "RStudio container stopped!"
}

restart_container() {
    echo "Restarting RStudio container: $CONTAINER_NAME"
    docker-compose -f "$COMPOSE_FILE" restart
}

view_logs() {
    echo "Following logs for container: $CONTAINER_NAME"
    docker-compose -f "$COMPOSE_FILE" logs -f
}

view_logs_tail() {
    echo "Last 100 log lines for container: $CONTAINER_NAME"
    docker-compose -f "$COMPOSE_FILE" logs --tail=100
}

exec_container() {
    echo "Opening bash shell in container: $CONTAINER_NAME (as root)"
    docker exec -it "$CONTAINER_NAME" /bin/bash
}

exec_command() {
    if [ -z "$2" ]; then
        echo "Error: Please specify a command to execute"
        echo "Usage: $0 exec-cmd 'command to execute'"
        exit 1
    fi
    docker exec -it "$CONTAINER_NAME" $2
}

open_user_shell() {
    # Get the default user from the container
    DEFAULT_USER=$(docker exec -i "$CONTAINER_NAME" env | grep DEFAULT_USER | cut -d'=' -f2)
    if [ -z "$DEFAULT_USER" ]; then
        DEFAULT_USER="rstudio"
    fi
    echo "Opening shell for user: $DEFAULT_USER in container: $CONTAINER_NAME"
    docker exec -it -u $DEFAULT_USER "$CONTAINER_NAME" /bin/bash
}

check_status() {
    echo "Status for RStudio container: $CONTAINER_NAME"
    docker-compose -f "$COMPOSE_FILE" ps
}

show_ports() {
    echo "Port mappings for RStudio container: $CONTAINER_NAME"
    docker port "$CONTAINER_NAME"
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
        exec_container
        ;;
    "exec-cmd")
        exec_command "$@"
        ;;
    "shell")
        open_user_shell
        ;;
    "status")
        check_status
        ;;
    "ports")
        show_ports
        ;;
    "help"|"-h"|"--help"|"")
        show_help
        ;;
    *)
        echo "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac