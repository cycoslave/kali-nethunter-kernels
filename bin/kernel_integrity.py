#!/usr/bin/env python3
## TODO:
##   $ grep '^\[' devices.cfg | sed -E 's/\[//; s/\]//' | while read -r x do; do grep -q " - id .*: ${x}$" devices.cfg || echo ${x}; done
from datetime import datetime
import os
import re
import sys
import yaml # $ python3 -m pip install pyyaml --user
import configparser

OUTPUT_FILE = "./kernel-summary.md"
INPUT_FILE = "./devices.cfg"
ROOT_DIR = "./"
repo_msg = "\n_This table was [generated automatically](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-devices/-/blob/master/.gitlab-ci.yml) on {} from the [Kali NetHunter GitLab repository](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-devices)_\n".format(datetime.now().strftime("%Y-%B-%d %H:%M:%S"))

## Input:
##   $ ls -l
##   ./
##    |---> [Android Version]/
##        |-> [Device]/
##   $ grep '##*' ./devices.cfg
##   ##* - angler:
##   ##*     model  : Nexus 6P
##   ##*     kernels:
##   ##*       - id         : angler
##   ##*         description: Stock Android
##   ##*         versions   :
##   ##*           - android     : nougat
##   ##*             linux       : 3.10
##   ##*             description : Android 7.1
##   ##*             author      : jcadduono
##   ##*             source      : 'git clone https://github.com/jcadduono/android_kernel_huawei_angler -b nethunter-7.1_2'
##   ##*             features    : [CDROM, HID, Injection]
##   ##*           - android     : oreo
##   ##*             linux       : 3.10
##   ##*             description : Android 8.1
##   ##*             author      : Re4son & yesimxev
##   ##*             source      : 'git clone https://github.com/Re4son/android_kernel_huawei_angler -b nethunter-8.1'
##   ##*             features    : [BT_RFCOMM, CDROM, HID, Injection, Nexmon, RTL8812AU, RTL8188EUS, Internal BT]
##   ##*       - id         : angler-los
##   ##*         description: LineageOS
##   ##*         versions   :
##   ##*           - android     : ten
##   ##*             linux       : 3.10
##   ##*             description : LineageOS 17.1 & Pixel Experience 10
##   ##*             author      : Re4son & yesimxev
##   ##*             source      : 'git clone https://github.com/Re4son/android_kernel_huawei_angler_pixel -b nethunter-10.0'
##   ##*             features    : [BT_RFCOMM, HID, Injection, Nexmon, RTL8812AU, Internal BT, RTL8188EUS]
##   $ grep -v '##*' ./devices.cfg
##   # Nexus 6P
##   [angler]
##   author = "Binkybear & jcadduono & re4son & yesimxev"
##   kernelstring = "NetHunter kernel for Nexus 6P"
##   arch = arm64
##   devicenames = angler
##   block = /dev/block/platform/soc.0/f9824900.sdhci/by-name/boot
##
##   # Nexus 6P for LineageOS 17.1 and Pixel Experience 10
##   [angler-los]
##   author = "Re4son & yesimxev"
##   kernelstring = "NetHunter kernel for Nexus 6P"
##   arch = arm64
##   flasher = anykernel
##   modules = 1
##   block = /dev/block/bootdevice/by-name/boot
##   slot_device = 0
##   #* Note: when using "anykernel" flasher, use commas to separate device names
##   devicenames = angler

def yaml_parse(data):
    result = ""
    lines = data.split('\n')
    for line in lines:
        if line.startswith('##*'):
            ## yaml doesn't like tabs so let's replace them with four spaces
            result += "{}\n".format(line.replace('\t', '    ')[3:])
    return yaml.safe_load(result)

def ini_parse():
    try:
        print('[i] Parsing: {}'.format(INPUT_FILE))
        Config = configparser.ConfigParser(strict=False)
        Config.read(INPUT_FILE)
        return Config.sections()
    except Exception as e:
        print('[-] Cannot parse ini input file: {} - {}'.format(file, e), file=sys.stderr)
        sys.exit(1)

def read_file(file):
    try:
        print('[i] Reading: {}'.format(file))
        with open(file) as f:
            data = f.read()
            f.close()
    except Exception as e:
        print('[-] Cannot open input file: {} - {}'.format(file, e), file=sys.stderr)
        sys.exit(1)
    return data

def get_versions(yml):
    # Discovery directories
    subdirectories = [ x.path for x in os.scandir(ROOT_DIR) if x.is_dir() and not x.path.startswith('{}.'.format(ROOT_DIR))]
    # Remove non Android version directories
    subdirectories.remove('{}bin'.format(ROOT_DIR))
    subdirectories.remove('{}example_scripts'.format(ROOT_DIR))
    subdirectories.remove('{}patches'.format(ROOT_DIR))

    for android_version_dir in subdirectories:
        android_version_dir = android_version_dir.lower()
        android_version_dir = re.sub(ROOT_DIR, '', android_version_dir)
        print("[i] Comparing whats in {}{}/* -> {}".format(ROOT_DIR, android_version_dir, INPUT_FILE))

        root, dirs, files = next(os.walk(android_version_dir))
        for kernel_id_dir in dirs:
            compare_dir_yml(android_version_dir, kernel_id_dir, yml)

def compare_dir_yml(android_version_dir, kernel_id_dir, yml):
    default = ""
    path = os.path.join(ROOT_DIR, android_version_dir, kernel_id_dir)

    # iterate over all device models
    for element in yml:
        # iterate over all model's entries in yaml file
        for device_model in element.keys():
            # iterate over all model's kernels
            for kernel in element[device_model].get('kernels', default):
                kernel_id = kernel.get('id', default)
                # have we got a kernel id/name match?
                if kernel_id == kernel_id_dir:
                    # iterate over all model kernels version's
                    for version in kernel['versions']:
                        android_version = version.get('android', default)
                        # have we got a kernel version match?
                        if android_version == android_version_dir:
                            return

    print("[-]   Found on disk ({}), but hasn't be added to: {}".format(path,  INPUT_FILE), file=sys.stderr)

def compare_yml_dir(yml):
    print("[i] Comparing whats in {} -> {}*".format(INPUT_FILE, ROOT_DIR))

    default = ""

    # iterate over all device models
    for element in yml:
        # iterate over all model's entries in yaml file
        for device_model in element.keys():
            model = element[device_model].get('model', default)

            # is there a kernel entry in the YAML file?
            if 'kernels' not in element[device_model]:
                print("[-]   In {}, found model ({}/{}), but is missing kernel entry".format(INPUT_FILE, device_model, model), file=sys.stderr)

            kernels = [x['id'] for x in element[device_model].get('kernels', default)]
            dup_kernels = {x for x in kernels if kernels.count(x) > 1}
            if dup_kernels:
                print("[-]   In {}, found model ({}/{}), but has multiple kernels with the same ID: {}".format(INPUT_FILE, device_model, model, dup_kernels), file=sys.stderr)

            for kernel in element[device_model].get('kernels', default):
                kernel_id = kernel.get('id', default)
                if not kernel_id.startswith(device_model):
                    print("[-]   In {}, kernel_id doesn't start with model id: model: {}   kernel_id: {}".format(INPUT_FILE, device_model, kernel_id), file=sys.stderr)

                versions = [x['android'] for x in kernel.get('versions', default)]
                dup_versions = {x for x in versions if versions.count(x) > 1}
                if dup_versions:
                    print("[-]   In {}, found model ({}/{}), but {} kernel id with multiple same android version: {}".format(INPUT_FILE, device_model, model, kernel_id, dup_versions), file=sys.stderr)

                for version in kernel['versions']:
                    android_version = version.get('android', default)
                    path = os.path.join(ROOT_DIR, android_version, kernel_id)
                    if not os.path.isdir(path):
                        print("[-]   In {}, found model ({}/{}), but missing on disk: {}".format(INPUT_FILE, device_model, model, path), file=sys.stderr)

def compare_yml_ini(yml, ini):
    print("[i] Comparing YAML to INI in: {}".format(INPUT_FILE))
    default = ""

    # iterate over all device models
    for element in yml:
        # iterate over all model's entries in yaml file
        for device_model in element.keys():
            for kernel in element[device_model].get('kernels', default):
                kernel_id = kernel.get('id', default)
                if kernel_id in ini:
                    ini.remove(kernel_id)

    for x in ini:
        print("[-]   In {}, found {} kernel build profile, but not a matching kernel-id in YAML".format(INPUT_FILE, x), file=sys.stderr)




def main(argv):
    # Assign variables
    data = read_file(INPUT_FILE)

    # Get data (YAML)
    yml = yaml_parse(data)

    # Get data (INI)
    ini = ini_parse()

    # Compare YAML to directory structure
    compare_yml_dir(yml)

    # Compare YAML to INI
    compare_yml_ini(yml, ini)

    # Get data (directory)
    #   and Compare directory structure to YAML
    get_versions(yml)

    # Exit
    exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])
