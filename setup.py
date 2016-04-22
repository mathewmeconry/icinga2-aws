#!/usr/bin/env python

from setuptools import setup
from distutils.command.install import install
from bcolors import bcolors
import subprocess

class CustomInstall(install):
      def run(self):
            awscli = subprocess.Popen(["which", "aws"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = awscli.communicate()
            if not out:
                  print
                  print(bcolors.FAIL + 'Please install first aws cli' + bcolors.ENDC)
            else:
                  subprocess.call(['aws', 'configure'])
                  install.run(self)
                  print
                  print
                  print(bcolors.OKGREEN + 'Please install boto3 and python-dateutil with easy_install-3.4' + bcolors.ENDC)

setup(name='icinga2-aws',
      version='0.1',
      description='Script to dynamically create hosts in Icinga 2 based on AWS Tags',
      author='Mathias Scherer',
      author_email='scherer.mat@gmail.com',
      install_requires=["boto3", "python-dateutil", "argparse"],
      license="MIT",
      include_package_data=True,
      cmdclass={'install': CustomInstall}
     )