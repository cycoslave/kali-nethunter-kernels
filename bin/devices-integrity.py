#!/usr/bin/env python3
from datetime import datetime
import os
import sys
import yaml # $ python3 -m venv .env; source .env/bin/activate; python3 -m pip install pyyaml

OUTPUT_FILE = "./kernel-summary.md"
INPUT_FILE = "./devices.yml"
ROOT_DIR = "./"
qty_dir_kernels = 0
qty_yml_kernels = 0

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
##           docs   : "https://forum.xda-developers.com/t/rom-official-kali-nethunter-for-the-huawei-nexus-6p-android-8-1.4080807/"
##           note   : >-
##                    Nexmon support<br>
##                    **Our preferred low end device**
##         - id     : angler-los
##           name   : Google Nexus 6P (LineageOS 17.1)
##           android: ten
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
##               features   : [BT_RFCOMM, CDROM, HID, Injection, Nexmon, RTL8812AU, RTL8188EUS, Internal_BT]
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
##               features   : [BT_RFCOMM, HID, Injection, Nexmon, RTL8812AU, Internal_BT, RTL8188EUS]

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
        for codename in element.keys():

            for key in element[codename].keys():
                match key:
                    case 'model' | 'images' | 'kernels':
                        continue
                    case _:
                        print("[-]   Found unknown value '{} -> {}': {}".format(codename, key, element[codename].get(key, default)), file=sys.stderr)

            # Useful for troubleshoot only
            #if len(element[codename].get('images', default)) > 1:
            #    print("[i]   Multiple images for: {}".format(codename))
            # Disabling as its optional to have pre-created image section - useful for troubleshoot only
            #if not element[codename].get('images', default):
            #    print("[-]   {} doesn't have a image section".format(codename), file=sys.stderr)
            for image in element[codename].get('images', default):
            # Useful for troubleshoot only
            #    if len(element[codename].get('images', default)) > 1:
            #        print("[i]     - {}".format(image.get('name', default)))
                for key in list(image.keys()):
                    match key:
                        case 'id' | 'name' | 'android' | 'rootfs' | 'docs' | 'note':
                            continue
                        case _:
                            print("[-]   Found unknown value '{} -> images -> {}': {}".format(codename, key, image.get(key, default)), file=sys.stderr)

            if not element[codename].get('kernels', default):
                print("[-]   {} doesn't have a kernel section".format(codename), file=sys.stderr)
            for kernel in element[codename].get('kernels', default):
                for key in list(kernel.keys()):
                    match key:
                        case 'id' | 'description' | 'versions' | 'arch' | 'flasher' | 'kernelstring' | 'ramdisk' | 'block' | 'devicenames' | 'resolution' | 'version' | 'supersu':
                            continue
                        case 'modules' | 'slot_device' :
                            if kernel.get('flasher', default) == 'anykernel':
                                continue
                            else:
                                print("[-]   Not using anykernel flasher, so can't use value '{} -> kernels -> {}': {}".format(codename, key, build.get(key, default)), file=sys.stderr)
                        case _:
                            print("[-]   Found unknown value '{} -> kernels -> {}': {}".format(codename, key, kernel.get(key, default)), file=sys.stderr)

                for version in kernel.get('versions', default):
                    for key in list(version.keys()):
                        match key:
                            case 'android' | 'linux' | 'kernel' | 'description' | 'author' | 'source' | 'features':
                                continue
                            case _:
                                print("[-]   Found unknown value '{} -> kernels -> versions -> {}': {}".format(codename, key, version.get(key, default)), file=sys.stderr)

                    #for feature in version.get('features', default):
                    #    match feature:
                    #        case 'BT_RFCOMM' | 'Internal_BT' | 'RTL-BT' | 'CDROM'| 'HID' | 'HID-4' | 'Injection' | 'Nexmon' | 'QCACLD' | 'ATH9K_HTC' | 'RTL8188EUS' | 'RTL8812AU' | 'RTL88XXAU' | 'NFS' :
                    #            continue
                    #        case _:
                    #            print("[-]   Found unknown value: {} -> kernels -> versions -> {} -> features -> {}".format(device_model, version.get('android', default), feature), file=sys.stderr)

def compare_yml(yml):
    print("[i] Checking YAML's <models>: images <-> kernels")

    default = ""
    # iterate over all device models
    for element in yml:
        # iterate over all model's entries in yaml file
        for codename in element.keys():
            image_array = []
            kernel_array = []

            for image in element[codename].get('images', default):
                image_array.append(image.get('id', default))

            for kernel in element[codename].get('kernels', default):
                kernel_array.append(kernel.get('id', default))

            for image in image_array:
                if image not in kernel_array:
                    print("[-]   Found image id, without matching kernel id: {} -> images -> id: {}".format(codename, image), file=sys.stderr)

            # Disabling as its optional to have pre-created image section - useful for troubleshoot only
            #for kernel in kernel_array:
            #    if kernel not in image_array:
            #        print("[-]   Found kernel id, without matching image id: {} -> images -> id: {}".format(codename, kernel), file=sys.stderr)


def compare_yml_dir(yml):
    print("[i] Comparing YAML: {} -> {}*".format(INPUT_FILE, ROOT_DIR))

    default = ""
    # iterate over all device models
    for element in yml:
        # iterate over all model's entries in yaml file
        for codename in element.keys():
            model = element[codename].get('model', default)

            # is there a kernel entry in the YAML file?
            if 'kernels' not in element[codename]:
                print("[-]   In {}, found model ({}/{}), but is missing kernel entry".format(INPUT_FILE, codename, model), file=sys.stderr)

            kernels = [x['id'] for x in element[codename].get('kernels', default)]
            dup_kernels = {x for x in kernels if kernels.count(x) > 1}
            if dup_kernels:
                print("[-]   In {}, found model ({}/{}), but has multiple kernels with the same ID: {}".format(INPUT_FILE, codename, model, dup_kernels), file=sys.stderr)

            for kernel in element[codename].get('kernels', default):
                kernel_id = kernel.get('id', default)
                if not kernel_id.startswith(codename):
                    print("[-]   In {}, kernel_id doesn't start with model id: model: {}   kernel_id: {}".format(INPUT_FILE, codename, kernel_id), file=sys.stderr)

                versions = [x['android'] for x in kernel.get('versions', default)]
                dup_versions = {x for x in versions if versions.count(x) > 1}
                if dup_versions:
                    print("[-]   In {}, found model ({}/{}), but {} kernel id with multiple same android version: {}".format(INPUT_FILE, codename, model, kernel_id, dup_versions), file=sys.stderr)

                for version in kernel.get('versions', default):
                    android_version = version.get('android', default)
                    path = os.path.join(ROOT_DIR, android_version, kernel_id)
                    if not os.path.isdir(path):
                        print("[-]   In {}, found model ({}/{}), but missing on disk: {}".format(INPUT_FILE, codename, model, path), file=sys.stderr)


def get_dir_versions():
    # Discovery directories
    subdirectories = [ x.path for x in os.scandir(ROOT_DIR) if x.is_dir() and not x.path.startswith('{}.'.format(ROOT_DIR))]
    # Remove non Android version directories
    subdirectories.remove('{}bin'.format(ROOT_DIR))
    subdirectories.remove('{}example_scripts'.format(ROOT_DIR))
    subdirectories.remove('{}patches'.format(ROOT_DIR))
    return subdirectories


def compare_dir_yml(subdirectories, yml):
    for android_version_dir in subdirectories:
        android_version_dir = android_version_dir.lower()
        android_version_dir = android_version_dir.replace(ROOT_DIR, '')
        print("[i] Comparing dir: {}{}/* -> {}".format(ROOT_DIR, android_version_dir, INPUT_FILE))

        root, dirs, files = next(os.walk(android_version_dir))
        for kernel_id_dir in dirs:
            do_compare_dir_yml(android_version_dir, kernel_id_dir, yml)


def do_compare_dir_yml(android_version_dir, kernel_id_dir, yml):
    default = ""
    path = os.path.join(ROOT_DIR, android_version_dir, kernel_id_dir)

    # iterate over all device models
    for element in yml:
        # iterate over all model's entries in yaml file
        for codename in element.keys():
            # iterate over all model's kernels
            for kernel in element[codename].get('kernels', default):
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


def count_kernel_dir(subdirectories):
    i = 0
    for android_version_dir in subdirectories:
        android_version_dir = android_version_dir.lower()
        android_version_dir = android_version_dir.replace(ROOT_DIR, '')
        x = android_version_dir.title()
        x = x.replace('Kitkat', '4.4 - KitKat')
        x = x.replace('Lollipop', '5.0 - Lollipop')
        x = x.replace('Marshmallow', '6 - Marshmallow')
        x = x.replace('Nougat', '7 - Nougat')
        x = x.replace('Preo', '8 - Oreo')
        x = x.replace('Pie', '9 - Pie')
        x = x.replace('Ten', '10 - Ten')
        x = x.replace('Eleven', '11 - Eleven')
        x = x.replace('Twelve', '12 - Twelve')
        x = x.replace('Thirteen', '13 - Thirteen')
        x = x.replace('Fourteen', '14 - Fourteen')
        x = x.replace('Wearos', 'Wear OS')
        path = ROOT_DIR + android_version_dir
        i += dir_count(path)
    return i


def dir_count(path):
    print('[i] Searching in: {}'.format(path))
    root, dirs, files = next(os.walk(path))
    return len(dirs)


def count_kernel_yml(yml):
    default = ""
    yml_kernels = []

    # iterate over all the data
    for element in yml:
        # iterate over all the device models
        for codename in element.keys():
            for kernel in element[codename].get('kernels', default):
                # iterate over all model kernels version's
                for version in kernel.get('versions', default):
                    android_version = version.get('android', default)
                    yml_kernels.append(android_version)
    return len(yml_kernels)


def print_stats(qty_dir_kernels, qty_yml_kernels):
    print('[i] Kernels in directories : {}'.format(qty_dir_kernels))
    print('[i] Kernels in YAML kernels: {}'.format(qty_yml_kernels))


def main(argv):
    # Read file in
    data = read_file(INPUT_FILE)

    # Get YAML file
    yml = yml_parse(data)

    # Get directory structure
    directories = get_dir_versions()

    # Check YAML keys/values
    check_yml(yml)

    # Lookup YAML's sections (images & kernels)
    compare_yml(yml)

    # Compare YAML to directory structure
    compare_yml_dir(yml)

    # Compare directory structure to YAML
    compare_dir_yml(directories, yml)

    # Generate stats
    qty_dir_kernels = count_kernel_dir(directories)
    qty_yml_kernels = count_kernel_yml(yml)

    # Print stats
    print_stats(qty_dir_kernels, qty_yml_kernels)

if __name__ == "__main__":
    main(sys.argv[1:])
