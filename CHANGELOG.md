# Changelog

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

