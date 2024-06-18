#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

install_openvpn() {
    if command_exists apt-get; then
        echo "Detected apt package manager. Installing packages..."
        sudo apt-get update
        sudo apt-get install -y openvpn polkit
    elif command_exists yum; then
        echo "Detected yum package manager. Installing packages..."
        sudo yum install -y openvpn polkit
    elif command_exists pacman; then
        echo "Detected pacman package manager. Installing packages..."
        sudo pacman -Sy openvpn polkit --noconfirm
    else
        echo "Unsupported package manager. Please install OpenVPN and Polkit manually."
        exit 1
    fi
}

# Install dependencies
printf "* Installing dependencies ( openvpn, polkit )...\n"
install_openvpn >/dev/null 2>&1

# Copy the source code
cp -r ./src ~/.local/haxtools

# Create a virtual environment
printf "* Creating virtual environment..."
python -m venv ~/.local/haxtools/venv
printf " [DONE]\n"

printf "* Installing python libraries..."
~/.local/haxtools/venv/bin/pip install -r ./requirements.txt >/dev/null
printf " [DONE]\n"

# Making the "hack" script executable
chmod +x ~/.local/haxtools/hack

# Making symlink
printf "* Creating a symlink in /usr/bin/hack..."
sudo ln -s ~/.local/haxtools/hack /usr/bin/hack
printf " [DONE]\n"
