#!/usr/bin/python3
import subprocess
import os.path

config_paths = {
    "gtk2.0.config": "/home/angerstoner/.gtkrc-2.0",
    "gtk3.0.config": "/home/angerstoner/.config/gtk-3.0/settings.ini",
    "import-gsettings": "/home/angerstoner/.config/gtk-3.0/import-gsettings",
    "sway.config": "/home/angerstoner/.config/sway/config",
    "termite.config": "/home/angerstoner/.config/termite/config",
    "waybar.config": "/home/angerstoner/.config/waybar/config",
    "waybar.style": "/home/angerstoner/.config/waybar/style.css",
    "zsh.config": "/home/angerstoner/.zshrc",
    "nvim.config": "/home/angerstoner/.config/nvim/init.vim",
    "latexmk.config": "/home/angerstoner/.latexmkrc"
}


def install_packages():
    pass


def link_config_files():
    for file in config_paths:
        filepath = "{}/{}".format(
            os.path.split(os.path.dirname(__file__))[0],  # parent dir/config file dir +
            file)  # filename

        link_cmd = ["ln", "-sf", filepath, config_paths[file]]
        subprocess.run(link_cmd)
        print(link_cmd)


def __main__():
    link_config_files()


__main__()
