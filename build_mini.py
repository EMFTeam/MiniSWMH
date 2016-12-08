#!/usr/bin/env python3

import sys
import datetime
import subprocess

from localpaths import rootpath


version = 'v1.2.8-BETA'

cut_titles = ['e_rajastan', 'e_mali', 'k_sahara', 'k_fezzan', 'k_kanem', 'k_hausaland']

mini_path = rootpath / 'MiniSWMH/MiniSWMH'
mapcut_path = rootpath / 'ck2utils/mapcut'


def main():
    mapcut_bin = 'mapcut' if sys.platform.startswith('linux') else 'mapcut.exe'
    mapcut_bin_path = mapcut_path / mapcut_bin

    if not mapcut_bin_path.exists():
        sys.stderr.write('mapcut binary not found: {}\n'.format(mapcut_bin_path))
        return 1

    try:
        sys.stdout.write(subprocess.check_output([str(mapcut_bin_path)] + cut_titles,
                                                 universal_newlines=True, stderr=subprocess.STDOUT))
    except subprocess.CalledProcessError as e:
        sys.stderr.write('mapcut failed!\ncommand: {}\nexit code: {}\n\n{}'.format(e.cmd, e.returncode, e.output))
        return 2

    with (mini_path / 'version.txt').open('w') as f:
        print('{} - {}'.format(version, datetime.date.today()), file=f)

    return 0


if __name__ == '__main__':
    sys.exit(main())
