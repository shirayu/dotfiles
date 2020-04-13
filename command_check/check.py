#!/usr/bin/env python3

import argparse
import codecs
import json
import os
import platform
import shutil
import subprocess
import sys
import typing


def brew_checks(targets: typing.List[str]) -> typing.Iterable[str]:
    res = subprocess.run(["brew", "list"], stdout=subprocess.PIPE)
    installed: typing.Set[str] = set()
    for item in res.stdout.decode('utf8').split():
        installed.add(item.split('@')[0])

    for t in targets:
        if t not in installed:
            yield t


def npm_checks(targets: typing.List[str]) -> typing.Iterable[str]:
    cmds = 'npm -g list --depth=0 --json=true'.split()
    res = subprocess.run(cmds, stdout=subprocess.PIPE)
    installed: typing.Set[str] = set(json.loads(
        res.stdout.decode('utf8'))['dependencies'].keys())

    for t in targets:
        if t not in installed:
            yield t


def checks(targets: typing.List[str]) -> typing.Iterable[str]:
    for t in targets:
        if not shutil.which(t):
            yield t


def get_list(path_in: str) -> typing.List[str]:
    with codecs.open(path_in, "r", "utf8") as inf:
        targets = [line.strip()for line in inf]
    return targets


def operation(path_indir: str) -> bool:
    def check() -> typing.Iterator[str]:
        pf = platform.system()
        if pf == 'Darwin':
            if shutil.which('brew'):
                for t in brew_checks(
                        get_list(os.path.join(path_indir, 'brew.txt'))):
                    yield t
            else:
                yield 'brew'
        elif pf == 'Linux':
            for t in checks(get_list(os.path.join(path_indir, 'linux.txt'))):
                yield t
        elif pf == 'Windows':
            for t in checks(get_list(os.path.join(path_indir, 'windows.txt'))):
                yield t
        for t in checks(get_list(os.path.join(path_indir, 'all.txt'))):
            yield t

        if shutil.which('npm'):
            for t in npm_checks(get_list(os.path.join(path_indir, 'npm.txt'))):
                yield f'@npm\t{t}'

        # TODO pip

    found = False
    for t in check():
        print(t)
        found = True
    return found


def get_opts() -> argparse.Namespace:
    script_dir: str = os.path.dirname(os.path.abspath(__file__))
    oparser = argparse.ArgumentParser()
    oparser.add_argument("--input", "-i", default=script_dir)
    return oparser.parse_args()


def main() -> None:
    opts = get_opts()
    found = operation(opts.input)
    if found:
        sys.exit(1)


if __name__ == '__main__':
    main()
