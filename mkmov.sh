#!/usr/local/bin/bash

INLIST=$1
OUTMOV="${INLIST%%.*}.mp4"
echo Inlist: ${INLIST}
echo Outmov: ${OUTMOV}

ffmpeg -f concat -safe 0 -i ${INLIST} -movflags +faststart -preset slow -crf 20 -c:v libx264 ${OUTMOV}
