#!/bin/sh
# Codex from your phone, with Puffin (Mac and Linux). Same as the website installer:
#   curl -fsSL https://raw.githubusercontent.com/justpuffin/codex-plugin/main/install.sh | bash -s -- --code ABCDE-FGHJK
# Get the code on the agent's page in Puffin: Coding from your phone > Codex > Get setup command.
set -eu
script="$(mktemp)"
trap 'rm -f "$script"' EXIT
curl -fsSL https://www.justpuffin.tech/install/codex.sh -o "$script"
sh "$script" "$@"
