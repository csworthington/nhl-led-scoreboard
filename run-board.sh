#!/bin/bash

sudo python3 src/main.py \
--led-gpio-mapping=regular \
--led-brightness=30 \
--led-slowdown-gpio=4 \
--led-cols=64