#!/usr/bin/python -u
import argparse, os

from gitlab_release.release_push import ReleasePoster, get_notes

import os
TOKEN = os.environ['CI_TOKEN']

def main():
    parser = argparse.ArgumentParser(description="Parameters",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    #parser.add_argument("token")
    parser.add_argument("--tagname")
    parser.add_argument("--proj_name")
    parser.add_argument("--release_package", default="/data/releases/")
    parser.add_argument("--changelog", default="CHANGELOG.md")
    parser.add_argument("--gitlab_server", default='https://gitlab.com')
    parser.add_argument("--allow_empty_change_log", action="store_true")


    args = parser.parse_args()
    fname = os.path.basename(args.release_package)
    dirname = os.path.dirname(args.release_package)

    notes = "Release " + args.tagname
    try:
        notes = get_notes(args.tagname, args.changelog)
    except RuntimeWarning:
        if not args.allow_empty_change_log:
            raise

    ReleasePoster(TOKEN, proj_name=args.proj_name,
                  gitlab_server=args.gitlab_server).release(dirname, fname, args.tagname, notes)


if __name__ == '__main__':
    main()
