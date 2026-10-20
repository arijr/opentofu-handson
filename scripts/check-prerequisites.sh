#!/usr/bin/env sh
set -eu

missing=0
for command_name in tofu docker git curl; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    printf 'ERRO: ferramenta ausente: %s\n' "$command_name" >&2
    missing=1
  fi
done

if command -v docker >/dev/null 2>&1; then
  if ! docker compose version >/dev/null 2>&1; then
    printf 'ERRO: Docker Compose v2 não está disponível.\n' >&2
    missing=1
  fi
fi

if [ "$missing" -ne 0 ]; then
  printf 'Instale as ferramentas ausentes conforme docs/pre-requisitos.md.\n' >&2
  exit 1
fi

printf 'Pré-requisitos encontrados:\n'
tofu version
docker compose version
git --version
curl --version | head -n 1
