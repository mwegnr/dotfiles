#!/usr/bin/python3
import json
import subprocess

dock_identifier_home = "17ef:a396"  # Bus 003 Device 019: ID 17ef:a396 Lenovo ThinkPad USB-C Dock Gen2 USB Audio
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
        return self.make == other.make and \
            self.model == other.model and \
            self.serial == other.serial


screen_identifiers_home = [
    Screen('LG Electronics', '24MB56', '508NTDVBJ122', 0),
    Screen('Dell Inc.', 'DELL U2717D', 'J0XYN8C4C8QS', 1920),
    Screen('LG Electronics', '24MB56', '0x0006EE50', 3840),
]

screen_identifiers_work = [
    Screen('Dell Inc.', 'Dell U4919DW', 'CQXTY2', 0),
    # TODO: find way to work around serial (alternating workplaces at work)
    Screen('LG Display', '0x06B3', 'Unknown', 5120)
]


def is_dock_connected(identifier: str) -> bool:
    usb_devices = subprocess.run(['lsusb'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    return identifier in usb_devices


def has_hostname(hostname: str) -> bool:
    detected_hostname = subprocess.run(['cat', '/etc/hostname'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    return hostname in detected_hostname


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
        # TODO: add resolution to screen identifiers, at work, we don't want 1080p
        subprocess.run(['sway', 'output', screen.output_port,
                        'mode 1920x1080@60Hz'])  # set all screens to FHD, 1440p won't work with the HDMI switch
        subprocess.run(['sway', 'output', screen.output_port, 'pos', f'{screen.y_pos}', '0'])  #
        subprocess.run(['sway', 'output', screen.output_port, 'enable'])
    if undock_internal:
        subprocess.run(['sway', 'output', 'eDP-1', 'disable'])


def undock():
    for i in range(12):
        subprocess.run(['sway', 'output', 'DP-{}'.format(i), 'disable'])
    subprocess.run(['sway', 'output', 'eDP-1', 'enable'])
    if has_hostname("eve"):
        subprocess.run(['sway', 'output', 'eDP-1', 'scale', '1.3'])  # set scale to 1.3 on hiDPI fw display


def restore_wallpaper():
    sway_bg_pid = subprocess.run(['pidof', 'swaybg'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    if sway_bg_pid == '':
        subprocess.Popen(['swaybg', '-i', '~/.config/wallpaper.png', '-m', 'fit'])


if is_dock_connected(dock_identifier_work):
    dock(get_connected_screens(get_output_json(), screen_identifiers_work))
elif is_dock_connected(dock_identifier_home):
    dock(get_connected_screens(get_output_json(), screen_identifiers_home), undock_internal=True)
else:
    undock()
