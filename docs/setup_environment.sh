#!/bin/bash
git clone https://oopnet-bot:${GITHUB_TOKEN}@github.com/oopnet/linux_epanet_2.2.git
cd linux_epanet_2.2 || exit
make
echo 'export PATH="$HOME/linux_epanet_2.2/epanet2:$PATH"' >> ~/.bashrc