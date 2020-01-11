# Changelog

## V 0.2.0 TBD

The focus for this release was Linux support, and implementing the current feature sets in Linux as much as possible.



Features:

- .deb support
- .tar.gz support (just extracting no binary installation stuff)
- Installation of custom PPA based packages
- Shell script installers (add to path coming later)
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

