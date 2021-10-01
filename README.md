# remote-office

Install on a raspberrypi requirements:

    sudo pip3 install -r requirements.txt 

Install the keylogger script:

    src/pi/install_app.sh




## Other cool stuff

#### Set hebrew keyboard on Raspberrypi:

edit file ``sudo vi /etc/default/keyboard`` and put:

```bash
XKBMODEL="pc105"
XKBLAYOUT="us,il"
XKBOPTIONS="grp:alt_shift_toggle,grp:switch,grp_led:scroll"
XKBVARIANT=","
BACKSPACE="guess"
```
reboot
