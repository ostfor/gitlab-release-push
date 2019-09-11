#!/usr/bin/python -u
import argparse, os

from gitlab_release.release_push import ReleasePoster


def main():
    parser = argparse.ArgumentParser(description="Parameters",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("token")
    parser.add_argument("--tagname")
    parser.add_argument("--proj_name")
    parser.add_argument("--release_package", default="/data/releases/")
    parser.add_argument("--changelog", default="CHANGELOG.md")
    parser.add_argument("--gitlab_server", default='https://gitlab.com')

    args = parser.parse_args()
    fname = os.path.basename(args.release_package)
    dirname = os.path.dirname(args.release_package)
    ReleasePoster(args.token, proj_name=args.proj_name,
                  gitlab_server=args.gitlab_server).release(dirname, fname, args.tagname, args.changelog)


if __name__ == '__main__':
    main()
