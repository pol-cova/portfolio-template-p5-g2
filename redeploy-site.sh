#!/bin/bash

DIR_PROJECT=~/portfolio-template-p5-g2
VENV=$DIR_PROJECT/python3-virtualenv

tmux kill-server 2>/dev/null || true

cd $DIR_PROJECT
git fetch && git reset origin/main --hard

source $VENV/bin/activate
pip install -r requirements.txt

tmux new-session -d -s flask -c $DIR_PROJECT \
  "source $VENV/bin/activate && flask run --host=0.0.0.0"
