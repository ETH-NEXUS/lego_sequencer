#!/bin/sh
# entrypoint.sh
# Reloadable PID 1 for Waitress/Flask
# Compatible with busybox /bin/sh (no wait -n)

set -u

export FLASK_APP=sequencer
export FLASK_ENV=development

CHILD=""
RELOAD=0
SHUTDOWN=0

start() {
  echo "[entrypoint] starting waitress..."
  # Launch in background and capture PID
  pipenv run python waitress_server.py &
  CHILD=$!
  echo "[entrypoint] waitress pid: $CHILD"
}

stop() {
  if [ -n "${CHILD}" ] && kill -0 "$CHILD" 2>/dev/null; then
    echo "[entrypoint] stopping waitress (pid $CHILD)..."
    # Graceful stop; Waitress traps TERM and exits
    kill -TERM "$CHILD"
    # Do NOT let a failing wait kill PID1 — swallow status
    wait "$CHILD" || true
  fi
}

on_hup() {
  echo "[entrypoint] HUP received: scheduling reload"
  RELOAD=1
  # Ask child to exit; the main loop will see wait() return and restart
  stop
}

on_term() {
  echo "[entrypoint] TERM/INT received: shutting down"
  SHUTDOWN=1
  stop
  exit 0
}

trap on_hup HUP
trap on_term TERM INT

start

# Control loop: always wait on current CHILD.
# If it exits because of reload, start again.
# If it crashes, auto-restart (dev-friendly).
while :; do
  # wait returns child's exit code; don't let a nonzero code kill PID1
  wait "$CHILD" || true
  if [ "$SHUTDOWN" -eq 1 ]; then
    exit 0
  fi
  if [ "$RELOAD" -eq 1 ]; then
    RELOAD=0
    echo "[entrypoint] reload: starting new waitress"
    start
    continue
  fi
  echo "[entrypoint] waitress exited unexpectedly; restarting in 1s..."
  sleep 1
  start
done
