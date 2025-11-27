#!/bin/zsh
# Application startup script

set -e

echo "Setting up virtual environment and installing dependencies..."
uv sync --all-extras --no-install-project
source .venv/bin/activate

# echo "Loading .env secrets"
# if [ -f .env ]; then
  # set -a   # Automatically export all variables
  # source .env || true   # source the file
  # set +a     # turn it off again
# else 
  # echo ".env not found, continuing without secrets..."
# fi

echo "Reading configurations..."
CONFIG_FILE="config.toml"

PORT=$(uv run python - <<'PY'
import toml, sys
try:
  data = toml.load(open("config.toml"))
  print(data.get("app", {}).get("PORT", 8080))
except Exception as e:
  print(f"Error reading config.toml: {e}", file=sys.stderr)
  sys.exit(1)  
PY
)

HOST=$(uv run python - <<'PY'
import toml, sys
try:
  data = toml.load(open("config.toml"))
  print(data.get("app", {}).get("HOST", "0.0.0.0"))
except Exception as e:
  print(f"Error reading config.toml: {e}", file=sys.stderr)
  sys.exit(1)  
PY
)


echo "Starting Sanic at http://$HOST:$PORT"
echo "Starting Celery worker..."

uv run sanic src.main:create_app \
  --host="$HOST" \
  --port="$PORT" \
  --workers=2 \
  --access-log \
  --reload \
  -R src/ \
  -R config.toml \
  --dev

SANIC_PID=$!

# Start celery
uv run celery -A src.services.celery_app:app worker --logleve=info concurrency=8 &

CELERY_PID =$!

echo "SANIC PID: $SANIC_PID"
echo "CELERY PID: $CELERY_PID"
echo "Stop with Ctrl+C or: kill $SANIC_PID $CELERY_PID"

# Keep script alive and forward Ctrl-C to both processes
trap "echo 'Shutting down...'; kill $SANIC_PID $CELERY_PID2>dev/null; wait" SIGINT SIGTERM

wait
