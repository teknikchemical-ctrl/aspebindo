#!/bin/bash
# usage: deck/render.sh [ONLY=1,2]  -> builds pptx, converts pdf, rasterises to scratch
cd /home/user/aspebindo
SK=/root/.claude/skills/synced/1447d632-3db4-4ffa-8639-0456923eecc3_b47be9f3-76fa-4276-9bf3-c539adcfb469/pptx
SCR=/tmp/claude-0/-home-user-aspebindo/77813a14-c1d4-514f-9bb7-a673f40e188a/scratchpad
export NODE_PATH=$SCR/nodeenv/node_modules
export DECK_OUT=${DECK_OUT:-test.pptx}
node deck/build.js || exit 1
cd deck && python3 $SK/scripts/office/soffice.py --headless --convert-to pdf $DECK_OUT >/dev/null 2>&1
rm -f $SCR/r-*.png; pdftoppm -r ${DPI:-110} -png ${DECK_OUT%.pptx}.pdf $SCR/r
ls $SCR/r-*.png
