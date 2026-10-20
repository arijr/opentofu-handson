#!/usr/bin/env sh
set -eu
project_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

if [ "${1-}" != "--destroy" ]; then
  printf 'Nenhum recurso foi removido.\n'
  printf 'Para destruir somente o state deste projeto, execute: %s --destroy\n' "$0"
  exit 0
fi

printf 'Isso destruirá os recursos gerenciados pelo state em %s/infra.\n' "$project_root"
printf 'Digite DESTROY para confirmar: '
read -r confirmation
if [ "$confirmation" != "DESTROY" ]; then
  printf 'Cancelado; nenhum recurso foi alterado.\n'
  exit 1
fi

tofu -chdir="$project_root/infra" destroy
docker compose -f "$project_root/docker-compose.yml" down
