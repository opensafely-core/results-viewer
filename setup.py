import os

from setuptools import find_namespace_packages, setup

with open(os.path.join("osview", "VERSION")) as f:
    version = f.read().strip()

setup(
    name="opensafely-viewer",
    version=version,
    packages=find_namespace_packages(exclude=["tests"]),
    include_package_data=True,
    url="https://github.com/opensafely-core/opensafely-viewer",
    description="Command line tool for running OpenSAFELY studies locally.",
    license="GPLv3",
    author="OpenSAFELY",
    author_email="tech@opensafely.org",
    python_requires=">=3.8",
    install_requires=[
        "jinja2>=3.0",
    ],
    entry_points={"console_scripts": ["osview=osview:main"]},
    classifiers=["License :: OSI Approved :: GNU General Public License v3 (GPLv3)"],
)
