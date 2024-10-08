#!/usr/bin/env python3
from datetime import datetime
import os
import sys
import yaml # $ python3 -m venv .env; source .env/bin/activate; python3 -m pip install pyyaml

OUTPUT_FILE = "./kernel-summary.md"
INPUT_FILE = "./devices.yml"
ROOT_DIR = "./"
repo_msg = "\n_This table was [generated automatically](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-devices/-/blob/master/.gitlab-ci.yml) on {} from the [Kali NetHunter GitLab repository](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-devices)_\n".format(datetime.now().strftime("%Y-%B-%d %H:%M:%S"))
qty_dir_kernels = 0
qty_yml_kernels = 0
qty_versions = { }

## Input:
##   $ ls -l
##   ./
##    |---> [Android Version]/
##        |-> [Device-ROM]/
##   $ cat ./devices.yml
##   - angler:
##       model  : Google Nexus 6P
##       kernels:
##         - id          : angler
##           description : Google Nexus 6P for stock Android
##           kernelstring: NetHunter kernel for Nexus 6P
##           arch        : arm64
##           devicenames : angler
##           block       : /dev/block/platform/soc.0/f9824900.sdhci/by-name/boot
##           versions    :
##             - android    : marshmallow
##               linux      : 3.10
##               description: Android 6
##               author     : Binkybear
##               source     : 'git clone https://github.com/binkybear/AK-Angler.git'
##               features   : [HID, Injection]
##             - android    : nougat
##               linux      : 3.10
##               description: Android 7.1
##               author     : jcadduono
##               source     : 'git clone https://github.com/jcadduono/android_kernel_huawei_angler -b nethunter-7.1_2'
##               features   : [CDROM, HID, Injection]
##             - android    : oreo
##               linux      : 3.10
##               description: Android 8.1
##               author     : Re4son & yesimxev
##               source     : 'git clone https://github.com/Re4son/android_kernel_huawei_angler -b nethunter-8.1'
##               features   : [BT_RFCOMM, CDROM, HID, Injection, Nexmon, RTL8812AU, RTL8188EUS, Internal BT]
##         - id          : angler-los
##           description : Google Nexus 6P for LineageOS and Pixel Experience
##           kernelstring: NetHunter kernel for Nexus 6P
##           arch        : arm64
##           flasher     : anykernel
##           modules     : 1
##           block       : /dev/block/bootdevice/by-name/boot
##           slot_device : 0
##           devicenames : angler
##           versions    :
##             - android    : ten
##               linux      : 3.10
##               description: LineageOS 17.1 & Pixel Experience 10
##               author     : Re4son & yesimxev
##               source     : 'git clone https://github.com/Re4son/android_kernel_huawei_angler_pixel -b nethunter-10.0'
##               features   : [BT_RFCOMM, HID, Injection, Nexmon, RTL8812AU, Internal BT, RTL8188EUS]


def read_file(file):
    try:
        print('[i] Reading: {}'.format(file))
        with open(file) as f:
            data = f.read()
            f.close()
    except Exception as e:
        print("[-] Cannot open input file: {} - {}".format(file, e), file=sys.stderr)
        sys.exit(1)
    return data


def yaml_parse(data):
    result = ""
    lines = data.split('\n')
    for line in lines:
        if not line.startswith('#'):
            ## yaml doesn't like tabs so let's replace them with four spaces
            result += "{}\n".format(line.replace('\t', '    '))
    return yaml.safe_load(result)


def count_yml(yml):
    default = ""
    yml_kernels = []

    # iterate over all device models
    for element in yml:
        # iterate over all model's entries in yaml file
        for device_model in element.keys():
            for kernel in element[device_model].get('kernels', default):
                # iterate over all model kernels version's
                for version in kernel.get('versions', default):
                    android_version = version.get('android', default)
                    yml_kernels.append(android_version)
    return len(yml_kernels)


def dir_count(path):
    print('[i] Searching in: {}'.format(path))
    root, dirs, files = next(os.walk(path))
    return len(dirs)


def count_android_versions():
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
        android_version_dir = android_version_dir.replace(ROOT_DIR, '')
        path = ROOT_DIR + android_version_dir
        v = android_version_dir.title()
        v = v.replace('kitkat', '4.4 - KitKat')
        v = v.replace('lollipop', '5.0 - Lollipop')
        v = v.replace('marshmallow', '6 - Marshmallow')
        v = v.replace('nougat', '7 - Nougat')
        v = v.replace('oreo', '8 - Oreo')
        v = v.replace('pie', '9 - Pie')
        v = v.replace('ten', '10 - Ten')
        v = v.replace('eleven', '11 - Eleven')
        v = v.replace('twelve', '12 - Twelve')
        v = v.replace('thirteen', '13 - Thirteen')
        v = v.replace('fourteen', '14 - Fourteen')
        v = v.replace('wearos', 'Wear OS')
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
            stats += "  - See [here for more details about the kernels](kernels.html) _([config file](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-devices/-/blob/master/devices.yml), [directories](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-kernel))_\n"
            stats += "  - **{} kernels build profiles** are in ./devices.yml\n".format(qty_yml_kernels)
            stats += "  - NetHunter is on **{} Android versions**\n".format(len(qty_versions))
            stats += "- [Kali NetHunter Statistics Overview](index.html)\n\n"
            f.write(str(meta))
            f.write(str(stats))
            f.write(str(data))
            f.write(str(repo_msg))
            f.close()
            print('[+] Writing: {}'.format(OUTPUT_FILE))
    except Exception as e:
        print("[-] Cannot write to output file: {} - {}".format(file, e), file=sys.stderr)
    return 0


def print_summary():
    print('[i] Android versions count : {}'.format(len(qty_versions)))
    print('[i] Kernels in directories : {}'.format(qty_dir_kernels))
    print('[i] Kernels in YAML kernels: {}'.format(qty_yml_kernels))


def main(argv):
    global qty_dir_kernels, qty_yml_kernels

    # Assign variables
    data = read_file(INPUT_FILE)

    # Get data (YAML)
    yml = yaml_parse(data)

    # Get data (Directories)
    get_versions()

    # Generate stats
    qty_dir_kernels = count_android_versions()
    qty_yml_kernels = count_yml(yml)

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
