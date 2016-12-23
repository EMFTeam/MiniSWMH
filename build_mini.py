#!/usr/bin/python3

import os
import sys
import datetime
import subprocess

from localpaths import rootpath


version = 'v1.2.8-BETA'
cut_titles = ['e_rajastan', 'e_mali', 'k_sahara', 'k_fezzan', 'k_kanem', 'k_hausaland']
scons_bin_path = '/usr/bin/scons'

mini_path = rootpath / 'MiniSWMH/MiniSWMH'
mapcut_path = rootpath / 'ck2utils/mapcut'


def build_mapcut():
    print(">> attempting to build mapcut from source...")
    os.chdir(str(mapcut_path))
    try:
        sys.stdout.write(subprocess.check_output(scons_bin_path, universal_newlines=True, stderr=subprocess.STDOUT))
    except subprocess.CalledProcessError as e:
        sys.stderr.write('> scons failed!\n> command: {}\n> exit code: {}\n\n{}'.format(e.cmd, e.returncode, e.output))
        sys.exit(1)


def main():
    mapcut_bin = 'mapcut' if sys.platform.startswith('linux') else 'mapcut.exe'
    mapcut_bin_path = mapcut_path / mapcut_bin

    if not mapcut_bin_path.exists():
        build_mapcut()
    if not mapcut_bin_path.exists():
        sys.stderr.write('mapcut binary not found: {}\n'.format(mapcut_bin_path))
        return 2

    print(">> executing mapcut...")

    try:
        sys.stdout.write(subprocess.check_output([str(mapcut_bin_path)] + cut_titles,
                                                 universal_newlines=True, stderr=subprocess.STDOUT))
    except subprocess.CalledProcessError as e:
        sys.stderr.write('> mapcut failed!\n> command: {}\n> exit code: {}\n\n{}'.format(e.cmd, e.returncode, e.output))
        return 3

    with (mini_path / 'version.txt').open('w') as f:
        print('{} - {}'.format(version, datetime.date.today()), file=f)

    return 0


if __name__ == '__main__':
    sys.exit(main())
