#!/usr/bin/python3
import subprocess
import os.path

USER_HOME = "/home/angerstoner"
CONFIGS_PATH = "configs"

config_paths = {
    f"{CONFIGS_PATH}/gtk2.0.config": f"{USER_HOME}/.gtkrc-2.0",
    f"{CONFIGS_PATH}/gtk3.0.config": f"{USER_HOME}/.config/gtk-3.0/settings.ini",
    f"{CONFIGS_PATH}/import-gsettings": f"{USER_HOME}/.config/gtk-3.0/import-gsettings",
    f"{CONFIGS_PATH}/sway.config": f"{USER_HOME}/.config/sway/config",
    f"{CONFIGS_PATH}/termite.config": f"{USER_HOME}/.config/termite/config",
    f"{CONFIGS_PATH}/waybar.config": f"{USER_HOME}/.config/waybar/config",
    f"{CONFIGS_PATH}/waybar.style": f"{USER_HOME}/.config/waybar/style.css",
    f"{CONFIGS_PATH}/zsh.config": f"{USER_HOME}/.zshrc",
    f"{CONFIGS_PATH}/nvim.config": f"{USER_HOME}/.config/nvim/init.vim",
    f"{CONFIGS_PATH}/latexmk.config": f"{USER_HOME}/.latexmkrc"
}


def install_packages():
    pass


def link_config_files():
    for file in config_paths:
        link_dir = os.path.split(config_paths[file])[0]
        filepath = "{}/{}".format(
            os.path.split(os.path.dirname(__file__))[0],  # parent dir/config file dir +
            file)  # filename

        os.makedirs(link_dir, exist_ok=True)
        link_cmd = ["ln", "-sf", filepath, config_paths[file]]
        subprocess.run(link_cmd)
        print(link_cmd)


def __main__():
    link_config_files()


__main__()
