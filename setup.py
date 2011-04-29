import os
import glob

from distutils.core import setup

from mcc2 import get_version

packages, other_files = [], [],
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk('mcc2/'):
    data_fullpath = []
    data_dirpath = []
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        for f in filenames:
            full = os.path.join(dirpath, f)
            data_dirpath.append(os.path.split(full)[0])
            data_fullpath.append(full)
    other_files.extend(zip(data_dirpath, [data_fullpath]))

data_files = [
    ('/usr/bin/', glob.glob('bin/mcc2*')),
    ('/usr/share/mandriva/bin/', glob.glob('bin/*-mechanism.py')),
    ('/usr/share/dbus-1/system-services/', glob.glob('dbus/*.service')),
    ('/etc/dbus-1/system.d/', glob.glob('dbus/*.conf')),
    ('/usr/share/polkit-1/actions/', glob.glob('policykit/*.policy')),
    ('/usr/share/mandriva/config', glob.glob('config/*.cfg')),
    ('/usr/share/applications/kde4/', glob.glob('kcm/mcc2-*.desktop')),
    ('/usr/share/kde4/services/', glob.glob('kcm/settings-*.desktop')),
    ('/usr/share/apps/mandriva-control-center/', glob.glob('kcm/*.py')),]

data_files.extend(other_files)

setup(name='mandriva-control-center',
    version=get_version().replace(' ', '-'),
    description='Mandriva Control Center',
    author='Wiliam Souza',
    author_email='wiliam@mandriva.com',
    url='',
    download_url='',
    package_dir={'mcc2': 'mcc2'},
    packages=packages,
    data_files=data_files,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: GPL',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Libraries :: Python Modules',]
    )
