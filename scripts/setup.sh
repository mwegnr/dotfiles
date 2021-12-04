#!/usr/bin/env bash

# install git and update archinstall to at least v2.3.0
pacman -Sy --noconfirm git archinstall

# download dotfiles & arch installer
git clone https://github.com/angerstoner/dotfiles
git clone https://github.com/archlinux/archinstall

# replace installed archinstall by newer version
pip uninstall archinstall -y
cd archinstall
python setup.py install

# launch archinstall with config
cd examples
cp ~/dotfiles/arch_install/* .
python guided.py --config /root/dotfiles/arch_install/config.json --silent --disk_layouts=/root/dotfiles/arch_install/disk_layout.json


arch-chroot /mnt/archinstall
useradd -m angerstoner
echo -e "devel\ndevel"  | passwd angerstoner