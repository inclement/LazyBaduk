from setuptools import setup, find_packages
from distutils.extension import Extension
from Cython.Distutils import build_ext

from os.path import join, dirname

packages = find_packages()

options = {'apk': {'window': None,
                   'requirements': 'sdl2,kivy,python3,pexpect,ptyprocess',
                   'android-api': 27,
                   'ndk-api': 23,
                   'ndk-dir': '/home/sandy/android/android-ndk-r17c',
                   'dist-name': 'lzviewer',
                   'ndk-version': '17c',
                   'package': 'net.inclem.lzviewer',
                   'permission': 'VIBRATE',
                   'arch': 'armeabi-v7a',
                   'wakelock': None,
                   'icon': 'build_media/icon.png',
                   }}
setup(
    name='Lazy Baduk',
    version='0.2',
    description='An SGF editor and Leela Zero analysis tool',
    author='Alexander Taylor',
    author_email='alexander@inclem.net',
    packages=packages,
    options=options,
    package_data={'nogo2': ['*.py', '*.kv', 'leelaz_binary_android', '*.so', 'network.gz'],
                  'nogo2/media': ['*.png', '*.atlas'],
                  'nogo2/media/boards': ['*.png', '*.atlas'],
                  'nogo2/media/stones': ['*.png', '*.atlas'],
                  'nogo2/media/homeatlas': ['*.png', '*.atlas'],
                  'nogo2/media/mainimages': ['*.png', '*.atlas'],
                  'nogo2/ext/gomill': ['*.py', '*.rst'],
                  'nogo2/gui': ['*.py', '*.kv'],
                  'nogo2/abstract': ['*.py'],
                  'nogo2/leelaz': ['*.py']}
)
