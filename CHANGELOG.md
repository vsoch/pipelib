# CHANGELOG

This is a manually generated log to track changes to the repository for each release.
Each section should include general headers such as **Implemented enhancements**
and **Merged pull requests**. Critical items to know are:

 - renamed commands
 - deprecated / removed commands
 - changed defaults
 - backward incompatible changes (recipe file format? image file format?)
 - migration guidance (how to convert images?)
 - changed behaviour (recipe sections work differently)

The versions coincide with releases on pip. Only major versions will be released as tags on Github.

## [0.0.x](https://github.com/vsoch/pipelib/tree/main) (0.0.x)
 - bug that VersionWrapper wasn't hashable (0.0.17)
 - support for new variant of packaging (0.0.16)
 - skip empty version strings in container tags (0.0.15)
 - support for major tag sort (0.0.14)
 - bug that re-using pipeline will remove steps (0.0.13)
 - shared operator for AND / OR (0.0.12)
 - removing deprecated distutils.LooseVersion (0.0.11)
 - adding composition (0.0.1)
 - skeleton release (0.0.0)
