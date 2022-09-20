#!/bin/bash
git clone https://oopnet-bot:${GITHUB_TOKEN}@github.com/oopnet/linux_epanet_2.2.git
cd linux_epanet_2.2 || exit
make
cur_path=$(pwd)
echo "$cur_path"
echo 'export PATH="$cur_path/epanet2:$PATH"' >> /home/docs/.bashrc
source /home/docs/.bashrc
echo "$PATH"