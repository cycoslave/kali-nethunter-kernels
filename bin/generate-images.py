#!/usr/bin/env python3
from datetime import datetime
import sys
import yaml # $ python3 -m venv .env; source .env/bin/activate; python3 -m pip install pyyaml

INPUT_FILE = "./devices.yml"
OUTPUT_FILE = "./images.md"
qty_images = 0       # Total images (some devices can have multiple images)
qty_image_models = 0 # Device model which have images
qty_no_image = 0

## Input:
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
    global qty_image_models, qty_images, qty_no_image
    default = ""
    images = []

    # Iterate over all the data
    for element in yml:
        # Iterate over all the device models
        for codename in element.keys():
            if element[codename].get('images', default):
                qty_image_models += 1
            else:
                qty_no_image += 1

            for image in element[codename].get('images', default):
                qty_images += 1
                docs = image.get('docs', default)
                if docs:
                    docs = "<{}>".format(docs)
                images.append("| {} | {} | {} | {} | {} | {} | {} |".format(
                                                                              image.get('name', default).ljust(23),
                                                                              codename.ljust(8),
                                                                              image.get('id', default).ljust(9),
                                                                              image.get('android', default).ljust(41),
                                                                              image.get('rootfs', default).ljust(6),
                                                                              docs.ljust(53),
                                                                              image.get('note', default).strip('<br>').ljust(5)
                                                                             )
                                                                         )
    return images


def generate_table(images):
    table  = "| Image Name (Android OS) | Codename | Kernel-ID | [Android Version](/android-versions.html) | Rootfs | [Documentation](https://www.kali.org/docs/nethunter/) | Notes |\n"
    table += "|-------------------------|----------|-----------|-------------------------------------------|--------|-------------------------------------------------------|-------|\n"

    # Iterate over all the results
    for image in sorted(images):
        table += "{}\n".format(image)

    return table


def write_file(data, file):
    try:
        with open(file, 'w') as f:
            meta  = '---\n'
            meta += 'title: Kali NetHunter Pre-created Images\n'
            meta += '---\n\n'
            stats  = "- The [next release](https://www.kali.org/releases/) cycle will include [**{}** Kali NetHunter pre-created images](/images.html) ready to [download](https://www.kali.org/get-kali/#kali-mobile)\n".format(qty_images)
            stats += "  - These {} images covers [**{} device models**](/image-models.html)\n".format(qty_images, qty_image_models)
            stats += "  - Another **{} NetHunter images can be self-generated** using the [build-scripts](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-installer)\n".format(qty_no_image)
            stats += "  - Meaning, there is a **total of [{} NetHunter supported device models](/device-kernels.html)**\n".format(qty_image_models + qty_no_image)
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
    print('[i] Pre-created images: {}'.format(qty_images))
    print('[i] Total supported device models           : {}'.format(qty_image_models + qty_no_image))
    print('[i] Device models with pre-created images   : {}'.format(qty_image_models))
    print('[i] Device models without pre-created images: {}'.format(qty_no_image))


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
