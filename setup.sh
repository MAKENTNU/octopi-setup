#!/bin/bash
set -euo pipefail

if [[ "$(whoami)" = "root" ]]; then
  >&2 echo "Do not run this script as the root user (through e.g. 'sudo')"
  exit 1
fi

home=~
# This is mainly done to not have to re-input the password for `sudo` after having upgraded packages,
# as that often takes long enough to make the OS re-prompt for the password
sudo su root <<HERE
set -euo pipefail

# Enable camera
raspi-config nonint do_camera 0

python3 customize_octopi_config.py

apt update
apt upgrade -y

# Command found at https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html#command-line-usage
"$home/oprint/bin/python" -m octoprint plugins softwareupdate:update


reboot
HERE
