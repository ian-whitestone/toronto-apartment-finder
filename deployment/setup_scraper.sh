#! /bin/bash

cd ~/apartment-finder

sudo apt-get update
sudo apt-get install python3-pip -y
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev zip git-core sqlite -y
sudo pip3 install -r requirements.txt

sudo service scraper stop || true
sudo cp deployment/scraper.conf /etc/init/scraper.conf
sudo service scraper start