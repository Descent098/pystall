![pystall logo](https://raw.githubusercontent.com/Descent098/pystall/master/pystall-logo.png)



A system to automate configuration and setup of fresh Operating systems.



## Quick-start

### Installation



#### From PyPi

You can install the project from PyPi using ```pip install pystall``` or ```pip3 install pystall```



#### From Source

clone this source repo using either the github button or ```git clone https://github.com/Descent098/pystall```.

Then in the root directory (the one with setup.py) run ```pip install .``` or ```sudo pip3 install .```. This will install the package and it's dependencies.



### Basic Usage

#### Custom defined resources

This script shows downloading the python 3 installer (a .exe) the go installer (a .msi) and a logo image (a .png).

```python
from pystall.core import EXEResource, MSIResource, StaticResource, build

python = EXEResource("python-installer", "https://www.python.org/ftp/python/3.8.1/python-3.8.1.exe")

go = MSIResource("Golang", "https://dl.google.com/go/go1.13.5.windows-amd64.msi")

logo = StaticResource("Wallpaper", ".png", "https://canadiancoding.ca/static/img/post-banners/python-post-banner.9bf19b390832.png")

build(python, go, logo)
```



#### Built-in resource library

There is also the option to use the built-in library of resources that have been setup.

```python
from pystall.core import build
from pystall.library import python, go, micro

build(python, go, micro)
```



#### Logging

If you want logs while the script runs you can use the show_logs() function in the core library

```python
from pystall.core import build, show_logs
from pystall.library import python, go, chrome, micro

show_logs()

build(python, go, chrome, micro)
```



#### Additional Docs

For a full list of available library resources & how to extend the framework for specific functionality check the wiki: https://github.com/Descent098/pystall/wiki



## Roadmap


1. ~Class that's inherited to setup dependencies~
2. Main python module that can be installed with pip through pypi
    1. ~Can be used in a python script.~
    2. Can be used as a CLI. 
    3. ~Use pyinstaller to run as a direct binary.~
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



For more detailed roadmap check out the project planning board on github: https://github.com/Descent098/pystall/projects/1

### Unknowns

Anything you don't know implementation details of yet.

1. Not sure how to implement .dmg installation.
2. Don't know how to support unconventional installations. (Maybe out of scope)
3. don't necessarily know how to support varying linux installations. Particularly how to check what linux is installed.


If you are interested I livestreamed the development of pystall and there is also a playlist of the development: https://www.youtube.com/watch?v=l3hBPfEtbko&list=PLY1W45yrIxjTF-5EqKSfZ1jKeb1YZo5ve
