#!/usr/bin/env python3
from datetime import datetime
import sys
import yaml # $ python3 -m venv .env; source .env/bin/activate; python3 -m pip install pyyaml

INPUT_FILE = "./devices.yml"
OUTPUT_FILE = "./image-models.md"
qty_images = 0       # Total images (some devices can have multiple images)
qty_image_models = 0 # Device model which have images

## Input:
##   $ cat ./devices.yml
##   - angler:
##       model  : Google Nexus 6P
##       images :
##         - id     : angler
##         - id     : angler-los

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


def get_images(yml):
    global qty_images, qty_image_models
    default = ""
    images = []

    # Iterate over all the data
    for element in yml:
        # Iterate over all the device models
        for codename in element.keys():
            devicemodel = element[codename].get('model', default)

            if 'images' in element[codename]:
                qty_image_models += 1
                i = len(element[codename].get('images', default))
                qty_images += i
                x = "{} ({})".format(devicemodel, codename)
                images.append("| {} | {} |".format(
                                                    x.ljust(23),
                                                    str(i).ljust(10),
                                                  )
                                                )
    return images


def generate_table(images):
    table  = "| Device Model (Codename) | Qty Images |\n"
    table += "|-------------------------|------------|\n"

    # Iterate over all the results
    for image in sorted(images):
        table += "{}\n".format(image)

    return table


def write_file(data, file):
    try:
        with open(file, 'w') as f:
            meta  = '---\n'
            meta += 'title: Kali NetHunter Device Modules Pre-created Images\n'
            meta += '---\n\n'
            stats  = "- The [next release](https://www.kali.org/releases/) cycle will pre-created images to support [**{}** model devices](/image-models.html)\n".format(qty_image_models)
            stats += "  - [**{}** pre-created images](/images.html) will able to [download](https://www.kali.org/get-kali/#kali-mobile)\n".format(qty_images)
            stats += "- [Kali NetHunter Statistics Overview](/index.html)\n\n"
            footer = "\n_This table was [generated automatically](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-devices/-/blob/master/.gitlab-ci.yml) on {} from the [Kali NetHunter GitLab repository](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-devices)_\n".format(datetime.now().strftime("%Y-%B-%d %H:%M:%S"))
            f.write(str(meta))
            f.write(str(stats))
            f.write(str(data))
            f.write(str(footer))
            f.close()
            print('[+] Writing: {}'.format(OUTPUT_FILE))
    except Exception as e:
        print("[-] Cannot write to output file: {} - {}".format(file, e), file=sys.stderr)


def print_stats():
    print('[i] Device models using pre-created images: {}'.format(qty_image_models))
    print('[i] Pre-created images                    : {}'.format(qty_images))


def main(argv):
    # Read file in
    data = read_file(INPUT_FILE)

    # Get YAML file
    yml = yaml_parse(data)

    # Generate stats
    images = get_images(yml)

    # Print stats
    print_stats()

    # Generate markdown
    generated_markdown = generate_table(images)

    # Write markdown to file
    write_file(generated_markdown, OUTPUT_FILE)

if __name__ == "__main__":
    main(sys.argv[1:])
