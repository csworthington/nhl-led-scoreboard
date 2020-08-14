#!/bin/bash

# Make script work regardless of where it is run from
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "${DIR}/.."

# start python virtualenv
source ./nhl-scoreboard/bin/activate

sudo python3 src/main.py --led-gpio-mapping=regular --led-slowdown-gpio=4 --led-brightness=20