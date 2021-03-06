from setuptools.command.sdist import sdist
from setuptools import setup, find_packages
import cPickle
import os
import shutil
import sys

if __name__ == '__main__':
    if sys.platform != 'win32':
        os.environ['CC'] = 'gcc'
        os.environ['CXX'] = 'g++'

    bt_required_packages = []
    if os.path.isfile('bt_required_packages'):
        bt_required_packages = open('bt_required_packages.req').read().splitlines()
    third_party_required_packages = open('third_party_required_packages.req').read().splitlines()
    require_packages = third_party_required_packages + bt_required_packages


class CustomSdist(sdist):
    def run(self):
        self.CopyChronosSourceFiles()
        sdist.run(self)

    @staticmethod
    def CopyChronosSourceFiles():
        chronosSourcePath = os.path.join('Contracts', 'Chronos')
        chronosDestinationPath = os.path.join('Chronos', 'ChronosScripts')
        if not os.path.isdir(chronosDestinationPath):
            os.mkdir(chronosDestinationPath)
        buildList = []
        for aggregate in [path for path in os.listdir(chronosSourcePath) if path.endswith('.py')]:
            buildList.append(aggregate[:-3])
            proto = aggregate[:-2] + 'proto'
            shutil.copyfile(os.path.join(chronosSourcePath, aggregate), os.path.join(chronosDestinationPath, aggregate))
            shutil.copyfile(os.path.join(chronosSourcePath, proto), os.path.join(chronosDestinationPath, proto))
        with open(os.path.join('Chronos', 'buildList.txt'), 'w') as buildListFile:
            cPickle.dump(buildList, buildListFile)
        chronosProtoPath = os.path.join('Chronos', '')
        if os.path.isfile('Chronos/Chronos.proto'):
            os.system("protoc -I={} --python_out={} Chronos/Chronos.proto".format(chronosProtoPath, chronosProtoPath))



setup(name='Chronos',
      version='1.0.0',
      author='Belvedere',
      author_email='Team_Brown_Tech@belvederetrading.com',
      cmdclass={'sdist': CustomSdist},
      packages=find_packages(),
      package_data={'Chronos': ['ChronosScripts/*', 'initd/*', 'bin/*', 'files/*', 'buildList.txt', 'Chronos.proto']},
      url='http://pypi:28080/simple/Chronos/',
      description='A distributed event sourcing framework',
      long_description=open('README.rst').read(),
      scripts=['Chronos/bin/chronos_deploy', 'Chronos/bin/chronoses'],
      install_requires=require_packages,
      tests_require=['mock'])
