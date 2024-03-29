#!/bin/bash
set -euo pipefail
# NOTE: Make sure that this script is idempotent;
#       if some code is added that makes this impossible, the README should also be changed to reflect this

home_dir=$(readlink -f "..")
# Get the directory containing this file, resolving symlinks (based on code from https://stackoverflow.com/a/51651602)
repo_dir="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
octoprint_python_executable="$home_dir/oprint/bin/python"

if [[ "$(whoami)" = "root" ]]; then
  >&2 echo "Do not run this script as the root user (through e.g. 'sudo')"
  exit 1
# This Python executable is necessary for updating OctoPrint's plugins
elif [ ! -e "$octoprint_python_executable" ]; then
  >&2 echo "The file '$octoprint_python_executable' does not exist;"
  >&2 echo "is this project not placed/configured correctly, or has OctoPrint/OctoPi changed setup?"
  exit 1
fi

register_and_run_weekly_cron_job() {
  local cron_job_script="$1"

  local script_filename
  script_filename=$(basename "$cron_job_script")
  local link_name="/etc/cron.weekly/$script_filename"
  # Register the cron job
  ln -sf "$cron_job_script" "$link_name"
  echo "+ Added symlink '$link_name' -> '$cron_job_script'"

  echo "+ Executing '$script_filename'..."
  # Execute the cron job script
  eval "$link_name"
}

camera_disabled=$(sudo raspi-config nonint get_camera)

# This is mainly done to not have to re-input the password for `sudo` after having upgraded packages,
# as that often takes long enough to make the OS re-prompt for the password
sudo su root <<HERE
set -euo pipefail

cd "$repo_dir"

# Enable camera
if [[ $camera_disabled != 0 ]]; then
  raspi-config nonint do_camera 0
  echo "+ Enabled Raspberry Pi camera"
fi

python3 -m python_scripts.customize_octopi_config

$(declare -f register_and_run_weekly_cron_job)
register_and_run_weekly_cron_job "$repo_dir/cron-jobs/weekly/update-software"
register_and_run_weekly_cron_job "$repo_dir/cron-jobs/weekly/zzz-reboot"

HERE
