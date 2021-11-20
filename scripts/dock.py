#!/usr/bin/python3
import subprocess
import json

dock_identifier = "17ef:1010"  # Bus 002 Device 002: ID 17ef:1010 Lenovo ThinkPad Ultra Dock Hub

screen_identifiers = {
    'left_screen': {
        'make': 'Acer Technologies',
        'model': 'Acer K222HQL',
        'serial': 'T1LEE0054201'
    },
    'center_screen': {
        'make': 'Goldstar Company Ltd',
        'model': '24MB56',
        'serial': ''
    },
    'right_screen': {
        'make': 'Goldstar Company Ltd',
        'model': '24MB56',
        'serial': '508NTDVBJ122'
    }
}


def is_dock_connected():
    usb_devices = subprocess.run(['lsusb'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    return dock_identifier in usb_devices


def get_output_json():
    return json.loads(subprocess.run(['swaymsg', '-t', 'get_outputs'], stdout=subprocess.PIPE).stdout.decode('utf-8'))


def get_mapping(output_json):
    left, center, right = ("", "", "")
    for screen in output_json:
        if screen['model'] == screen_identifiers['left_screen']['model']:
            left = screen['name']
        elif screen['model'] == screen_identifiers['center_screen']['model'] and \
                screen['serial'] == screen_identifiers['center_screen']['serial']:
            center = screen['name']
        elif screen['model'] == screen_identifiers['right_screen']['model'] and \
                screen['serial'] == screen_identifiers['right_screen']['serial']:
            right = screen['name']
    return left, center, right


def dock(left, center, right):
    subprocess.run(['sway', 'output', 'eDP-1', 'disable'])  # disable internal screen
    subprocess.run(['sway', 'output', left, 'pos', '0', '0'])  # left screen
    subprocess.run(['sway', 'output', left, 'enable'])
    subprocess.run(['sway', 'output', center, 'pos', '1920', '0'])  # center screen
    subprocess.run(['sway', 'output', center, 'enable'])
    subprocess.run(['sway', 'output', right, 'pos', '3840', '0'])  # right screen
    subprocess.run(['sway', 'output', right, 'enable'])


def undock():
    for i in range(12):
        subprocess.run(['sway', 'output', 'DP-{}'.format(i), 'disable'])
    subprocess.run(['sway', 'output', 'eDP-1', 'enable'])


def restore_wallpaper():
    sway_bg_pid = subprocess.run(['pidof', 'swaybg'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    if sway_bg_pid == '':
        subprocess.Popen(['swaybg', '-i', '/home/angerstoner/.config/wallpaper.png', '-m', 'fit'])


if is_dock_connected():
    left_screen, right_screen, center_screen = get_mapping(get_output_json())
    dock(left_screen, right_screen, center_screen)
else:
    undock()
