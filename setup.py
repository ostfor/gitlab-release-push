from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='osf_visualizer',
      use_scm_version=True,
      setup_requires=['setuptools_scm'],
      install_requires=required,
      description='Gitlab release',
      url='http://github.com/ostfor/gitlab_release',
      author='Denis Brailovsky',
      author_email='denis.brailovsky@gmail.com',
      license='MIT',

      packages=["gitlab_release.{}".format(pkg) for pkg in find_packages("gitlab_release")] + ["gitlab_release"],

      zip_safe=False)
