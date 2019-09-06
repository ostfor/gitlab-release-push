import argparse

import gitlab
import os


def get_notes(tag, chlog):
    delim = "## ["
    with open(chlog, 'r') as f:
        chlog = f.read().split(delim)
    vers = [a for a in chlog if tag + "]" in a]
    if len(vers) == 0:
        raise RuntimeWarning("Warning: None changlog")
    if len(vers) > 1:
        print(vers)
        raise RuntimeError("Error: Found two versions in chlog canditates nothing will be posted")

    text = "\n".join([v for v in vers[0].split('\n')][1:]).strip()
    return text


def find_package_from_old_releases(folder, tag):
    file_names = os.listdir(folder)
    fnames = [fname_ for fname_ in file_names if "-" + tag + "-" in fname_ or "_" + tag + "-" in fname_]
    if len(fnames) == 0:
        raise RuntimeWarning("No candidates")
    if len(fnames) == 1:
        return fnames[0]
    else:
        print(fnames)
        fnames = [nm for nm in fnames if "toy" not in nm]
        if len(fnames) != 1:
            raise RuntimeWarning("Error: Found two release canditates nothing will be posted")

        return fnames[0]


class ReleasePoster(object):
    """docstring for ReleasePoster"""

    def __init__(self, private_token, proj_name, gitlab_server):
        self.proj_name = proj_name
        self.gl_server = gitlab_server
        self.gl = gitlab.Gitlab(gitlab_server, private_token=private_token)
        self.proj = self.gl.projects.get(proj_name)
        self.tags = self.proj.tags.list(all=True)
        self.tags = self.tags[::-1]
        print(self.tags)
        print("SERV: ", self.gl_server)

    def release_all_tags(self, release_folder, chlog):
        for tag in self.tags:
            try:
                fname = find_package_from_old_releases(release_folder, tag.name)
            except RuntimeWarning as e:
                print(e)
                continue
            try:
                notes = get_notes(tag.name, chlog)
            except RuntimeWarning as e:
                print(e)
                notes = "Release #{}".format(tag.name)
            self.release(fname, tag.name, notes, release_folder)

    def release(self, fname, tag_name, text, release_folder):
        print("SERV: ", self.gl_server)
        f = self.proj.upload(fname, filepath=os.path.join(release_folder, fname))
        release_url = "/".join([self.gl_server, self.proj_name, f['url']])
        print(release_url)
        request = {
            'name': 'Release ' + tag_name, 'tag_name': tag_name,
            'description': text + "\n[Download]({})".format(release_url),
            "assets": {"links": [
                {"name": fname, "url": release_url}]
            }
        }
        print(request)
        try:
            _release = self.proj.releases.create(request)
        except gitlab.exceptions.GitlabCreateError:
            self.proj.releases.delete(tag_name)
            _release = self.proj.releases.create(request)
        return _release


def main():
    parser = argparse.ArgumentParser(description="Parameters",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("token")
    parser.add_argument("--proj_name")
    parser.add_argument("--release_folder", default="/data/releases/")
    parser.add_argument("--changelog", default="CHANGELOG.md")

    args = parser.parse_args()

    ReleasePoster(args.token, proj_name=args.proj_name,
                  gitlab_server='https://gitlab.com').release_all_tags(args.release_folder,
                                                                       args.changelog)


if __name__ == '__main__':
    main()
