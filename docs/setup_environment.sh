#!/bin/bash
git clone https://oopnet-bot:${GITHUB_TOKEN}@github.com/oopnet/linux_epanet_2.2.git
cd linux_epanet_2.2 || exit
make
cur_path=$(pwd)
echo 'export PATH="$cur_path/epanet2:$PATH"' >> ~/.bashrc
source ~/.bashrc
echo $PATH