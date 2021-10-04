#!/bin/bash
SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
sudo cp -v "${SCRIPTPATH}/myapp.desktop" /etc/xdg/autostart/myapp.desktop
echo "Installed"

