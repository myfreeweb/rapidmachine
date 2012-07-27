#!/usr/bin/env python
import sys
from distutils.core import setup
from rapidmachine import __version__

if sys.version < "2.5":
    sys.exit("Python 2.5 or higher is required")

setup(name="rapidmachine",
      version=__version__,
      description="A high-level web toolkit for Rapid API Development",
#      long_description="""""",
      license="Apache License 2.0",
      author="myfreeweb",
      author_email="floatboth@me.com",
      url="https://github.com/myfreeweb/rapidmachine",
      requires=["werkzeug", "urlobject", "dictshield"],
      packages=["rapidmachine"],
      keywords=["web", "rest", "http"],
      classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries",
      ],
      package_data={},
)
