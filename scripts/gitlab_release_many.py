#!/usr/bin/env python

import argparse
from gitlab_release.release_push import ReleasePoster
import os

TOKEN = os.environ['CI_TOKEN']

def main():
    parser = argparse.ArgumentParser(description="Parameters",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--proj_name")
    parser.add_argument("--release_folder", default="/data/releases/")
    parser.add_argument("--changelog", default="CHANGELOG.md")

    parser.add_argument("--gitlab_server", default='https://gitlab.com')
    args = parser.parse_args()

    ReleasePoster(TOKEN, proj_name=args.proj_name,
                  gitlab_server=args.gitlab_server).release_all_tags(args.release_folder, args.changelog)


if __name__ == '__main__':
    main()
