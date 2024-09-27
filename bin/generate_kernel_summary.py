#!/usr/bin/env python3
from datetime import datetime
import os
import re
import sys

OUTPUT_FILE = "./kernel-summary.md"
ROOT_DIR = "./"
repo_msg = "\n_This table was [generated automatically](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-devices/-/blob/master/.gitlab-ci.yml) on {} from the [Kali NetHunter GitLab repository](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-devices)_\n".format(datetime.now().strftime("%Y-%B-%d %H:%M:%S"))
qty_kernels = 0
qty_versions = { }

## Input:
## $ ls -l
## [...]
## ------------------------------------------------------------ ##
## ./
##  |---> [Android Version]/
##      |-> [Device]/

def dir_count(path):
    print('[i] Searching in: {}'.format(path))
    root, dirs, files = next(os.walk(path))
    return len(dirs)

def calc_kernels():
    t = 0
    for v in qty_versions:
        t += qty_versions[v]
    return t

def get_versions():
    # Discovery directories
    subdirectories = [ x.path for x in os.scandir(ROOT_DIR) if x.is_dir() and not x.path.startswith('{}.'.format(ROOT_DIR))]
    # Remove non Android version directories
    subdirectories.remove('{}bin'.format(ROOT_DIR))
    subdirectories.remove('{}example_scripts'.format(ROOT_DIR))
    subdirectories.remove('{}patches'.format(ROOT_DIR))

    for android_version_dir in subdirectories:
        android_version_dir = android_version_dir.lower()
        android_version_dir = re.sub(ROOT_DIR, '', android_version_dir)
        path = ROOT_DIR + android_version_dir
        v = android_version_dir.title()
        v = re.sub('kitkat', '4.4 - KitKat', v, flags=re.I)
        v = re.sub('lollipop', '5.0 - Lollipop', v, flags=re.I)
        v = re.sub('marshmallow', '6 - Marshmallow', v, flags=re.I)
        v = re.sub('nougat', '7 - Nougat', v, flags=re.I)
        v = re.sub('oreo', '8 - Oreo', v, flags=re.I)
        v = re.sub('pie', '9 - Pie', v, flags=re.I)
        v = re.sub('ten', '10 - Ten', v, flags=re.I)
        v = re.sub('eleven', '11 - Eleven', v, flags=re.I)
        v = re.sub('twelve', '12 - Twelve', v, flags=re.I)
        v = re.sub('thirteen', '13 - Thirteen', v, flags=re.I)
        v = re.sub('fourteen', '14 - Fourteen', v, flags=re.I)
        v = re.sub('wearos', 'Wear OS', v, flags=re.I)
        qty_versions[v] = dir_count(path)

def generate_table():
    table  = "| Android Version | Qty |\n"
    table += "|-----------------|-----|\n"
    # iterate over all the models
    for v in sorted(qty_versions):
        table += "| {} | {} |\n".format(v.ljust(15),
                                        str(qty_versions[v]).ljust(3))
    return table

def write_file(data, file):
    try:
        with open(file, 'w') as f:
            meta  = '---\n'
            meta += 'title: Kali NetHunter Kernel Summary\n'
            meta += '---\n\n'
            stats  = "- The official [Kali NetHunter repository](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-devices) has a total of [**{}** kernels](kernels.html) directories\n".format(str(qty_kernels))
            stats += "  - See [here for more details about the kernels](kernels.html) _([config file](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-devices/-/blob/master/devices.cfg), [directories](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-kernel))_\n"
            stats += "  - NetHunter is on **{} Android versions**\n".format(len(qty_versions))
            stats += "- [Kali NetHunter Statistics Overview](index.html)\n\n"
            f.write(str(meta))
            f.write(str(stats))
            f.write(str(data))
            f.write(str(repo_msg))
            f.close()
            print('[+] Writing: {}'.format(OUTPUT_FILE))
    except Exception as e:
        print('[-] Cannot write to output file: {} - {}'.format(file, e))
    return 0

def print_summary():
    print('[i] Android versions count: {}'.format(len(qty_versions)))
    print('[i] Kernel directories: {}'.format(qty_kernels))

def main(argv):
    global qty_kernels

    # Get data
    get_versions()

    # Generate stats
    qty_kernels = calc_kernels()

    # Print result
    print_summary()

    # Generate markdown
    generated_markdown = generate_table()

    # Create markdown file
    write_file(generated_markdown, OUTPUT_FILE)

    # Exit
    exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])
