# Changelog

## V 0.3.0 September 15th 2020

Focus for this release is to make the whole API more user and dev friendly.

Features:
- Notification to let people know that they have to agree to the TOS of each piece of software
- Ability to specify resources as dependencies
- Resource file format; use YAML files to specify a set of resources
- Added download progress bars
- Created function to add folders to path (will be implemented in next release)

Development QOL:
- Added user docs to the repo under /docs
- ReadTheDocs Site update
- Added test suite
- Added deepsource.io for quality validation
- Added type hints to all functions/methods
- Moved from universal planning board to version specific planning boards

## V 0.2.0 January 15th 2020

The focus for this release was debian linux support, and implementing the current feature sets in debian linux as much as possible.

Features:

- Added Support for local files and not just download links
- .deb support
- .tar.gz support (just extracting no binary installation stuff)
- Installation of custom PPA based packages
- Installation of apt packages
- Porting all available resource library resources

Development QOL:

- Added nox for automation
    - Distribution building
    - Distribution releasing
    - Running tests
- Began implementing functionality and runtime compatibility tests with pytest



## V 0.1.0 January 5th 2020

Features:

- Created base resource class that can be extended to support multiple file types
- Ability to install binaries from URL or local path (currently limited to .exe and .msi)
- Ability to download static assets from the web (image files, video files etc)
- Ability to download and extract zip archives
- Initial library of predefined resources (15 in total)

