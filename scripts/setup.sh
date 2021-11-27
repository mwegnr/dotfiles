#!/usr/bin/env bash

# install git and update archinstall to at least v2.3.0
pacman -Sy --noconfirm git archinstall

# download dotfiles & arch installer
git clone https://github.com/angerstoner/dotfiles
git clone https://github.com/archlinux/archinstall

# launch archinstall with config
archinstall --config /root/dotfiles/arch_install/config.json --silent --disk_layouts=/root/dotfiles/arch_install/disk_layout.json

arch-chroot /mnt/archinstall
useradd -m angerstoner
echo -e "devel\ndevel"  | passwd angerstoner