#!/usr/bin/python3
import subprocess
import json

# TODO: change to dell home dock
dock_identifier_home = "04d9:0296"  # Keyboard, because thunderbolt dock does not have a USB ID
dock_identifier_work = "413c:b06e"  # Bus 005 Device 006: ID 413c:b06e Dell Computer Corp. Dell dock


class Screen:
    def __init__(self, make: str, model: str, serial: str, y_pos: int = 0, output_port=""):
        self.make = make
        self.model = model
        self.serial = serial
        self.y_pos = y_pos
        self.output_port = output_port

    def __eq__(self, other) -> bool:
        if not isinstance(other, Screen):
            return False
        return \
            self.make == other.make and \
            self.model == other.model and \
            self.serial == other.serial


screen_identifiers_home = [
    # Screen('Dell Inc.', 'Dell U4919DW', 'CQXTY2', 0),
    Screen('Acer Technologies', 'Acer K222HQL', 'T1LEE0054201', 0),
    Screen('Goldstar Company Ltd', '24MB56', '', 1920),
    Screen('Goldstar Company Ltd', '24MB56', '508NTDVBJ122', 3840),
]

screen_identifiers_work = [
    Screen('Dell Inc.', 'Dell U4919DW', 'CQXTY2', 0),
    Screen('Unknown', '0x06B3', '0x00000000', 5120)
]


def is_dock_connected(identifier: str) -> bool:
    usb_devices = subprocess.run(['lsusb'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    return identifier in usb_devices


def get_output_json():
    return json.loads(subprocess.run(['swaymsg', '-t', 'get_outputs'], stdout=subprocess.PIPE).stdout.decode('utf-8'))


def get_connected_screens(output_json, screen_identifiers: list[Screen]) -> list[Screen]:
    connected_screens = [Screen(screen['make'], screen['model'], screen["serial"], output_port=screen['name'])
                         for screen in output_json]
    for screen in connected_screens:
        for configured_screen in screen_identifiers:
            if screen == configured_screen:
                screen.y_pos = configured_screen.y_pos
    return connected_screens


def dock(screens: list[Screen], undock_internal=False):
    for screen in screens:
        subprocess.run(['sway', 'output', screen.output_port, 'pos', f'{screen.y_pos}', '0'])  #
        subprocess.run(['sway', 'output', screen.output_port, 'enable'])
    if undock_internal:
        subprocess.run(['sway', 'output', 'eDP-1', 'disable'])


def undock():
    for i in range(12):
        subprocess.run(['sway', 'output', 'DP-{}'.format(i), 'disable'])
    subprocess.run(['sway', 'output', 'eDP-1', 'enable'])


def restore_wallpaper():
    sway_bg_pid = subprocess.run(['pidof', 'swaybg'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    if sway_bg_pid == '':
        subprocess.Popen(['swaybg', '-i', '/home/angerstoner/.config/wallpaper.png', '-m', 'fit'])


if is_dock_connected(dock_identifier_work):
    dock(get_connected_screens(get_output_json(), screen_identifiers_work))
elif is_dock_connected(dock_identifier_home):
    dock(get_connected_screens(get_output_json(), screen_identifiers_home), undock_internal=True)
else:
    undock()
