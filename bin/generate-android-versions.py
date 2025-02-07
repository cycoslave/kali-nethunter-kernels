#!/usr/bin/env python3
from datetime import datetime
import sys
import yaml # $ python3 -m venv .env; source .env/bin/activate; python3 -m pip install pyyaml

INPUT_FILE = "./devices.yml"
OUTPUT_FILE = "./android-versions.md"
qty_kernel_versions = 0
android_versions = {}

## Input:
##   $ cat ./devices.yml
##   - angler:
##       kernels:
##         - id          : angler
##           versions    :
##             - android    : marshmallow
##             - android    : nougat
##             - android    : oreo
##         - id          : angler-los
##           versions    :
##             - android    : ten

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


def get_android_versions(yml):
    default = ""
    yml_kernels = {}

    # Iterate over all the data
    for element in yml:
        # Iterate over all the device models
        for codename in element.keys():
            # Iterate over all the device model's kernels
            for kernel in element[codename].get('kernels', default):
                # Iterate over all device model kernels version's
                for version in kernel.get('versions', default):
                    android_version = version.get('android', default)
                    # Make the name a little bit more end-user friendly
                    android_version = android_version.title()
                    # If updating, make sure to update: ./kali-docs/nethunter/installing-nethunter/index.md
                    #                                   ./kali-nethunter-kernels/bin/generate-android-versions.py
                    android_version = android_version.replace('Kitkat', '4.4 - KitKat')
                    android_version = android_version.replace('Lollipop', '5.0 - Lollipop')
                    android_version = android_version.replace('Marshmallow', '6 - Marshmallow')
                    android_version = android_version.replace('Nougat', '7 - Nougat')
                    android_version = android_version.replace('Oreo', '8 - Oreo')
                    android_version = android_version.replace('Pie', '9 - Pie')
                    android_version = android_version.replace('Ten', '10 - Ten')
                    android_version = android_version.replace('Eleven', '11 - Eleven')
                    android_version = android_version.replace('Twelve', '12 - Twelve')
                    android_version = android_version.replace('Thirteen', '13 - Thirteen')
                    android_version = android_version.replace('Fourteen', '14 - Fourteen')
                    android_version = android_version.replace('Fifteen', '15 - Fifteen')
                    android_version = android_version.replace('Wearos', 'Wear OS')
                    if android_version not in yml_kernels:
                        yml_kernels[android_version] = 0
                    yml_kernels[android_version] += 1
    return yml_kernels


def count_android_versions(android_versions):
    i = 0
    for version in android_versions:
        i += android_versions[version]
    return i


def generate_table(qty_kernel_versions):
    table  = "| Android Version | Qty |\n"
    table += "|-----------------|-----|\n"

    # Iterate over all the results
    for version in sorted(android_versions):
        table += "| {} | {} |\n".format(
                                        version.ljust(15),
                                        str(android_versions[version]).ljust(3)
                                        )
    return table


def write_file(data, file):
    global qty_kernel_versions, android_versions
    try:
        with open(file, 'w') as f:
            meta  = '---\n'
            meta += 'title: Kali NetHunter Android Versions\n'
            meta += '---\n\n'
            stats  = "- Kali NetHunter is on [**{} Android versions**](/android-version.html)\n".format(len(android_versions))
            stats += "  - There is a total of [**{} kernel versions**](/kernels.html) _(= device modules * <!-- device modules--> kernels * <!--device module--> [Android versions](/android-version.html))_\n".format(qty_kernel_versions)
            stats += "- [Kali NetHunter Statistics Overview](/index.html)\n\n"
            footer = "\n_This table was [generated automatically](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-kernels/-/blob/main/.gitlab-ci.yml) on {} from the [Kali NetHunter GitLab repository](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-kernels)_\n".format(datetime.now().strftime("%Y-%B-%d %H:%M:%S"))
            f.write(str(meta))
            f.write(str(stats))
            f.write(str(data))
            f.write(str(footer))
            f.close()
            print('[+] Writing: {}'.format(OUTPUT_FILE))
    except Exception as e:
        print("[-] Cannot write to output file: {} - {}".format(file, e), file=sys.stderr)


def print_stats():
    global qty_kernel_versions, android_versions
    print('[i] Android versions: {}'.format(len(android_versions)))
    print('[i] Kernel versions : {}'.format(qty_kernel_versions))


def main(argv):
    global qty_kernel_versions, android_versions
    # Read file in
    data = read_file(INPUT_FILE)

    # Get YAML file
    yml = yaml_parse(data)

    # Get all Android versions
    android_versions = get_android_versions(yml)

    # Count all kernels versions
    qty_kernel_versions = count_android_versions(android_versions)

    # Print stats
    print_stats()

    # Generate markdown
    generated_markdown = generate_table(qty_kernel_versions)

    # Write markdown to file
    write_file(generated_markdown, OUTPUT_FILE)

if __name__ == "__main__":
    main(sys.argv[1:])
