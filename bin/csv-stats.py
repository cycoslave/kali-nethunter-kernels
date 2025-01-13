#!/usr/bin/env python3
# $ python3 -m venv .env; source .env/bin/activate; python3 -m pip install gitpython requests pyyaml
# $ ./$0
#
# The "Kali NetHunter Project" repository used to contain "everything". Over the years, items started to split out into their own:
# 2014-09-20: NetHunter 1.0.0 ~ Kali NetHunter Project repo created
#   https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-project/-/commit/4b294d10d39a07a28bef533d20c253d06494c7f6
# 2016-01-06: NetHunter 3.0.0 ~ Kali NetHunter Project starts to use use "/installer" sub-directory
#   https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-project/-/commit/e3f086d561b8efcde5689ac9d6da1044f085cbab
#   https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-installer/-/commit/022cc3ae7dacd4fcc8ad9fdb5d0cf2d28d38b2b8
# 2016-07-18: Kali 2016.2 ~ Kali NetHunter Kernel repo created
#   https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-project/-/commit/cf93429d3773cec12160886072627d5951163e61
#   https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-kernels/-/commit/30b515f19d3bbbd24fc1ad9e27847b22ba66ed22
# 2024-10-10: Kali 2024.4 ~ Kali NetHunter Installer repo created using Project's /installer sub-direcotry
#   https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-project/-/commit/0bd99b6c2f64ae883398874233c3ec99faf96404
#   https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-installer/-/commit/d6251ea19baf2900615edb3f3af60736fe39cf15
#
# --[ devices.yml
#   - Kali 2024.4+
#   - Method "#3"
#   - Production, deployment & metrics ("everything" file)
#   - YML - Builder, Kernels, Images & GitLab CI Web pages
# --[ devices.cfg
#   - Kali/NetHunter 3.0.0 <= 2024.3
#       https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-kernels/-/commit/de27dd5a1a0e67adb4e139b124c9c5021c0fe639
#       https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-installer/-/commit/3ce3bd67f7e5f055e6636434bf49a22fc9175145
#  - Method "#0, #1 & #2"
#  - Production
#   - INI  - kali-nethunter-installer: ./build.py              (Builder)
#            Used during building process
#            Supports multiple ROMs per device, so can't use it for devices
#   - YAML - kali-nethunter-installer: ./prep-release.py       (Pre-generated images)
#            kali-nethunter-kernels: ./bin/generate*images*.py (GitLab CI Web pages)
#            Which images gets pre-generated to release (aka images)
#            Doesn't have everything, so can't use it for devices
# --[ kernels.yml
#   - Kali 2020.2 <= 2024.3
#   - Method "#2"
#   - Metrics
#       https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-kernels/-/commit/d99c8d539c6bf2bde4ddc8a4fb8d132344e38206
#   - YAML - kali-nethunter-kernels: ./bin/generate*kernels*.py (GitLab CI Web pages)
#            Indexes the binary files (aka Kernel)
#            Best bet for devices - but wasn't always kept in-sync with the builder (devices.cfg INI) - as not used a huge amount, making it easy to miss
# --[ kernels.txt
#   - Kali/NetHunter 3.0 <= 2020.1
#       https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-kernels/-/commit/98dfa1252ee799bfe28f334889ccd1ee2cf7384f
#   - Method "#0 & #1"
#   - Deployment
#   - TXT
# --[ androidmenu.sh
#   - Kali/NetHunter 1.0 <= 2.0
#     - Outside of this repo ~ https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-project/
#   - Method "#0"
#   - Production
#   - Static/SHell (TXT?)
#
# | Terms      | Breakdown/Explanation                  | Example                                                                                        |
# |------------|----------------------------------------|------------------------------------------------------------------------------------------------|
# | ROM        | The OS used                            | LineageOS or OxygenOS or Stock                                                                 |
# | Devices    | Device (model - psychical item)        | OnePlus 2 / Google Nexus 6P                                                                    |
# | Buildables | Device + ROM                           | OnePlus 2 using LineageOS or OxygenOS                                                          |
# | Kernels    | Device + ROM + Android version         | OnePlus 2 using LineageOS 16.0 (Android "Pie" 9.0) or OxygenOS 3 (Android "Marshmallow" 6.0)   |
# | Images     | Pre-generated images that are released | OnePlus 2 LineageOS 16.0 (Android "Pie" 9.0)
#
# Prior to 2024.4, there was multiple places in even more places would need to be updated (e.g. YAML + YAML & INI) - as a result, it was easy to get out-of-sync between them
#   As a result, the numbers are "rough"
#   There was a clean up done when everything was merged into a single file and format, but wasn't backported to previous commits, means data may not exact
#   REF: https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-kernels/-/commit/6b6d383ef1282eec59ac7bed551c4e33937a0aa7
#        https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-kernels/-/commit/6b6d383ef1282eec59ac7bed551c4e33937a0aa7
#
# Another issue is, the git tags don't always align with release
#   Git tags are/were automatically generated based on release date, not build for the release date
#   Example, kali-2021.2. Git Tag: 2021-05-31 date, on 2021-05-25 Pocophone F1/beryllium support added, however images wasn't created for release.
#   REF: https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-kernels/-/commit/951738bbb3c2508cba9ce1f03aa29c1a00f8c16d
#        https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-kernels/-/commit/068a6d952b56d463f71a7e97d624d8bb980a8507
#   Add on the fact, Kali NetHunter release-cycle previously was created outside of Kali's release cycle (3 weeks ahead of release date at times), means data may not exact (again)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import configparser
import git
import os
import re
import requests
import sys
import yaml

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# | NetHunter | Devices | Images | Kalifs   | Release Date | REF                                                                                                                                   |
# |-----------|---------|--------|----------|--------------|---------------------------------------------------------------------------------------------------------------------------------------|
# | 1.0.0     | 4       | 4      | 1.0.9 ?? |   2014-09-23 | https://x.com/kalilinux/status/514404154933260288                                                                                     |
# | 1.0.2     | 5       | 5      | 1.0.9a   |   2014-09-30 | https://www.offsec.com/blog/kali-nexus-nethunter-1-0-2/                                                                               |
# | 1.1.0     | 6       | 6      | 1.0.9a   |   2015-01-05 | https://www.offsec.com/blog/nethunter-1-1-released/                                                                                   |
# | 1.2.0     | 8 ??    | 11 ??  | 1.1.0 ?? |   2015-04-01 | https://www.offsec.com/blog/nethunter-1-2-lollipop-nexus-six-and-nine/                                                                |
# | 1.2.1     | 8       | 11     | 1.1.0    | < 2015-04-21 | https://web.archive.org/web/20150421030801/https://www.offensive-security.com/kali-linux-nethunter-download/                          |
# | 2.0.0     | 7       | 12     | 1.1.0    |   2015-08-11 | https://www.kali.org/blog/kali-linux-2-0-release/#kali-linux-20-arm-images--nethunter-20                                              |
# | 3.0.0     | 8       | 12     | 2.0      |   2016-01-06 | https://www.offsec.com/blog/nethunter-3-0-released/                                                                                   |
# | 3.1.0 [*] | 13      | 20     | 2016.1   |   2016-07-07 | `curl -s -I https://old.kali.org/nethunter-images/nethunter-3.1/nethunter-3.1-flo-marshmallow-kalifs-full.zip | grep Last-Modified `  |
# | 3.27 [*]  | 7       | 7      | 2016.2   |   2016-11-20 | `curl -s -I https://old.kali.org/nethunter-images/nethunter-3.27/nethunter-3.27-flo-marshmallow-kalifs-full.zip | grep Last-Modified` |
# | 2019.2    | 12      | 17     | 2019.2   |   2019-05-21 | https://www.kali.org/blog/kali-linux-2019-2-release/                                                                                  |
# [*] = Non-released builds

# This is "static" as its was done outside of this repo
method0_static = [
    # NetHunter 1.0.0 -> 2.0.0
    #   Kernels: 5 = https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-project/-/tree/nethunter-x.x.x/devices/frozen_kernels/4.4.4

    # https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-project/-/tree/nethunter-1.0.0
    #   Devices   : $ find devices/ -type f -maxdepth 1 | wc -l
    #   Buildables: $ grep -c 'Build All.*Android' androidmenu.sh
    #   Kernels   ; $ grep '# git clone https://github.com' androidmenu.sh | grep -vc 'github.com/offensive-security\|binkybear/kali-scripts'
    #   Kernels   : $ grep -Rh 'git clone' devices/ | sort -u | wc -l
    #   Images    : https://web.archive.org/web/20140926010944/https://www.offensive-security.com/kali-linux-nethunter-download/
    ["1.0.0", 4, 6, 6, 4],

    # https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-project/-/tree/nethunter-1.0.2
    #   Devices   : $ find devices/ -type f -maxdepth 1 | wc -l
    #   Buildables: $ grep -c 'Build All.*Android' androidmenu.sh
    #   Kernels   : $ grep '# git clone https://github.com' androidmenu.sh | grep -vc 'github.com/offensive-security\|binkybear/kali-scripts'
    #   Kernels   : $ grep -Rh 'git clone' devices/ | sort -u | wc -l
    #   Images    : https://web.archive.org/web/20141001232758/http://www.offensive-security.com/kali-linux-nethunter-download/
    ["1.0.2", 7, 12, 12, 5],

    # https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-project/-/tree/nethunter-1.1.0
    #   Devices   : $ find devices/ -type f -maxdepth 1 | wc -l
    #   Devices   : $ grep '# - ' androidmenu.sh | grep -vc 'Toolchain'   # Should do -2 off the total, as Samsung Galaxy S4/S5 are not valid
    #   Buildables: $ grep -c 'Build All.*Android' androidmenu.sh         # Should do -4 off the total, as Samsung Galaxy S4/S5's Android 4/5 are not valid
    #   Kernels   : $ grep '# git clone https://github.com' androidmenu.sh | grep -vc 'github.com/offensive-security\|##########\|galaxy'   # Removing Samsung Galaxy S4/S5
    #   Kernels   : $ grep -Rh 'git clone' devices/ | grep -v 'android.googlesource.com\|#####' | sort -u | wc -l   # Extra kernel for nexus7-flo-deb
    #   Images    : https://web.archive.org/web/20150107004306/https://www.offensive-security.com/kali-linux-nethunter-download/
    ["1.1.0", 8, 15, 13, 6],

    # https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-project/-/tree/nethunter-1.2.0
    #   Devices   : $ find devices/ -type f -maxdepth 1 | wc -l
    #   Devices   : $ grep '# - ' androidmenu.sh | grep -vc 'Toolchain'   # Should do -2 off the total, as Samsung Galaxy S4/S5 are not valid
    #   Buildables: $ grep -c 'Build All.*Android' androidmenu.sh         # Should do -4 off the total, as Samsung Galaxy S4/S5's Android 4/5 are not valid
    #   Kernels   : $ grep '# git clone https://github.com' androidmenu.sh | grep -vc 'github.com/offensive-security\|##########\|galaxy'   # Removing Samsung Galaxy S4/S5
    #   Kernels   : $ grep -Rh 'git clone' devices/ | grep -v 'android.googlesource.com\|#####' | sort -u | wc -l   # Extra kernel for nexus7-flo-deb
    #   Images    : https://www.offsec.com/blog/nethunter-1-2-lollipop-nexus-six-and-nine/
    ["1.2.0", 8, 15, 15, 11],

    # https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-project/-/tree/nethunter-1.2.1
    #   Devices   : $ find devices/ -type f -maxdepth 1 | wc -l
    #   Devices   : $ grep '# - ' androidmenu.sh | grep -vc 'Toolchain'   # Should do -2 off the total, as Samsung Galaxy S4/S5 are not valid
    #   Buildables: $ grep -c 'Build All.*Android' androidmenu.sh         # Should do -4 off the total, as Samsung Galaxy S4/S5's Android 4/5 are not valid
    #   Kernels   : $ grep '# git clone https://github.com' androidmenu.sh | grep -vc 'github.com/offensive-security\|##########\|galaxy'   # Removing Samsung Galaxy S4/S5
    #   Kernels   : $ grep -Rh 'git clone' devices/ | grep -v 'android.googlesource.com\|#####' | sort -u | wc -l   # Extra kernel for nexus7-flo-deb
    #   Images    : https://web.archive.org/web/20150421030801/https://www.offensive-security.com/kali-linux-nethunter-download/
    ["1.2.1", 8, 15, 15, 11],

    # https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-project/-/tree/nethunter-2.0.0
    #   Devices   : $ find devices/ -type f -maxdepth 1 | wc -l
    #   Devices   : $ grep '# - ' androidmenu.sh | grep -vc 'Toolchain'   # Should do -2 off the total, as Samsung Galaxy S4/S5 are not valid
    #   Buildables: $ grep -c 'Build All.*Android' androidmenu.sh         # Should do -4 off the total, as Samsung Galaxy S4/S5's Android 4/5 are not valid
    #   Kernels   : $ grep '# git clone https://github.com' androidmenu.sh | grep -vc 'github.com/offensive-security\|##########\|galaxy'   # Removing Samsung Galaxy S4/S5
    #   Kernels   : $ grep -Rh 'git clone' devices/ | grep -v 'android.googlesource.com\|#####' | sort -u | wc -l   # Extra kernel for nexus7-flo-deb
    #   Images    : https://web.archive.org/web/20150905062656/https://www.offensive-security.com/kali-linux-nethunter-download/
    ["2.0.0", 8, 15, 15, 12],

    # https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-project/-/tree/nethunter-3.0.0
    #   Devices   : $ grep '# - ' kernels.txt | grep -vc 'Toolchain'
    #   Devices   : $ grep '^# ' AnyKernel2/devices.cfg | grep -vc ' for '
    #   Buildables: $ grep '^\[.*\]$' AnyKernel2/devices.cfg | grep -vc 'DEVELOPER'
    #   Kernels   : $ grep 'git clone' kernels.txt | grep -vc 'android.googlesource.com'
    #   Images    : https://web.archive.org/web/20160110075634/https://www.offensive-security.com/kali-linux-nethunter-download/
    ["3.0.0", 11, 12, 23, 12]
]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def bail(outstr):
    print(f"[-] {outstr}", file=sys.stderr)
    sys.exit(1)

def readfile(file):
    try:
        with open(file) as f:
            data = f.read()
            f.close()
    except:
        bail(f"Cannot open input file: {file}")
    return data

# devices.cfg had YAML in, but commented out
def yaml_parse(data, comments=False):
    result = ""
    lines = data.split('\n')
    for line in lines:
        if comments and line.startswith('##*'):
            # yaml doesn't like tabs so let's replace them with four spaces
            result += "{}\n".format(line.replace('\t', '    ')[3:])
        elif not comments and not line.startswith('#'):
            result += "{}\n".format(line)
    return yaml.safe_load(result)

def ini_parse(data):
    try:
        Config = configparser.ConfigParser(strict=False)
        Config.read_string(data)
        return Config.sections()
    except Exception as e:
        bail('Cannot parse ini input file: {} - {}'.format(file, e))

def do_yaml(yml, prefix):
    devices = 0
    buildables = 0
    images = 0
    kernels = 0
    # Iterate over all device models
    for element in yml:
        devices += 1
        # Iterate over all model's entries in yaml file
        for codename in element.keys():
            for image in element[codename].get('images', ''):
                images += 1
            for kernel in element[codename].get('kernels', ''):
                buildables += 1
                for version in kernel.get('versions', ''):
                    kernels += 1
    #print(f"{prefix}:  devices: {devices}\tbuildables: {buildables}\tkernels: {kernels}\timages: {images}\tMethod 3: YAML")
    print(f"{prefix}\t{devices}\t{buildables}\t{kernels}\t{images}\tMethod 3 (YAML)")

def do_cfg_yaml(yml_cfg, yml, ini, prefix):
    devices = 0
    #devices_yml = 0   # Alt
    buildables = len(ini)
    images = 0
    kernels = 0
    for element in yml_cfg:
        #devices_yml += 1   # Alt
        for codename in element.keys():
            for image in element[codename].get('images', ''):
                images += 1
    for element in yml:
        devices += 1
        for codename in element.keys():
            for kernel in element[codename].get('kernels', ''):
                for version in kernel.get('versions', ''):
                    kernels += 1
    # Git tags may not be 100% correct during this time frame (pull from file-based resources) vs what really was released (Just isn't done locally)
    #images_old, images_generic = do_old_kali(prefix)
    images, images_generic = do_old_kali(prefix)
    x = ""
    #if images != images_old:heyhey

    #    x += f"old: {images_old} devices, {images_generic} generic   "
    if x:
        #x = f"\t{x.rstrip()}"
        x = f" ({x.rstrip()})"
    #print(f"{prefix}:  devices: {devices}\tbuildables: {buildables}\tkernels: {kernels}\timages: {images}{x}\tMethod 2: CFG+YAML")
    print(f"{prefix}\t{devices}\t{buildables}\t{kernels}\t{images}\tMethod 2 (CFG+YAML)")

def do_cfg_txt(txt, ini, prefix):
    devices = (txt.count('\n\n# ') - txt.count('Toolchain'))
    buildables = len(ini)
    images, generic = do_old_kali(prefix)
    kernels = (txt.count('# git clone') - txt.count('# git clone https://android.googlesource.com'))
    x = ""
    #if generic:
    #    x += f"Generic: {generic} "
    if x:
        #x = f"\t{x.rstrip()}"
        x = f" ({x.rstrip()})"
    #print(f"{prefix}:  devices: {devices}\tbuildables: {buildables}\tkernels: {kernels}\timages: {images}{x}\tMethod 1: CFG+TXT")
    print(f"{prefix}\t{devices}\t{buildables}\t{kernels}\t{images}\tMethod 1 (CFG+TXT)")

def do_nethunter_static():
    for release in method0_static:
        # NetHunter version, devices, buildables, kernels, images
        prefix = release[0]
        devices = release[1]
        buildables = release[2]
        kernels = release[3]
        images = release[4]
        #print(f"{prefix} :  devices: {devices}\tbuildables: {buildables}\tkernels: {kernels}\timages: {images}\tMethod 0: Static")
        print(f"{prefix}\t{devices}\t{buildables}\t{kernels}\t{images}\tMethod 0 (Static)")

def do_old_kali(release):
    zip_cnt = 0
    generic_cnt = 0

    response = requests.get(f'https://old.kali.org/nethunter-images/kali-{release}/')
    if response.status_code == 200:
        zip_files = re.findall('href="(nethunter-.*?.zip)"', response.text)
        generic_files = re.findall('href="(nethunter-.*?-generic-.*?.zip)"', response.text)
        #print (sorted(x for x in (zip_files)))

        generic_cnt = len(generic_files)
        zip_cnt = len(zip_files) - generic_cnt
    return zip_cnt, generic_cnt

def main(argv):
    # Go to root directory of repo
    filepath = os.path.join(__file__, os.path.pardir)
    abspath = os.path.abspath(filepath)
    dirname = os.path.dirname(abspath)
    os.chdir(dirname)

    #
    # Header
    #
    #print("NetHunter Version\tDevices\tBuildables\tKernels\tImages\tMethod")
    print("Version\tDevices\tBuilds\tKernels\tImages\tMethod")

    #
    # NetHunter-*
    #
    # Method 0
    do_nethunter_static()

    #
    # Kali-*
    #

    # Files to use
    files = ["kernels.txt", "kernels.yml", "devices.cfg", "devices.yml"]

    # Get git tags
    gitrepo = git.Repo(dirname)
    gittags = sorted(gitrepo.tags, key=lambda t: t.tag.tagged_date)
    # Loop on git tags
    for tag in gittags:
        data = {}
        # Try and get files at git tag
        for file in files:
            try:
                # No "git show" support directly in gitpython, so calling git direct:
                #   REF: https://gitpython.readthedocs.io/en/stable/tutorial.html#using-git-directly
                data[file] = gitrepo.git.show("%s:%s" % (tag, file))
            except:
                pass

        # Method 3 - Kali-2024.4+
        if 'devices.yml' in data:
            yml = yaml_parse(data['devices.yml'])
            do_yaml(yml, tag)
        # Method 2 - Kali-2020.2 <= 2024.3
        elif 'devices.cfg' in data and 'kernels.yml' in data:
            ini = ini_parse(data["devices.cfg"])
            yml_cfg = yaml_parse(data["devices.cfg"], True)
            yml = yaml_parse(data["kernels.yml"])
            do_cfg_yaml(yml_cfg, yml, ini, tag)
        # Method 1 - Kali-2016.2 <= 2020.1
        elif 'devices.cfg' in data and 'kernels.txt' in data:
            ini = ini_parse(data["devices.cfg"])
            txt = data["kernels.txt"]
            do_cfg_txt(txt, ini, tag)
        else:
            bail(f"Unknown files to process for {tag}")

    #
    # Latest
    #

    # Do latest
    # Method 3
    if os.path.isfile('devices.yml'):
        data = readfile('devices.yml')
        yml = yaml_parse(data)
        do_yaml(yml, "HEAD  ")

if __name__ == "__main__":
    main(sys.argv[1:])
