#!/bin/bash
set +e

LOG=/tmp/postcreate.log
echo "[postcreate] $(date -Iseconds) START" > "$LOG"

echo "[postcreate] cwd=$(pwd)" >> "$LOG"
echo "[postcreate] whoami=$(whoami)" >> "$LOG"
echo "[postcreate] PATH=$PATH" >> "$LOG"

echo "[postcreate] python: $(command -v python)" >> "$LOG"
python --version >> "$LOG" 2>&1

echo "[postcreate] ---- check imports ----" >> "$LOG"
python -c "import numpy, streamlit, sentence_transformers" >> "$LOG" 2>&1
RC=$?
echo "[postcreate] imports RC=$RC" >> "$LOG"
if [ $RC -ne 0 ]; then
  echo "[postcreate] WARN: missing python packages, skipping index build" >> "$LOG"
else
  echo "[postcreate] ---- build index ----" >> "$LOG"
  python -m app.data.index >> "$LOG" 2>&1
  RC=$?
  echo "[postcreate] index RC=$RC" >> "$LOG"
fi

echo "[postcreate] ---- start streamlit ----" >> "$LOG"
nohup python -m streamlit run app/web/main.py \
  --server.address=0.0.0.0 \
  --server.port=8501 \
  --server.runOnSave=true \
  > /tmp/streamlit.log 2>&1 &
PID=$!
echo "[postcreate] streamlit PID=$PID" >> "$LOG"

echo "[postcreate] ---- start textbook http server (port 8502) ----" >> "$LOG"
nohup python -m http.server 8502 \
  --directory /workspace/app/static/textbook \
  --bind 0.0.0.0 \
  > /tmp/http_server.log 2>&1 &
HTTP_PID=$!
echo "[postcreate] http server PID=$HTTP_PID" >> "$LOG"

echo "[postcreate] waiting 5s for servers to bind..." >> "$LOG"
sleep 5

if kill -0 "$PID" 2>/dev/null; then
  echo "[postcreate] streamlit is alive" >> "$LOG"
else
  echo "[postcreate] streamlit died, log follows:" >> "$LOG"
  cat /tmp/streamlit.log >> "$LOG" 2>/dev/null
fi

if kill -0 "$HTTP_PID" 2>/dev/null; then
  echo "[postcreate] http server is alive" >> "$LOG"
else
  echo "[postcreate] http server died, log follows:" >> "$LOG"
  cat /tmp/http_server.log >> "$LOG" 2>/dev/null
fi

echo "[postcreate] DONE" >> "$LOG"
exit 0
