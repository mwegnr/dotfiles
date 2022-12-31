#!/bin/bash

usb_dongle_name=Jabra_Link_380_50C2EDC6B02E-00
bt_headset_name=50_C2_ED_9B_00_61

# check if headset is connected in headphone or headset mode
if pactl list short | grep -q $usb_dongle_name\.pro; then
    mode=headset
else
    mode=headphone
fi

usb_dongle_id=$(pactl list short | grep "$usb_dongle_name.*alsa" | awk '{ print $1 }')
bt_headset_id=$(pactl list short | grep "$bt_headset_name.*module-bluez5-device" | awk '{ print $1 }')

echo $mode
if [ $mode = "headset" ]; then
    echo "Switching to headphone mode (BT)"
    pactl set-card-profile $bt_headset_id a2dp-sink
    pactl set-card-profile $usb_dongle_id off

    # after the device has switched the output device id appears
    # default device has to be set to this
    bt_headset_output_id=$(pactl list short | grep -P "$bt_headset_name.a2dp-sink\s" | awk '{ print $2 }')
    pactl set-default-sink $bt_headset_output_id
else
    echo "Switching to headset mode (USB)"
    pactl set-card-profile $usb_dongle_id pro-audio 
    pactl set-card-profile $bt_headset_id off
    
    # same as above
    usb_dongle_output_id=$(pactl list short | grep "$usb_dongle_name.pro-output-0\s" | awk '{ print $2 }')
    pactl set-default-sink $usb_dongle_output_id
fi
