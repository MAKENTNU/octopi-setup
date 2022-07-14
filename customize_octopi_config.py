import re
from pathlib import Path


REPLACEMENT_STRINGS = (
    ("camera=", 'camera="raspi"'),
    ("camera_raspi_options=", 'camera_raspi_options="-fps 2 -x 640 -y 480 -quality 5"'),
)

octopi_config_file = Path('/boot/octopi.txt')


def replace_line_starting_with(starting_with: str, replacement: str, string: str):
    return re.sub(rf"^[ #]*{starting_with}.*$", replacement, string, count=1, flags=re.MULTILINE)


file_contents = octopi_config_file.read_text()

new_file_contents = file_contents
for line_starting_with, replacement_str in REPLACEMENT_STRINGS:
    new_file_contents = replace_line_starting_with(line_starting_with, replacement_str, new_file_contents)

if new_file_contents != file_contents:
    octopi_config_file.write_text(new_file_contents)

    print(f"Wrote the following lines to {octopi_config_file}:")
    for _, replacement_str in REPLACEMENT_STRINGS:
        print(replacement_str)
    print()
