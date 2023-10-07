#!/bin/bash

cp convform/bots/vtipobot_edited.json ../cvf/bots/vtipobot.json
cp -r ../cvf/bots/ convform/bots/
cp ../cvf/Cargo.toml convform/Cargo.toml

# cd convform/ && maturin develop && cd ..
python test.py
