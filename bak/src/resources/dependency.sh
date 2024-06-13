#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install OpenVPN
install_openvpn() {
    # Check if OpenVPN is already installed
    if command_exists openvpn && command_exists polkit; then
        echo "OpenVPN is already installed."
        return
    fi

    # Detect package manager and install OpenVPN
    if command_exists apt-get; then
        echo "Detected apt package manager. Installing OpenVPN..."
        sudo apt-get update
        sudo apt-get install -y openvpn polkit
    elif command_exists yum; then
        echo "Detected yum package manager. Installing OpenVPN..."
        sudo yum install -y openvpn polkit
    elif command_exists pacman; then
        echo "Detected pacman package manager. Installing OpenVPN..."
        sudo pacman -Sy openvpn polkit --noconfirm
    else
        echo "Unsupported package manager. Please install OpenVPN manually."
        exit 1
    fi
}

# Main script
install_openvpn
