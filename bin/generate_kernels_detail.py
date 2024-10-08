#!/usr/bin/env python3
from datetime import datetime
import sys
import yaml # $ python3 -m venv .env; source .env/bin/activate; python3 -m pip install pyyaml

OUTPUT_FILE = "./kernels.md"
INPUT_FILE = "./devices.yml"
repo_msg = "\n_This table was [generated automatically](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-devices/-/blob/master/.gitlab-ci.yml) on {} from the [Kali NetHunter GitLab repository](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-devices)_\n".format(datetime.now().strftime("%Y-%B-%d %H:%M:%S"))
qty_total_models = 0
qty_kernels_models = 0
qty_kernels = 0
qty_no_kernels = 0

## Input:
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


def generate_table(data):
    global qty_kernels, qty_no_kernels, qty_total_models, qty_kernels_models
    default = " " # Isn't a mistake to be a space - as if source is 'empty', messes up the <code> blocks (via `)
    kernels = []

    # iterate over all the models
    for element in data:
        # iterate over all the versions
        for kernel_name in element.keys():
            qty_total_models += 1
            model = element[kernel_name].get('model', default)
            if 'kernels' in element[kernel_name]:
                qty_kernels_models += 1
                for kernel in element[kernel_name].get('kernels', default):
                    for version in kernel.get('versions', default):
                        qty_kernels += 1
                        features = ""
                        i = 0
                        for f in version.get('features', default):
                            if i > 0:
                                features += ", "
                            features += f
                            i += 1
                        ## REF: https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-project/-/blob/master/nethunter-installer/build.py
                        #build_cmd = "./build.py -d {} --{} -fs full".format( kernel.get('id', default) version.get('android', default) )
                        kernels.append("| {} | {} | {} | {} | {} | {} | {} | {} | `{}` |\n".format(
                                                                                             model,
                                                                                             kernel.get('id', default),
                                                                                             version.get('android', default),
                                                                                             version.get('linux', default),
                                                                                             version.get('kernel', default),
                                                                                             version.get('description', default),
                                                                                             features,
                                                                                             version.get('author', default),
                                                                                             version.get('source', default)
                                                                                     )
                                                                                 )
            else:
                qty_no_kernels += 1

    table  = "| Display Name | Kernel ID | [Android Version](kernel-summary.html) | Linux Version | Kernel Version | Description | Features | Author | Source |\n"
    table += "|--------------|-----------|----------------------------------------|---------------|----------------|-------------|----------|--------|--------|\n"
    # iterate over all the kernels
    for kernel in sorted(kernels):
        table += "{}".format(kernel)

    return table


def write_file(data, file):
    try:
        with open(file, 'w') as f:
            meta  = '---\n'
            meta += 'title: Kali NetHunter Kernel Details\n'
            meta += '---\n\n'
            stats  = "- The official [Kali NetHunter repository](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-devices) is using [**{}** kernels](kernel-summary.html)\n".format(str(qty_kernels))
            stats += "  - See [here for more details about the kernels](kernels.html) _([config file](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-devices/-/blob/master/devices.yml))_\n"
            stats += "  - These kernels can be used on **{} device models**\n".format(str(qty_total_models))
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
    print('[i] Known kernels  : {}'.format(qty_kernels))
    print('[i] Missing kernels: {}'.format(qty_no_kernels))
    print('[i] Device models with kernels   : {}'.format(qty_kernels_models))
    print('[i] Total supported device models: {}'.format(qty_total_models))


def main(argv):
    # Assign variables
    data = read_file(INPUT_FILE)

    # Get data
    res = yaml_parse(data)

    # Generate stats & markdown
    generated_markdown = generate_table(res)

    # Print result
    print_summary()

    # Create markdown file
    write_file(generated_markdown, OUTPUT_FILE)

    # Exit
    exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])
