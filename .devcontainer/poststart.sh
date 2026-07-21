#!/bin/bash
set +e

LOG=/tmp/poststart.log
echo "[poststart] $(date -Iseconds) START" > "$LOG"

if curl -sf http://localhost:8501/_stcore/health > /dev/null; then
  echo "[poststart] streamlit is healthy, skip" >> "$LOG"
else
  echo "[poststart] ---- (re)start streamlit ----" >> "$LOG"
  pkill -f "streamlit run app/web/main.py" 2>/dev/null
  sleep 2
  nohup python -m streamlit run app/web/main.py \
    --server.address=0.0.0.0 \
    --server.port=8501 \
    --server.runOnSave=true \
    > /tmp/streamlit.log 2>&1 &
  echo "[poststart] streamlit PID=$!" >> "$LOG"
fi

if curl -sf -o /dev/null http://localhost:8502/; then
  echo "[poststart] http server is healthy, skip" >> "$LOG"
else
  echo "[poststart] ---- (re)start textbook http server (port 8502) ----" >> "$LOG"
  pkill -f "http.server 8502" 2>/dev/null
  sleep 1
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
  tail -30 /tmp/streamlit.log >> "$LOG" 2>/dev/null
fi

if curl -sf -o /dev/null http://localhost:8502/; then
  echo "[poststart] http server is alive" >> "$LOG"
else
  echo "[poststart] http server did not respond, log follows:" >> "$LOG"
  tail -30 /tmp/http_server.log >> "$LOG" 2>/dev/null
fi

echo "[poststart] DONE" >> "$LOG"
exit 0
