#!/usr/bin/python3
import subprocess
import os.path

USER_HOME = "/home/angerstoner"

config_paths = {
    "gtk2.0.config": f"{USER_HOME}/.gtkrc-2.0",
    "gtk3.0.config": f"{USER_HOME}/.config/gtk-3.0/settings.ini",
    "import-gsettings": f"{USER_HOME}/.config/gtk-3.0/import-gsettings",
    "sway.config": f"{USER_HOME}/.config/sway/config",
    "termite.config": f"{USER_HOME}/.config/termite/config",
    "waybar.config": f"{USER_HOME}/.config/waybar/config",
    "waybar.style": f"{USER_HOME}/.config/waybar/style.css",
    "zsh.config": f"{USER_HOME}/.zshrc",
    "nvim.config": f"{USER_HOME}/.config/nvim/init.vim",
    "latexmk.config": f"{USER_HOME}/.latexmkrc"
}


def install_packages():
    pass


def link_config_files():
    for file in config_paths:
        filepath = "{}/{}".format(
            os.path.split(os.path.dirname(__file__))[0],  # parent dir/config file dir +
            file)  # filename

        os.makedirs(filepath, exist_ok=True)
        link_cmd = ["ln", "-sf", filepath, config_paths[file]]
        subprocess.run(link_cmd)
        print(link_cmd)


def __main__():
    link_config_files()


__main__()
