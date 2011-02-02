import os
import glob

from distutils.core import setup

from mcc2 import get_version

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk('mcc2'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        prefix = dirpath[13:] # Strip "mcc2/" or "mcc2\"
        for f in filenames:
            data_files.append(os.path.join(prefix, f))

setup(name='mandriva-control-center2',
    version=get_version().replace(' ', '-'),
    description='Mandriva Control Center 2',
    author='Wiliam Souza',
    author_email='wiliam@mandriva.com',
    url='',
    download_url='',
    package_dir={'mcc2': 'mcc2'},
    packages=packages,
    package_data={'mcc2': data_files},
    data_files=[
        ('/usr/share/mcc2/bin/', glob.glob("bin/*-mechanism.py")),
        ('/usr/share/dbus-1/system-services/', glob.glob("dbus/*.service")),
        ('/etc/dbus-1/system.d/', glob.glob("dbus/*.conf")),
        ('/usr/share/polkit-1/actions/', glob.glob("policykit/*.policy"))],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: ',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Libraries :: Python Modules',]
    )