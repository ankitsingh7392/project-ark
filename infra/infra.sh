#!/usr/bin/env bash
# infra.sh — project infrastructure manager
# Add a new service by dropping a docker-compose.yml + .env.example into infra/<service>/

set -euo pipefail

INFRA_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SECRETS_DIR="${HOME}/.secrets"
SECRETS_ENV="${SECRETS_DIR}/.env"

# ─── colours ───────────────────────────────────────────────────────────────
RED='\033[0;31m'; YELLOW='\033[1;33m'; GREEN='\033[0;32m'
CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

info()    { printf "${CYAN}  →${RESET} %s\n" "$*"; }
success() { printf "${GREEN}  ✓${RESET} %s\n" "$*"; }
warn()    { printf "${YELLOW}  !${RESET} %s\n" "$*"; }
error()   { printf "${RED}  ✗${RESET} %s\n" "$*" >&2; }
header()  { printf "\n${BOLD}==> %s${RESET}\n" "$*"; }

# ─── secrets / .env helpers ────────────────────────────────────────────────

_init_secrets_dir() {
    mkdir -p "$SECRETS_DIR"
    chmod 700 "$SECRETS_DIR"
    touch "$SECRETS_ENV"
    chmod 600 "$SECRETS_ENV"
}

# Load the global secrets file into the current shell (silent — no set -a noise)
_load_secrets() {
    [[ -f "$SECRETS_ENV" ]] || return 0
    while IFS= read -r line || [[ -n "$line" ]]; do
        [[ "$line" =~ ^#.*$|^[[:space:]]*$ ]] && continue
        local key="${line%%=*}"
        # Only set if not already exported (local .env takes precedence)
        [[ -z "${!key+x}" ]] && export "${line?}"
    done < "$SECRETS_ENV"
}

# Upsert a key=value into the global secrets file
_save_secret() {
    local key="$1" value="$2"
    _init_secrets_dir
    local filtered
    filtered="$(grep -v "^${key}=" "$SECRETS_ENV" 2>/dev/null || true)"
    # Write filtered content (may be empty) then append new entry
    printf '%s\n' "$filtered" > "$SECRETS_ENV"
    printf '%s=%s\n' "$key" "$value" >> "$SECRETS_ENV"
    # Trim leading blank line that printf can leave when filtered is empty
    sed -i '' '/^[[:space:]]*$/d' "$SECRETS_ENV" 2>/dev/null || \
        sed -i '/^[[:space:]]*$/d' "$SECRETS_ENV"
    chmod 600 "$SECRETS_ENV"
}

# Returns true if the key name looks sensitive (mask input)
_is_sensitive() { [[ "$1" =~ (PASSWORD|SECRET|TOKEN|KEY|PASS) ]]; }

# Ensure every var declared in .env.example is set; prompt if missing.
# Writes the resolved values to infra/<service>/.env and $HOME/.secrets/.env.
ensure_credentials() {
    local service_dir="$1"
    local env_example="${service_dir}/.env.example"
    local env_file="${service_dir}/.env"

    [[ -f "$env_example" ]] || return 0

    # Precedence: existing service .env > global secrets > prompt
    _load_secrets
    if [[ -f "$env_file" ]]; then
        while IFS= read -r line || [[ -n "$line" ]]; do
            [[ "$line" =~ ^#.*$|^[[:space:]]*$ ]] && continue
            export "${line?}"   # service .env wins
        done < "$env_file"
    fi

    local any_prompted=false

    while IFS= read -r line || [[ -n "$line" ]]; do
        [[ "$line" =~ ^#.*$|^[[:space:]]*$ ]] && continue
        local key="${line%%=*}"
        local default_val="${line#*=}"

        if [[ -z "${!key+x}" || -z "${!key}" ]]; then
            any_prompted=true
            local input=""
            if _is_sensitive "$key"; then
                read -rsp "  ${BOLD}${key}${RESET} (sensitive, default hidden): " input
                echo
                [[ -z "$input" && -n "$default_val" ]] && input="$default_val"
            else
                read -rp "  ${BOLD}${key}${RESET} [${default_val}]: " input
                [[ -z "$input" ]] && input="$default_val"
            fi
            export "${key}=${input}"
            _save_secret "$key" "$input"
        fi
    done < "$env_example"

    # Always (re)write the service .env so it stays in sync
    {
        while IFS= read -r line || [[ -n "$line" ]]; do
            [[ "$line" =~ ^#.*$|^[[:space:]]*$ ]] && continue
            local key="${line%%=*}"
            printf '%s=%s\n' "$key" "${!key}"
        done < "$env_example"
    } > "$env_file"
    chmod 600 "$env_file"

    $any_prompted && success "Credentials saved to ${env_file} and ${SECRETS_ENV}"
}

# ─── service discovery ─────────────────────────────────────────────────────

discover_services() {
    local services=()
    for dir in "${INFRA_DIR}"/*/; do
        [[ -f "${dir}docker-compose.yml" ]] && services+=("$(basename "$dir")")
    done
    printf '%s\n' "${services[@]:-}"
}

resolve_services() {
    # If caller passed explicit names, validate them; otherwise use all discovered.
    if [[ $# -gt 0 ]]; then
        for svc in "$@"; do
            if [[ ! -f "${INFRA_DIR}/${svc}/docker-compose.yml" ]]; then
                error "Unknown service: ${svc}"
                printf "  Available: %s\n" "$(discover_services | tr '\n' ',' | sed 's/,$//')"
                exit 1
            fi
        done
        printf '%s\n' "$@"
    else
        discover_services
    fi
}

# ─── commands ──────────────────────────────────────────────────────────────

cmd_up() {
    local services
    mapfile -t services < <(resolve_services "$@")

    for svc in "${services[@]}"; do
        local dir="${INFRA_DIR}/${svc}"
        header "Starting: ${svc}"
        ensure_credentials "$dir"
        info "Launching containers…"
        docker compose -f "${dir}/docker-compose.yml" up -d
        success "${svc} is up"
    done
}

cmd_down() {
    local services
    mapfile -t services < <(resolve_services "$@")

    for svc in "${services[@]}"; do
        local dir="${INFRA_DIR}/${svc}"
        header "Stopping: ${svc}"
        docker compose -f "${dir}/docker-compose.yml" down
        success "${svc} is down"
    done
}

cmd_restart() {
    local services
    mapfile -t services < <(resolve_services "$@")
    cmd_down "${services[@]}"
    cmd_up   "${services[@]}"
}

cmd_status() {
    local services
    mapfile -t services < <(resolve_services "$@")

    for svc in "${services[@]}"; do
        header "Status: ${svc}"
        docker compose -f "${INFRA_DIR}/${svc}/docker-compose.yml" ps
    done
}

cmd_logs() {
    # logs always targets a single service (or first one)
    local svc="${1:-}"
    if [[ -z "$svc" ]]; then
        error "Specify a service: $0 logs <service>"
        exit 1
    fi
    [[ ! -f "${INFRA_DIR}/${svc}/docker-compose.yml" ]] && { error "Unknown service: ${svc}"; exit 1; }
    docker compose -f "${INFRA_DIR}/${svc}/docker-compose.yml" logs -f "${@:2}"
}

# ─── usage ─────────────────────────────────────────────────────────────────

usage() {
    printf '%s — project infrastructure manager\n\n' "${BOLD}infra.sh${RESET}"
    printf "Usage: %s <command> [service...]\n\n" "$0"
    printf "Commands:\n"
    printf "  %-18s %s\n" "up [svc...]"      "Start services and prompt for missing credentials"
    printf "  %-18s %s\n" "down [svc...]"    "Stop and remove containers"
    printf "  %-18s %s\n" "restart [svc...]" "Stop then start"
    printf "  %-18s %s\n" "status [svc...]"  "Show container status"
    printf "  %-18s %s\n" "logs <svc>"       "Follow logs for a service"
    printf "\n"
    local svcs
    svcs="$(discover_services | tr '\n' ',' | sed 's/,$//' || echo '(none found)')"
    printf "Discovered services: %s\n" "$svcs"
    printf "\nCredentials are read from (in order of precedence):\n"
    printf "  1. infra/<service>/.env\n"
    printf "  2. %s\n" "$SECRETS_ENV"
    printf "  3. Interactive prompt (saved to both locations above)\n"
}

# ─── entrypoint ────────────────────────────────────────────────────────────

COMMAND="${1:-help}"
shift || true

case "$COMMAND" in
    up)       cmd_up      "$@" ;;
    down)     cmd_down    "$@" ;;
    restart)  cmd_restart "$@" ;;
    status)   cmd_status  "$@" ;;
    logs)     cmd_logs    "$@" ;;
    help|--help|-h) usage ;;
    *)
        error "Unknown command: ${COMMAND}"
        usage
        exit 1
        ;;
esac
