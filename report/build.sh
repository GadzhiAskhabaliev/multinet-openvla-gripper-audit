#!/bin/sh
# Rebuild the PDF report: figure from the archived predictions, then HTML -> PDF with headless Chrome.
set -e
cd "$(dirname "$0")"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
python3 figure.py
"$CHROME" --headless --disable-gpu --no-pdf-header-footer \
    --print-to-pdf="$PWD/multinet_gripper_audit.pdf" "file://$PWD/report.html" 2>/dev/null
echo "$PWD/multinet_gripper_audit.pdf"
