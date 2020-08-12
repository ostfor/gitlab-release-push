import gitlab, os


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
                release_package_fname = find_package_from_old_releases(release_folder, tag.name)
            except RuntimeWarning as e:
                print(e)
                continue
            try:
                notes = get_notes(tag.name, chlog)
            except RuntimeWarning as e:
                print(e)
                notes = "Release #{}".format(tag.name)
            self.release(os.path.join(release_folder, release_package_fname), tag.name, notes)

    def release(self, release_package_fname_list, release_jsons_fname_list, tag_name, text):

        def parse_release_package_fname_list(release_package_fname_list, release_json_fname_list):
            asset_links = []
            release_text = "\n\n"

            release_text = release_text + "### Packages"
            for package_fname in release_package_fname_list:
                release_package_fname = os.path.basename(package_fname)
                release_folder = os.path.dirname(package_fname)
                
                f = self.proj.upload(release_package_fname,
                                     filepath=os.path.join(release_folder, release_package_fname))

                release_url = "/".join([self.gl_server, self.proj_name, f['url']])
                asset = {"name": release_package_fname, "url": release_url}
                asset_links.append(asset)
                release_text = release_text + "\n\n[Download package {}]({})".format(release_package_fname, release_url)

            release_text = release_text + "\n\n\n ### JSON schema"
            for json_fname in release_json_fname_list:
                release_json_fname = os.path.basename(json_fname)
                release_folder = os.path.dirname(json_fname)

                f = self.proj.upload(release_json_fname,
                                     filepath=os.path.join(release_folder, release_json_fname))

                release_url = "/".join([self.gl_server, self.proj_name, f['url']])
                asset = {"name": release_json_fname, "url": release_url}
                asset_links.append(asset)
                release_text = release_text + "\n\n[Download schema {}]({})".format(release_json_fname, release_url)

            return asset_links, release_text

        print("Server: ", self.gl_server)
        asset_links, release_text = parse_release_package_fname_list(release_package_fname_list, release_json_fname_list)

        request = {
            'name': 'Release ' + tag_name, 'tag_name': tag_name,
            'description': text + release_text,
            "assets": {"links": asset_links}
        }
        print(request)
        try:
            _release = self.proj.releases.create(request)
        except gitlab.exceptions.GitlabCreateError:
            self.proj.releases.delete(tag_name)
            _release = self.proj.releases.create(request)
        return _release
