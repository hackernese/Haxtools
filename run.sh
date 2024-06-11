#!/bin/bash

# Used while debugging only 

args="$@"
go build -C src -o ../tmp/.hack
./tmp/.hack  $args