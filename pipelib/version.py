__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

__version__ = "0.0.0"
AUTHOR = "Vanessa Sochat"
EMAIL = "vsoch@users.noreply.github.com"
NAME = "pipelib"
PACKAGE_URL = "https://github.com/vsoch/pipelib"
KEYWORDS = "library for collating (filtering, comparing, ordering) things"
DESCRIPTION = "A command line client and functions for collation."
LICENSE = "LICENSE"

################################################################################
# Global requirements

INSTALL_REQUIRES = ()

TESTS_REQUIRES = (("pytest", {"min_version": "4.6.2"}),)

################################################################################
# Submodule Requirements

INSTALL_REQUIRES_ALL = INSTALL_REQUIRES + TESTS_REQUIRES
