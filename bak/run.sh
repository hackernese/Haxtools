#!/bin/bash

# Used while debugging only 
args="$@"

# This progam requiresv SUID to function properly
sudo rm -f ./tmp/.hack
go build -C src -o ../tmp/.hack
sudo chown root:root ./tmp/.hack
sudo chmod u+xs ./tmp/.hack

./tmp/.hack  $args