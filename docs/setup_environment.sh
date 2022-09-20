#!/bin/bash
git clone https://oopnet-bot:"${GITHUB_TOKEN}"@github.com/oopnet/linux_epanet_2.2.git
cd linux_epanet_2.2 || exit
make
cp epanet2 /home/docs/checkouts/readthedocs.org/user_builds/oopnet/envs/latest/bin/epanet2