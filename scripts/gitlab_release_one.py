#!/usr/bin/env python

import argparse
import os
from gitlab_release.release_push import ReleasePoster, get_notes

TOKEN = os.environ['CI_TOKEN']


def main():
    parser = argparse.ArgumentParser(description="Parameters",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--tagname")
    parser.add_argument("--proj_name")
    parser.add_argument("--release_package", nargs="+")
    parser.add_argument("--changelog", default="CHANGELOG.md")
    parser.add_argument("--gitlab_server", default='https://gitlab.com')
    parser.add_argument("--allow_empty_change_log", action="store_true")
    args = parser.parse_args()

    notes = "Release " + args.tagname
    try:
        notes = get_notes(args.tagname, args.changelog)
    except RuntimeWarning:
        if not args.allow_empty_change_log:
            raise

    ReleasePoster(TOKEN, proj_name=args.proj_name,
                  gitlab_server=args.gitlab_server).release(release_package_fname_list=args.release_package,
                                                            tag_name=args.tagname, text=notes)


if __name__ == '__main__':
    main()
