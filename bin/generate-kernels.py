#!/usr/bin/env python3
from datetime import datetime
import sys
import yaml # $ python3 -m venv .env; source .env/bin/activate; python3 -m pip install pyyaml

INPUT_FILE = "./devices.yml"
OUTPUT_FILE = "./kernels.md"
qty_kernels = 0
qty_models = 0

## Input:
##   $ cat ./devices.yml
##   - angler:
##       model  : Google Nexus 6P
##       kernels:
##         - id          : angler
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


def yaml_parse(data):
    result = ""
    lines = data.split('\n')
    for line in lines:
        if not line.startswith('#'):
            ## YAML doesn't like tabs so let's replace them with four spaces
            result += "{}\n".format(line.replace('\t', '    '))
    return yaml.safe_load(result)


def get_kernels(yml):
    global qty_kernels, qty_models
    default = " " # Isn't a mistake to be a space - as if source is 'empty', messes up the <code> blocks (via `)
    kernels = []

    # Iterate over all the data
    for element in yml:
        # Iterate over all the device models
        for codename in element.keys():
            qty_models += 1
            model = element[codename].get('model', default)
            # Iterate over all the device model's kernels
            for kernel in element[codename].get('kernels', default):
                if 'versions' in kernel:
                    # Iterate over all device model kernels version's
                    for version in kernel.get('versions', default):
                        qty_kernels += 1
                        features = ""
                        if 'features' in version:
                            for f in version.get('features', default):
                                if features:
                                    features += ", "
                                features += f
                        kernels.append("| {} | {} | {} | {} | {} | {} | {} | {} | `{}` |".format(
                                                                                             model.ljust(12),
                                                                                             kernel.get('id', default).ljust(9),
                                                                                             version.get('android', default).ljust(41),
                                                                                             str(version.get('linux', default)).ljust(13),
                                                                                             version.get('kernel', default).ljust(14),
                                                                                             version.get('description', default).ljust(11),
                                                                                             features.ljust(8),
                                                                                             version.get('author', default).ljust(6),
                                                                                             version.get('source', default).ljust(6),
                                                                                     )
                                                                                 )
    return kernels


def generate_table(kernels):
    table  = "| Display Name | Kernel-ID | [Android Version](/android-versions.html) | Linux Version | Kernel Version | Description | Features | Author | Source |\n"
    table += "|--------------|-----------|-------------------------------------------|---------------|----------------|-------------|----------|--------|--------|\n"

    # Iterate over all the results
    for kernel in sorted(kernels):
        table += "{}\n".format(kernel)

    return table


def write_file(data, file):
    try:
        with open(file, 'w') as f:
            meta  = '---\n'
            meta += 'title: Kali NetHunter Kernels\n'
            meta += '---\n\n'
            stats  = "- Kali NetHunter has a total of [**{} kernels**](/kernels.html)\n".format(str(qty_kernels))
            stats += "  - These kernels can be used on [**{} device models**](/device-kernels.html)\n".format(str(qty_models))
            stats += "- [Kali NetHunter Statistics Overview](/index.html)\n\n"
            footer = "\n_This table was [generated automatically](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-kernels/-/blob/master/.gitlab-ci.yml) on {} from the [Kali NetHunter GitLab repository](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-kernels)_\n".format(datetime.now().strftime("%Y-%B-%d %H:%M:%S"))
            f.write(str(meta))
            f.write(str(stats))
            f.write(str(data))
            f.write(str(footer))
            f.close()
            print('[+] Writing: {}'.format(OUTPUT_FILE))
    except Exception as e:
        print("[-] Cannot write to output file: {} - {}".format(file, e), file=sys.stderr)


def print_stats():
    print('[i] Kernels      : {}'.format(qty_kernels))
    print('[i] Device models: {}'.format(qty_models))


def main(argv):
    # Read file in
    data = read_file(INPUT_FILE)

    # Get YAML file
    yml = yaml_parse(data)

    # Generate stats
    kernels = get_kernels(yml)

    # Print stats
    print_stats()

    # Generate markdown
    generated_markdown = generate_table(kernels)

    # Write markdown to file
    write_file(generated_markdown, OUTPUT_FILE)

if __name__ == "__main__":
    main(sys.argv[1:])
