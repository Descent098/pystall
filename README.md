

<img src="./pystall-logo.png" style="zoom:30%;" />



# Pystall

A system to automate configuration and setup of fresh Operating systems.



## Quick-start

### Installation

clone this source repo using either the github button or ```git clone https://github.com/Descent098/pystall```.

Then in the root directory (the one with setup.py) run ```pip install .``` or ```sudo pip3 install .```. This will install the package and it's dependencies.

### Basic Usage

This script shows downloading the python 3 installer (a .exe) the go installer (a .msi) and a logo image (a .png).

```python
from pystall.core import EXEResource, MSIResource, StaticResource, build

python = EXEResource("python-installer", "https://www.python.org/ftp/python/3.8.1/python-3.8.1.exe")

go = MSIResource("Golang", "https://dl.google.com/go/go1.13.5.windows-amd64.msi")

logo = StaticResource("Wallpaper", ".png", "https://canadiancoding.ca/static/img/post-banners/python-post-banner.9bf19b390832.png")

build(python, go, logo)
```

## Roadmap


1. ~Class that's inherited to setup dependencies~
2. Main python module that can be installed with pip through pypi
    1. ~Can be used in a python script.~
    2. Can be used as a CLI. 
    3. Use pyinstaller to run as a direct binary.
3. A way of supporting many filetypes (images, video files, installers etc.)
    1. ~Grab the files~
    2. ~Put them in a particular path if necessary~
    3. Run installers if necessary (make sure there is a flag not to run the binary, and that arguments can be passed)
4. MacOS Support (needs to be validated)
5. A CLI interface
    1. Pass files with a JSON schema for installing dependencies.
6. Configuration of installations
    1. Handling PATH variables
    2. Handle running installers as admin.
7. Asynchronously download files. (technically already possible with popen but a better solution can be found)


### Unknowns

Anything you don't know implementation details of yet.



1. Not sure how to implement .dmg installation.
2. Don't know how to support unconventional installations. (Maybe out of scope)
3. don't necessarily know how to support varying linux installations. Particularly how to check what linux is installed. 





### Assumptions & Dependencies

**Assumptions**

- Python 3+ is installed
- Pip for python 3 is installed



**Dependencies**

- requests
- subprocess
- os
- sys
- docopt
- tqdm
- colored

