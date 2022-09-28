# octopi-setup
Setup of Raspberry Pis running OctoPi, mainly for enabling streaming to [a Django website](https://github.com/MAKENTNU/web).


### Setup
(The stream should be visible on the website without following these steps,
but doing this ensures that it's set up properly and that the software is up-to-date.)

1. Enter the home folder if you are not already there: `cd ~`
1. Clone this repository: `git clone https://github.com/MAKENTNU/octopi-setup.git`
1. Enter the newly created `octopi-setup` folder: `cd octopi-setup/`
1. Run the setup script: `./setup.sh`
   * *This script is idempotent, so it should be safe to run multiple times on the same system - for whatever reason*

The RPi will reboot once the script is done.

---

A detailed guide on the hardware setup is available on MAKE NTNU's Google Drive.
