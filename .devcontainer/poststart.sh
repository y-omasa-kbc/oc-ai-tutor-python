#!/bin/bash
set +e

LOG=/tmp/poststart.log
echo "[poststart] $(date -Iseconds) START" > "$LOG"

if pgrep -f "streamlit run app/web/main.py" > /dev/null; then
  echo "[poststart] streamlit already running, skip" >> "$LOG"
else
  echo "[poststart] ---- start streamlit ----" >> "$LOG"
  nohup python -m streamlit run app/web/main.py \
    --server.address=0.0.0.0 \
    --server.port=8501 \
    --server.runOnSave=true \
    > /tmp/streamlit.log 2>&1 &
  echo "[poststart] streamlit PID=$!" >> "$LOG"
fi

if pgrep -f "http.server 8502" > /dev/null; then
  echo "[poststart] http server already running, skip" >> "$LOG"
else
  echo "[poststart] ---- start textbook http server (port 8502) ----" >> "$LOG"
  nohup python -m http.server 8502 \
    --directory /workspace/app/static/textbook \
    --bind 0.0.0.0 \
    > /tmp/http_server.log 2>&1 &
  echo "[poststart] http server PID=$!" >> "$LOG"
fi

echo "[poststart] waiting 5s for servers to bind..." >> "$LOG"
sleep 5

if curl -sf http://localhost:8501/_stcore/health > /dev/null; then
  echo "[poststart] streamlit is alive" >> "$LOG"
else
  echo "[poststart] streamlit did not respond, log follows:" >> "$LOG"
  cat /tmp/streamlit.log >> "$LOG" 2>/dev/null
fi

if curl -sf -o /dev/null http://localhost:8502/; then
  echo "[poststart] http server is alive" >> "$LOG"
else
  echo "[poststart] http server did not respond, log follows:" >> "$LOG"
  cat /tmp/http_server.log >> "$LOG" 2>/dev/null
fi

echo "[poststart] DONE" >> "$LOG"
exit 0
