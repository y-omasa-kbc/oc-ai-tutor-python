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

echo "[postcreate] DONE" >> "$LOG"
exit 0
