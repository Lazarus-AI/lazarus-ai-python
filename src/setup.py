from setuptools import setup, find_packages
setup(
  name = 'lazarus-ai',
  packages = ['lazarus_ai', 'errors', 'utils'],
  version = '0.11',
  license='MIT',
  description = 'Lazarus AI Python Library',
  author = 'Caroline Abel, KK Barrows, Alvin Xie',
  author_email = 'caroline@lazarus.enterprises, kathleen@lazarus.enterprises, alvin@lazarus.enterprises',
  url = 'https://www.lazarusforms.com/',
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # TODO
  install_requires=[
          'requests',
          'stringcase',
      ],
  classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
  ],
)
