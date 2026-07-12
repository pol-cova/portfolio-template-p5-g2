#!/bin/bash

DIR_PROJECT="/root/portfolio-template-p5-g2"
VENV="$DIR_PROJECT/python3-virtualenv"

cd "$DIR_PROJECT"

git fetch origin
git reset --hard origin/main

"$VENV/bin/pip" install -r requirements.txt

systemctl restart myportfolio
