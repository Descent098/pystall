# Quick Start

Here is everything you need to get started with using pystall.

## Installation

### From PyPi

You can install the project from PyPi using ```pip install pystall``` or ```pip3 install pystall```



### From Source

clone this source repo using either the github button or ```git clone https://github.com/Descent098/pystall```.



Then in the root directory (the one with setup.py) run ```pip install .``` or ```sudo pip3 install .```. This will install the package and it's dependencies. Keep in mind if you are looking to develop for pystall our [contribution guide](/contribution-guide) has information on how to get a dev environment setup.



## Built-in resource library

There is a built in set of predefined resources for common packages, if you have a relatively simple setup this may be a good option for you. The full list of resources is available in the [resource library list](/resource-library-list). In this example we are looking at a cross-platform example of installing [python](https://www.python.org/)(latest version: I know very meta), [golang](https://golang.org/), and [micro](https://micro-editor.github.io/):

```python
from pystall.core import build
from pystall.library import python, go, micro

build(python, go, micro)
```



## Custom defined resources

This script shows how to define your own resources based on the classes included in core of pystall. In this example I am defining: the python 3 latest installer the go installer and a static asset of an image (in this case a .png file):

```python
from pystall.core import EXEResource, MSIResource, StaticResource, build

python = EXEResource("python-installer", "https://www.python.org/ftp/python/3.8.1/python-3.8.1.exe")

go = MSIResource("Golang", "https://dl.google.com/go/go1.13.5.windows-amd64.msi")

logo = StaticResource("Wallpaper", ".png", "https://canadiancoding.ca/static/img/post-banners/python-post-banner.9bf19b390832.png")

build(python, go, logo)
```



If your resource does not fit into the predefined subclasses then take a look at [creating a custom subclass](/custom-subclasses).



## Logging

If you want logs while the script runs you can use the show_logs() function in the core library. Currently the show_logs() function only displays to stdout, but there are plans to add an optional file handler, and improve formatting down the road.

```python
from pystall.core import build, show_logs
from pystall.library import python, go, chrome, micro

show_logs()

build(python, go, chrome, micro)
```