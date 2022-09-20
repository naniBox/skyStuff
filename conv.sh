#!/usr/local/bin/bash

gm convert -quality 92 "$1" "${1%.*}.jpg"
