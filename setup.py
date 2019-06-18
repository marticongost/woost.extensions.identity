"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from setuptools import setup

setup(
    name = "woost.extensions.identity",
    version = "0.0b1",
    description = """A extension for the Woost CMS that implements the login
        flow for Google, Facebook and other third party providers.
        """,
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: ZODB",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP :: Site Management"
    ],
    install_requires = [
        "woost==3.0.*"
    ],
    packages = [
        "woost.extensions.identity"
    ],
    include_package_data = True,
    zip_safe = False
)

