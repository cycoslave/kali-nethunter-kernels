#!/usr/bin/env python3
from datetime import datetime
import os
import re
import sys
import yaml # $ python3 -m pip install pyyaml --user

OUTPUT_FILE = "./kernel-summary.md"
INPUT_FILE = "./devices.cfg"
ROOT_DIR = "./"
repo_msg = "\n_This table was [generated automatically](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-devices/-/blob/master/.gitlab-ci.yml) on {} from the [Kali NetHunter GitLab repository](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-devices)_\n".format(datetime.now().strftime("%Y-%B-%d %H:%M:%S"))
qty_dir_kernels = 0
qty_yml_kernels = 0
qty_versions = { }

## Input:
## $ ls -l
## [...]
## ------------------------------------------------------------ ##
## ./
##  |---> [Android Version]/
##      |-> [Device]/
## $ grep '##*' ./devices.cfg
## [...]
## ------------------------------------------------------------ ##
## ##* - a5ulte:
## ##*     model   : Samsung Galaxy A5 (2015)
## ##*     kernels :
## ##*       - id          : a5ulte-cm
## ##*         description : Samsung Galaxy A5 (2015) for CyanogenMod
## ##*         versions    :
## ##*           - android      : marshmallow
## ##*             linux        : '3.10'
## ##*             kernel       : 1.3
## ##*             description  : CyanogenMod 13
## ##*             author       : DeadSquirrel01
## ##*             source       : 'git clone https://github.com/DeadSquirrel01/nethunter-kernel-a5ulte.git -b cm-13.0'
## ##*             features     : []
## ##*       - id          : a5ulte-tw
## ##*         description : Samsung Galaxy A5 (2015) for TouchWiz (Europe)
## ##*         versions    :
## ##*           - android      : marshmallow
## ##*             linux        : '3.10'
## ##*             kernel       : 1.3
## ##*             description  : TouchWiz 6
## ##*             author       : DeadSquirrel01
## ##*             source       : 'git clone https://github.com/DeadSquirrel01/nethunter-kernel-a5ulte.git -b touchwiz-6.0'
## ##*             features     : []

def yaml_parse(data):
    result = ""
    lines = data.split('\n')
    for line in lines:
        if line.startswith('##*'):
            ## yaml doesn't like tabs so let's replace them with four spaces
            result += "{}\n".format(line.replace('\t', '    ')[3:])
    return yaml.safe_load(result)

def read_file(file):
    try:
        print('[i] Reading: {}'.format(file))
        with open(file) as f:
            data = f.read()
            f.close()
    except Exception as e:
        print('[-] Cannot open input file: {} - {}'.format(file, e))
        sys.exit(1)
    return data

def yml_count(yml):
    default = ""
    yml_kernels = []

    # iterate over all device models
    for element in yml:
        # iterate over all model's entries in yaml file
        for device_model in element.keys():
            # iterate over all model's kernels
            for kernel in element[device_model].get('kernels', default):
                # iterate over all model kernels version's
                for version in kernel['versions']:
                    android_version = version.get('android', default)
                    yml_kernels.append(android_version)
    return len(yml_kernels)


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
            stats  = "- The official [Kali NetHunter repository](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-devices) has a total of [**{}** kernels](kernels-summary.html) directories\n".format(str(qty_dir_kernels))
            stats += "  - See [here for more details about the kernels](kernels.html) _([config file](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-devices/-/blob/master/devices.cfg), [directories](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-kernel))_\n"
            stats += "  - **{} kernels** are in ./devices.cfg\n".format(qty_yml_kernels) # See: ./bin/kernel_integrity.py
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
    print('[i] Kernels in directories: {}'.format(qty_dir_kernels))
    print('[i] Kernels in YAML       : {}'.format(qty_yml_kernels))

def main(argv):
    global qty_dir_kernels, qty_yml_kernels

    # Assign variables
    data = read_file(INPUT_FILE)

    # Get data (YAML)
    yml = yaml_parse(data)

    # Get data (Directories)
    get_versions()

    # Generate stats
    qty_dir_kernels = calc_kernels()
    qty_yml_kernels = yml_count(yml)

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
