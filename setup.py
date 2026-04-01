import re

from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

with open('./twitscraper/__init__.py') as f:
    version = re.findall(r"__version__ = '(.+)'", f.read())[0]

setup(
    name='twitscraper',
    version=version,
    packages=find_packages(exclude=['tests*', 'examples*']),
    install_requires=[
        'httpx[socks]',
        'filetype',
        'beautifulsoup4',
        'pyotp',
        'lxml',
        'webvtt-py',
        'm3u8',
        'Js2Py-3.13',
        'curl_cffi',
    ],
    python_requires='>=3.10',
    description='Twitter/X API wrapper with no API key required.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    package_data={'twitscraper': ['py.typed']},
)
