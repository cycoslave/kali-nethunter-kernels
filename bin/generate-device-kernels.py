#!/usr/bin/env python3
from datetime import datetime
import sys
import yaml # $ python3 -m venv .env; source .env/bin/activate; python3 -m pip install pyyaml

INPUT_FILE = "./devices.yml"
OUTPUT_FILE = "./device-kernels.md"
qty_models = 0       # Total device modules
qty_images = 0       # Total images (some devices can have multiple images)
qty_image_models = 0 # Device model which have images
qty_kernels = 0
qty_kernel_versions = 0

## Input:
##   $ cat ./devices.yml
##   - angler:
##       model  : Google Nexus 6P
##       images :
##         - id     : angler
##         - id     : angler-los
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
    global qty_models, qty_images, qty_image_models, qty_kernels, qty_kernel_versions
    default = ""
    devices = []

    # Iterate over all the data
    for element in yml:
        # Iterate over all the device models
        for codename in element.keys():
            qty_models += 1
            devicemodel = element[codename].get('model', default)

            if element[codename].get('images', default):
                qty_image_models += 1

            images_cnt = len(element[codename].get('images', default))
            qty_images += images_cnt
            images_cnt = '' if images_cnt == '0' else images_cnt

            kernel_cnt = len(element[codename].get('kernels', default))
            qty_kernels += kernel_cnt

            versions_cnt = 0
            for kernel in element[codename].get('kernels', default):
                versions_cnt += len(kernel.get('versions', default))
            qty_kernel_versions += versions_cnt

            x = "{} ({})".format(devicemodel, codename)
            devices.append("| {} | {} | {} | {} |".format(
                                                            x.ljust(23),
                                                            str(images_cnt).ljust(38),
                                                            str(kernel_cnt).ljust(11),
                                                            str(versions_cnt).ljust(67),
                                                          )
                                                        )
    return devices


def generate_table(devices):
    table  = "| Device Model (Codename) | [Qty Pre-created Images](/images.html) | Qty Kernels | [Qty Kernel Versions](/kernels.html) |\n"
    table += "|-------------------------|----------------------------------------|-------------|--------------------------------------|\n"

    # Iterate over all the results
    for device in sorted(devices):
        table += "{}\n".format(device)
    return table


def write_file(data, file):
    try:
        with open(file, 'w') as f:
            meta  = '---\n'
            meta += 'title: Kali NetHunter Device Modules Kernels\n'
            meta += '---\n\n'
            stats  = "- Kali NetHunter supports [**{} device modules**](/device-kernels.html)\n".format(qty_models)
            stats += "  - Of which [**{} devices**](/image-models.html) have [**{} pre-created images**](/images.html)\n".format(qty_image_models, qty_images)
            stats += "  - There is a total of **{} kernels**, made up of [**{} kernel versions**](/kernels.html) _(= device modules * <!-- device modules--> kernels * <!--device module--> [Android versions](/android-version.html))_\n".format(qty_kernels, qty_kernel_versions)
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
    print('[i] Device models     : {}'.format(qty_models))
    print('[i] Device models with pre-created images: {}'.format(qty_image_models))
    print('[i] Pre-created images: {}'.format(qty_images))
    print('[i] Kernels           : {}'.format(qty_kernels))
    print('[i] Kernel versions   : {}'.format(qty_kernel_versions))


def main(argv):
    # Read file in
    data = read_file(INPUT_FILE)

    # Get YAML file
    yml = yaml_parse(data)

    # Generate stats
    devices = get_android_versions(yml)

    # Print stats
    print_stats()

    # Generate markdown
    generated_markdown = generate_table(devices)

    # Write markdown to file
    write_file(generated_markdown, OUTPUT_FILE)

if __name__ == "__main__":
    main(sys.argv[1:])
