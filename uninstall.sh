#!/bin/bash

printf "* Removing ~/.local/haxtools...\n"
sudo rm -r ~/.local/haxtools
printf "* Removing symlink /usr/bin/hack...\n"
sudo rm -r /usr/bin/hack
