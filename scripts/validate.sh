#!/usr/bin/env sh
set -eu
project_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

for configuration in \
  infra \
  labs/04-state-lifecycle/lock-demo/bootstrap \
  labs/04-state-lifecycle/lock-demo/hold-lock
do
  tofu -chdir="$project_root/$configuration" fmt -check -recursive
  tofu -chdir="$project_root/$configuration" init -backend=false
  tofu -chdir="$project_root/$configuration" validate
done
