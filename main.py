import fnmatch
import sys

import cdtb
from cdtb.hashes import (
    default_hashfile,
    default_hash_dir,
    update_default_hashfile,
)
from cdtb.wad import Wad


def download_hashes():
    default_hash_dir.mkdir(parents=True, exist_ok=True)
    hash_files = [
        'hashes.binentries.txt',
        'hashes.binfields.txt',
        'hashes.binhashes.txt',
        'hashes.bintypes.txt',
        'hashes.game.txt',
        'hashes.lcu.txt',
        'hashes.rst.txt',
    ]
    for basename in hash_files:
        update_default_hashfile(basename)


def unpack_file(file_path, output_path, pattern):
    hashfile = default_hashfile(file_path)

    wad = Wad(file_path, hashes=hashfile.load())

    wad.files = [wf for wf in wad.files if any(wf.path is not None and fnmatch.fnmatchcase(wf.path, pattern) for p in pattern)]

    for wf in wad.files:
        print(wf.path)

    wad.guess_extensions()
    wad.extract(output_path, overwrite=True)


if __name__ == "__main__":
    if sys.argv[1] == "download_hashes":
        download_hashes()
    elif sys.argv[1] == "unpack_file":
        if len(sys.argv) < 5:
            print("Usage: unpack_file <file_path> <output_path>")
            sys.exit(1)
        unpack_file(sys.argv[2], sys.argv[3], sys.argv[4])
