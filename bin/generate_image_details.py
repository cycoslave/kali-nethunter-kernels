#!/usr/bin/env python3
from datetime import datetime
import sys
import yaml # $ python3 -m venv .env; source .env/bin/activate; python3 -m pip install pyyaml

OUTPUT_FILE = "./images.md"
INPUT_FILE = "./devices.yml"
repo_msg = "\n_This table was [generated automatically](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-devices/-/blob/master/.gitlab-ci.yml) on {} from the [Kali NetHunter GitLab repository](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-devices)_\n".format(datetime.now().strftime("%Y-%B-%d %H:%M:%S"))
qty_total_models = 0
qty_images_models = 0
qty_images = 0
qty_no_images = 0

## Input:
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
    global qty_total_models, qty_images_models, qty_images, qty_no_images
    default = ""
    images = []

    # iterate over all the models
    for element in data:
        # iterate over all the versions
        for kernel_name in element.keys():
            qty_total_models += 1
            if 'images' in element[kernel_name]:
                qty_images_models += 1
                if len(element[kernel_name].get('images', default)) > 1:
                    print("[i]   Multiple images for: {}".format(element[kernel_name].get('model', default)))
                for image in element[kernel_name].get('images', default):
                    qty_images += 1
                    docs = image.get('docs', default)
                    if len(element[kernel_name].get('images', default)) > 1:
                        print("[i]     - {}".format(image.get('name', default)))
                    if docs:
                        docs = "<{}>".format(docs)
                    images.append("| {} | {} | {} | {} | {} | {} | {} | {} |\n".format(
                                                                                  image.get('name', default).ljust(25),
                                                                                  kernel_name.ljust(6),
                                                                                  image.get('id', default).ljust(9),
                                                                                  image.get('android', default).ljust(38),
                                                                                  image.get('rootfs', default).ljust(6),
                                                                                  image.get('status', default).ljust(6).title(),
                                                                                  docs.ljust(53),
                                                                                  image.get('note', default).strip('<br>').ljust(5)
                                                                                 )
                                                                             )
            else:
                qty_no_images += 1
                #print("[-] Possible issue with: {} (no images)".format(element[kernel_name].get('model', default)), file=sys.stderr)

    table  = "| Display Name (Android OS) | Device | Kernel ID | [Android Version](kernel-summary.html) | Rootfs | Status | [Documentation](https://www.kali.org/docs/nethunter/) | Notes |\n"
    table += "|---------------------------|--------|-----------|----------------------------------------|--------|--------|-------------------------------------------------------|-------|\n"
    # iterate over all the models
    for device in sorted(images):
        table += "{}".format(device)

    return table


def write_file(data, file):
    try:
        with open(file, 'w') as f:
            meta  = '---\n'
            meta += 'title: Kali NetHunter Pre-created Images\n'
            meta += '---\n\n'
            stats  = "- The [next release](https://www.kali.org/releases/) cycle will include [**{}** Kali NetHunter pre-created images](image-summary.html) ready to [download](https://www.kali.org/get-kali/#kali-mobile)\n".format(str(qty_images))
            stats += "  - See [here for more details about the pre-created images](images.html) _([config file](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-devices/-/blob/master/devices.yml))_\n"
            stats += "  - These {} images covers **{} device models**\n".format(str(qty_images), qty_images_models)
            #stats += "  - _Another {} NetHunter images can be self-generated using the build-scripts_\n".format(qty_no_images)
            #stats += "  - _Meaning, there is a **total of {} NetHunter supported images**_\n".format(qty_images + qty_no_images)
            #stats += "- _NetHunter is supported on a total of **{} device models**_\n".format(qty_total_models)
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
    print('[i] Pre-created images              : {}'.format(qty_images))
    print('[i] Pre-created images device models: {}'.format(qty_images_models))
    print('[i] Non pre-created images: {}'.format(qty_no_images))
    print('[i] Total supported images: {}'.format(qty_images + qty_no_images))
    print('[i] Total supported models: {}'.format(qty_total_models))


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
