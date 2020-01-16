![pystall logo](https://raw.githubusercontent.com/Descent098/pystall/master/pystall-logo.png)



A system to automate installation and configuration of resources.



## Quick-start

### Installation



#### From PyPi

You can install the project from PyPi using ```pip install pystall``` or ```pip3 install pystall```



#### From Source

clone this source repo using either the github button or ```git clone https://github.com/Descent098/pystall```

Then in the root directory (the one with setup.py) run ```pip install .``` or ```sudo pip3 install .``` This will install the package and it's dependencies.



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

For a full list of available library resources, how to extend the framework for specific functionality, and a development guide if you would like to contribute,  check the docs: https://pystall.readthedocs.io/en/latest/



## Roadmap

For more detailed roadmap check out the project planning board on github: https://github.com/Descent098/pystall/projects/1



## Assumptions

- You are running Windows, Linux (currently debian-based, with arch support in future), or Mac OS (on the way)
- Your machine is x86 64-bit based (no I won't be adding 32-bit support, but arm support is coming)
- You have an internet connection (if downloading resources and not using local copies of installers)



## What is Pystall?

**Pystall is:**

- A system to write single scripts to setup environments across platforms
- A relatively boilerplate-free method of writing system configurations
- A way to create easy to distribute binaries to handle complicated installations.
- Meant for end-users looking for a simple syntax to create scripts



**Pystall is not:**

- A server management utility
- An infrastructure management utility
- An orchestration replacement (ansible, jenkins, puppet, chef etc.)
- Meant for consistent (in terms of frequency) updating to existing packages (though i'm not opposed to this in the future necessarily)
- An **ABSOLUTELY** automated system, due to the amount of tradeoffs of extensibility I have opted to leave installers to be configured as they run (i.e. running the python installer exe still requires you to do the configuration).
