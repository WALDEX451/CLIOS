#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "[CLIOS] Raspberry Pi setup starten..."

if [[ "$(id -u)" -eq 0 ]]; then
  SUDO=""
else
  SUDO="sudo"
fi

$SUDO apt-get update
$SUDO apt-get install -y \
  python3 \
  python3-pip \
  python3-venv \
  nmap \
  ufw \
  net-tools \
  iproute2 \
  wireless-tools \
  iw \
  curl \
  openssl

if [[ ! -d ".venv" ]]; then
  python3 -m venv .venv
fi

.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

chmod +x clios setup_pi.sh

if [[ ! -f "config.json" ]]; then
  .venv/bin/python - <<'PY'
from bootstrap import build_default_config
from pathlib import Path
import json

config_path = Path("config.json")
config_path.write_text(json.dumps(build_default_config(), indent=4), encoding="utf-8")
print("[CLIOS] config.json aangemaakt.")
PY
fi

cat > clios.service <<SERVICE
[Unit]
Description=CLIOS Raspberry Pi Shell
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=$SCRIPT_DIR
ExecStart=$SCRIPT_DIR/.venv/bin/python $SCRIPT_DIR/main.py
Restart=on-failure
User=$(id -un)
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
SERVICE

echo "[CLIOS] Setup klaar."
echo "[CLIOS] Start met: ./clios"
echo "[CLIOS] Optioneel autostart:"
echo "  sudo cp $SCRIPT_DIR/clios.service /etc/systemd/system/clios.service"
echo "  sudo systemctl daemon-reload"
echo "  sudo systemctl enable --now clios.service"
