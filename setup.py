# -*- coding: UTF−8 -*-

import os

from setuptools import setup, find_packages

from play_helpers.ph_constants_config import PhConfigConst

# all packages dependencies
packages = find_packages()
if not packages:
    print(f'Selecting Hardcoded Packages')
    packages = [
        PhConfigConst.TOOL_PACKAGE_NAME,
    ]
print(f'Packages are {packages}')

# run-time dependencies
install_reqs = [
    'packaging',
    'pandas',
    'psutil',
    'tzlocal',
    'click',
    'twisted',
    'incremental',
    'requests',
    'pycryptodome',
    'ruamel.yaml',
    'sphinx',
    'sphinx_rtd_theme',
]

# build-time dependencies
setup_reqs = [
    'click',
    'twisted',
    'incremental',
]

# get long description from the README.md
with open(os.path.join(os.path.dirname(__file__), "README.md"), "r", encoding="utf-8") as fd:
    long_description = fd.read()

setup(
    use_incremental=True,
    setup_requires=setup_reqs,
    name=PhConfigConst.TOOL_NAME,
    author="Pratik Jaiswal",
    author_email="impratikjaiswal@gmail.com",
    description=PhConfigConst.TOOL_DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=PhConfigConst.TOOL_URL,
    project_urls={
        "Bug Tracker": PhConfigConst.TOOL_URL_BUG_TRACKER,
    },
    keywords=PhConfigConst.TOOL_META_KEYWORDS,
    license="GNU GENERAL PUBLIC LICENSE v3.0",
    python_requires=">=3.9",
    packages=packages,
    install_requires=install_reqs,
    # test_suite="test.play_helpers",
)
