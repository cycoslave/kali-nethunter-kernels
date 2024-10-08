#!/usr/bin/env python3
from datetime import datetime
import os
import sys
import yaml # $ python3 -m venv .env; source .env/bin/activate; python3 -m pip install pyyaml

OUTPUT_FILE = "./kernel-summary.md"
INPUT_FILE = "./devices.yml"
ROOT_DIR = "./"
repo_msg = "\n_This table was [generated automatically](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-devices/-/blob/master/.gitlab-ci.yml) on {} from the [Kali NetHunter GitLab repository](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-devices)_\n".format(datetime.now().strftime("%Y-%B-%d %H:%M:%S"))

## Input:
##   $ ls -l
##   ./
##    |---> [Android Version]/
##        |-> [Device-ROM]/
##   $ cat ./devices.yml
##   - angler:
##       model  : Google Nexus 6P
##       images :
##         - id     : angler
##           name   : Google Nexus 6P (Oreo)
##           android: oreo
##           status : stable
##           rootfs : full
##           docs   : "https://forum.xda-developers.com/t/rom-official-kali-nethunter-for-the-huawei-nexus-6p-android-8-1.4080807/"
##           note   : >-
##                    Nexmon support<br>
##                    **Our preferred low end device**
##         - id     : angler-los
##           name   : Google Nexus 6P (LineageOS 17.1)
##           android: ten
##           status : latest
##           rootfs : full
##           docs   : "https://forum.xda-developers.com/t/rom-official-kali-nethunter-for-the-huawei-nexus-6p-los17-1.4079087/"
##           note   : >-
##                    Nexmon support<br>
##                    **Our preferred low end device**<br>
##                    Warning: Android Ten is still experimental
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


def yml_parse(data):
    result = ""
    lines = data.split('\n')
    for line in lines:
        if not line.startswith('#'):
            ## yaml doesn't like tabs so let's replace them with four spaces
            result += "{}\n".format(line.replace('\t', '    '))
    return yaml.safe_load(result)


def check_yml(yml):
    print("[i] Checking YAML's values")

    default = ""
    # iterate over all device models
    for element in yml:
        # iterate over all model's entries in yaml file
        for device_model in element.keys():

            for key in element[device_model].keys():
                match key:
                    case 'model' | 'images' | 'kernels':
                        continue
                    case _:
                        print("[-]   Found unknown value '{} -> {}': {}".format(device_model, key, element[device_model].get(key, default)), file=sys.stderr)

            for image in element[device_model].get('images', default):
                for key in list(image.keys()):
                    match key:
                        case 'id' | 'name' | 'android' | 'status' | 'rootfs' | 'docs' | 'note':
                            continue
                        case _:
                            print("[-]   Found unknown value '{} -> images -> {}': {}".format(device_model, key, image.get(key, default)), file=sys.stderr)

            for kernel in element[device_model].get('kernels', default):
                for key in list(kernel.keys()):
                    match key:
                        case 'id' | 'description' | 'versions' | 'arch' | 'flasher' | 'kernelstring' | 'ramdisk' | 'block' | 'devicenames' | 'resolution' | 'version' | 'supersu':
                            continue
                        case 'modules' | 'slot_device' :
                            if kernel.get('flasher', default) == 'anykernel':
                                continue
                            else:
                                print("[-]   Not using anykernel flasher, so can't use value '{} -> kernels -> {}': {}".format(device_model, key, build.get(key, default)), file=sys.stderr)
                        case _:
                            print("[-]   Found unknown value '{} -> kernels -> {}': {}".format(device_model, key, kernel.get(key, default)), file=sys.stderr)

                for version in kernel.get('versions', default):
                    for key in list(version.keys()):
                        match key:
                            case 'android' | 'linux' | 'kernel' | 'description' | 'author' | 'source' | 'features':
                                continue
                            case _:
                                print("[-]   Found unknown value '{} -> kernels -> versions -> {}': {}".format(device_model, key, version.get(key, default)), file=sys.stderr)


def compare_yml(yml):
    print("[i] Checking YAML's <models>: images <-> kernels")

    default = ""
    # iterate over all device models
    for element in yml:
        # iterate over all model's entries in yaml file
        for device_model in element.keys():
            image_array = []
            kernel_array = []

            for image in element[device_model].get('images', default):
                image_array.append(image.get('id', default))

            for kernel in element[device_model].get('kernels', default):
                kernel_array.append(kernel.get('id', default))

            for image in image_array:
                if image not in kernel_array:
                    print("[-]   Found unknown image id, without matching kernel id: {} -> images -> id: {}".format(device_model, image), file=sys.stderr)

            for kernel in kernel_array:
                if kernel not in kernel_array:
                    print("[-]   Found unknown kernel id, without matching kernel id: {} -> kernels -> id: {}".format(device_model, kernel), file=sys.stderr)


def compare_yml_dir(yml):
    print("[i] Comparing YAML: {} -> {}*".format(INPUT_FILE, ROOT_DIR))

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

                for version in kernel.get('versions', default):
                    android_version = version.get('android', default)
                    path = os.path.join(ROOT_DIR, android_version, kernel_id)
                    if not os.path.isdir(path):
                        print("[-]   In {}, found model ({}/{}), but missing on disk: {}".format(INPUT_FILE, device_model, model, path), file=sys.stderr)


def get_versions(yml):
    # Discovery directories
    subdirectories = [ x.path for x in os.scandir(ROOT_DIR) if x.is_dir() and not x.path.startswith('{}.'.format(ROOT_DIR))]
    # Remove non Android version directories
    subdirectories.remove('{}bin'.format(ROOT_DIR))
    subdirectories.remove('{}example_scripts'.format(ROOT_DIR))
    subdirectories.remove('{}patches'.format(ROOT_DIR))

    for android_version_dir in subdirectories:
        android_version_dir = android_version_dir.lower()
        android_version_dir = android_version_dir.replace(ROOT_DIR, '')
        print("[i] Comparing dir: {}{}/* -> {}".format(ROOT_DIR, android_version_dir, INPUT_FILE))

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
                    for version in kernel.get('versions', default):
                        android_version = version.get('android', default)
                        # have we got a kernel version match?
                        if android_version == android_version_dir:
                            return

    print("[-]   Found on disk ({}), but hasn't be added to: {}".format(path,  INPUT_FILE), file=sys.stderr)


def main(argv):
    # Assign variables
    data = read_file(INPUT_FILE)

    # Get data (YAML)
    yml = yml_parse(data)

    # Check YAML keys
    check_yml(yml)

    # Compare YAML's sections (images & kernels)
    compare_yml(yml)

    # Compare YAML to directory structure
    compare_yml_dir(yml)

    # Get data (directory)
    #   and compare directory structure to YAML
    get_versions(yml)

    # Exit
    exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])
