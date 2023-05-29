import re
from difflib import unified_diff
from pathlib import Path
from urllib.request import urlopen


# Each tuple below does the following job:
# (<String that matches the start of a line (commented out or not)>, <String that will replace the line matched by the first element>)
REPLACEMENT_STRINGS = (
    # Drastically lower the framerate and quality, to make the streams less demanding for the RPis
    ('camera_usb_options=', 'camera_usb_options="-r 640x480 -f 2 -q 5"'),  # (Docs: https://faq.octoprint.org/mjpg-streamer-config)
)

octopi_config_file = Path('/boot/octopi.txt')
# This should be the updated version of `octopi_config_file`;
# should occasionally check whether that's still the case, or if the file has e.g. been moved to another directory within the repo
OCTOPI_CONFIG_FILE_URL = 'https://raw.githubusercontent.com/guysoft/OctoPi/devel/src/modules/octopi/filesystem/boot/octopi.txt'


def replace_line_starting_with(starting_with: str, replacement: str, string: str):
    return re.sub(rf"^[ #]*{starting_with}.*$", replacement, string, count=1, flags=re.MULTILINE)


# Downloading updated version of `octopi_config_file`
with urlopen(OCTOPI_CONFIG_FILE_URL) as file_response:
    new_file_contents = file_response.read().decode()

# Opening current version of `octopi_config_file`
file_contents = octopi_config_file.read_text()

for line_starting_with, replacement_str in REPLACEMENT_STRINGS:
    new_file_contents = replace_line_starting_with(line_starting_with, replacement_str, new_file_contents)

# Only write to the file if it's actually different:
if new_file_contents != file_contents:
    octopi_config_file.write_text(new_file_contents)

    print(f"Wrote to {octopi_config_file} with the following diff:")
    for diff_line in unified_diff(file_contents.splitlines(keepends=True), new_file_contents.splitlines(keepends=True),
                                  fromfile=f"{octopi_config_file} (old)", tofile=f"{octopi_config_file} (new)"):
        print(diff_line, end="")
    print()
