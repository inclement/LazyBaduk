from setuptools import setup, find_packages
from distutils.extension import Extension
from Cython.Distutils import build_ext

from os.path import join, dirname

packages = find_packages()

options = {'apk': {#'window': None,
    'requirements': 'sdl2,kivy,python3,pexpect,ptyprocess',
    'blacklist-requirements': 'openssl,sqlite3',
    'android-api': 27,
    'ndk-api': 23,
    'ndk-dir': '/home/sandy/android/android-ndk-r17c',
    'dist-name': 'lazybaduk',
    'ndk-version': '17c',
    'package': 'net.inclem.lazybaduk',
    'permission': 'VIBRATE',
    'arch': 'armeabi-v7a',
    'wakelock': None,
    'icon': 'build_media/icon.png',
    'presplash': 'build_media/splash.png',
    }}
setup(
    name='Lazy Baduk',
    version='0.7',
    description='A Leela Zero analysis tool',
    author='Alexander Taylor',
    author_email='alexander@inclem.net',
    packages=packages,
    options=options,
    # package_data={'nogo2': ['*.py', '*.kv', '*.so', '13_205.txt.gz'],
    # package_data={'nogo2': ['*.py', '*.kv', '*.so', 'd351f06e446ba10697bfd2977b4be52c3de148032865eaaf9efc9796aea95a0c.gz'],
    # package_data={'nogo2': ['*.py', '*.kv', '*.so', 'elfv2.gz'],
    package_data={'nogo2': ['*.py', '*.kv', '*.so', '0a963117.gz'],
    # package_data={'nogo2': ['*.py', '*.kv', '*.so', '33986b7f9456660c0877b1fc9b310fc2d4e9ba6aa9cee5e5d242bd7b2fb1b166.gz'],
    # package_data={'nogo2': ['*.py', '*.kv', '*.so', '85a936847e2759ab5ea0389bbe061245dc6025ef9d317a0d1315cc1078b0c34a.gz'],
    # package_data={'nogo2': ['*.py', '*.kv', '*.so', 'network.gz'],
    # package_data={'nogo2': ['*.py', '*.kv', '*.so', 'network.gz'],
    # package_data={'nogo2': ['*.py', '*.kv', '*.so'],
                  'nogo2/media': ['*.png', '*.atlas'],
                  # 'nogo2/media/boards': ['*.png', '*.atlas'],
                  'nogo2/media/stones': ['*.png', '*.atlas'],
                  'nogo2/media/homeatlas': ['*.png', '*.atlas'],
                  'nogo2/media/mainimages': ['*.png', '*.atlas'],
                  'nogo2/ext/gomill': ['*.py', '*.rst'],
                  'nogo2/gui': ['*.py', '*.kv'],
                  'nogo2/abstract': ['*.py'],
                  'nogo2/assets': ['fontello.ttf'],
                  # 'nogo2/leelaz': ['*.py', 'leelaz_binary_android_9x9'],
                  # 'nogo2/leelaz': ['*.py', 'leelaz_binary_android_13x13'],
                  'nogo2/leelaz': ['*.py', 'leelaz_binary_android'],
                  # 'nogo2/leelaz9x9': ['*.py', '9x9-20-128.txt.gz'],
    }
)
