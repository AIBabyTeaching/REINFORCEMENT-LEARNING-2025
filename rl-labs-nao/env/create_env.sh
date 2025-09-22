#!/usr/bin/env bash
set -euo pipefail
NAME=${1:-rl-labs-nao}
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$ROOT_DIR/.venv/$NAME"

python3.11 -m venv "$VENV_DIR"
# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip
pip install -r "$ROOT_DIR/requirements.txt"
python -m ipykernel install --user --name "$NAME" --display-name "RL Labs (py311)"
echo "Environment '$NAME' ready. Activate with: source $VENV_DIR/bin/activate"
