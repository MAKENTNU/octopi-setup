import re
from urllib.request import urlopen
from pathlib import Path


REPLACEMENT_STRINGS = (
    ('camera_usb_options=', 'camera_usb_options="-r 640x480 -f 2 -q 5"'),
)

octopi_config_file = Path('/boot/octopi.txt')

OCTOPI_CONFIG_FILE_URL = 'https://raw.githubusercontent.com/guysoft/OctoPi/devel/src/modules/octopi/filesystem/boot/octopi.txt'


def replace_line_starting_with(starting_with: str, replacement: str, string: str):
    return re.sub(rf"^[ #]*{starting_with}.*$", replacement, string, count=1, flags=re.MULTILINE)


# Downloading updated version of octopi.txt
with urlopen(OCTOPI_CONFIG_FILE_URL) as file_response:
    new_file_contents = file_response.read().decode()

# Opening old version of octopi.txt
file_contents = octopi_config_file.read_text()

for line_starting_with, replacement_str in REPLACEMENT_STRINGS:
    new_file_contents = replace_line_starting_with(line_starting_with, replacement_str, new_file_contents)

# If old and new version are different, writing new version of octopi.txt to file
if new_file_contents != file_contents:
    octopi_config_file.write_text(new_file_contents)

    print(f"Wrote the following lines to {octopi_config_file}:")
    for _, replacement_str in REPLACEMENT_STRINGS:
        print(replacement_str)
    print()
