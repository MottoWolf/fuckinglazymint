#!/bin/bash

# Pre check
sudo apt-get install python -y
sudo apt install software-properties-common
sudo add-apt-repository ppa:ansible/ansible -y
sudo add-apt-repository ppa:git-core/ppa -y

# Install
sudo apt update
sudo apt install git -y
sudo apt-get install git-core -y
sudo apt install ansible -y
