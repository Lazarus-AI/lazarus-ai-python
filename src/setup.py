from setuptools import setup, find_packages
setup(
  name = 'lazarus-ai',
  packages = ['lazarus_ai', 'errors', 'utils'],
  version = '1.0.0',
  license='MIT',
  description = 'Lazarus AI Python Library',
  author = 'Caroline Abel, KK Barrows, Alvin Xie',
  author_email = 'caroline@lazarus.enterprises, kathleen@lazarus.enterprises, alvin@lazarus.enterprises',
  url = 'https://www.lazarusforms.com/',
  download_url = 'https://github.com/Lazarus-AI/lazarus-ai-python/archive/refs/tags/v1.0.0.tar.gz',
  install_requires=[
          'requests',
          'stringcase',
  ],
  project_urls={
    "Bug Tracker": "https://github.com/Lazarus-AI/lazarus-ai-python/issues",
    "Documentation": "https://lazarus.stoplight.io/docs/lazarus-forms/welcome",
    "Source Code": "https://github.com/Lazarus-AI/lazarus-ai-python",
  },
  classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
  ],
)
