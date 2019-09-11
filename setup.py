from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='gitlab_release',
      use_scm_version=True,
      setup_requires=['setuptools_scm'],
      install_requires=required,
      description='Gitlab release',
      url='http://github.com/ostfor/gitlab_release',
      author='Denis Brailovsky',
      author_email='denis.brailovsky@gmail.com',
      license='MIT',
      install_requires=["python-gitlab>=1.11.0"],
      packages=["gitlab_release.{}".format(pkg) for pkg in find_packages("gitlab_release")] + ["gitlab_release"],
      scripts = ["scripts/gitlab_release_one.py", "scripts/gitlab_release_many.py"],
      zip_safe=False)
