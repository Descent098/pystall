# Resource Library List

The custom resource library has many predefined resources that can be used easily in a script. It will have (currently only Windows and Debian Linux) them for multiple operating systems so the terminology doesn't change per OS. For example let's create a script that pulls in python, Visual Studio Code, Google Chrome, and git:

```python
from pystall.core import build, show_logs
from pystall.library import python, vscode, chrome, git

show_logs()

build(python, vscode, chrome, git)
```

Here is the list of all the currently implemented resources:



*Python*; The python programming language installer

- **Variable Name**: python
- **Website**: [http://python.org/](http://python.org/)
- **Type**: Binary installer, Custom PPA
- **OS's**: Windows, Linux



*Golang*; The go programming language installer

- **Variable Name**: go
- **Website**: [https://golang.org/](https://golang.org/)
- **Type**: Binary installer, Custom PPA
- **OS's**: Windows, Linux



*Visual Studio Code*: Visual Studio Code text editor

- **Variable Name**: vscode
- **Website**: [https://code.visualstudio.com/](https://code.visualstudio.com/)
- **Type**: Binary installer
- **OS's**: Windows, Linux



*Git*; The git version control system installer

- **Variable Name**: git
- **Website**: [https://git-scm.com/](https://git-scm.com/)
- **Type**: Binary installer, APT package
- **OS's**: Windows, Linux



*Open Broadcast System*; The open broadcast system installer

- **Variable Name**: obs
- **Website**: [https://obsproject.com/](https://obsproject.com/)
- **Type**: Binary installer, Custom PPA
- **OS's**: Windows, Linux



*Rustlang*; The rust language installer

- **Variable Name**: rust
- **Website**: [https://www.rust-lang.org/](https://www.rust-lang.org/)
- **Type**: Binary installer
- **OS's**: Windows



*Haskell*; The haskell language installer

- **Variable Name**: haskell
- **Website**: [https://haskell.org/](https://haskell.org/)
- **Type**: Binary installer, APT Resource
- **OS's**: Windows, Linux



*Typora*; The typora markdown editor installer

- **Variable Name**: typora
- **Website**: [https://www.typora.io/](https://www.typora.io/)
- **Type**: Binary installer
- **OS's**: Windows



*Steam*; The steam game storefront installer

- **Variable Name**: steam
- **Website**: [https://store.steampowered.com/](https://store.steampowered.com/)
- **Type**: Binary installer, APT Resource
- **OS's**: Windows, Linux



*Google Chrome*;  The google chrome browser installer

- **Variable Name**: chrome
- **Website**: [https://www.google.com/chrome/](https://www.google.com/chrome/)
- **Type**: Binary installer
- **OS's**: Windows, Linux



*Mozilla FireFox*;  The mozilla FireFox browser installer

- **Variable Name**: chrome
- **Website**: [https://www.mozilla.org/en-CA/firefox/](https://www.mozilla.org/en-CA/firefox/)
- **Type**: Binary installer
- **OS's**: Windows, Linux



*Brave*;  The brave browser installer

- **Variable Name**: brave
- **Website**: [https://brave.com/](https://brave.com/)
- **Type**: Binary installer
- **OS's**: Windows



*Opera*;  The opera browser installer

- **Variable Name**: opera
- **Website**: [https://www.opera.com/](https://www.opera.com/)
- **Type**: Binary installer
- **OS's**: Windows, Linux



*Creative Cloud Desktop App*;  The creative cloud desktop app zip

- **Variable Name**: creative_cloud
- **Website**: [https://www.adobe.com/ca/creativecloud.html](https://www.adobe.com/ca/creativecloud.html)
- **Type**: ZIP archive
- **OS's**: Windows



*Cmder Terminal Emulator*;  The Cmder Terminal Emulator zip

- **Variable Name**: cmder
- **Website**: [https://cmder.net/](https://cmder.net/)
- **Type**: ZIP archive
- **OS's**: Windows



*Micro Terminal Text Editor*;   The micro console text editor zip

- **Variable Name**: micro
- **Website**: [https://micro-editor.github.io/](https://micro-editor.github.io/)
- **Type**: ZIP archive, TARBALL archive
- **OS's**: Windows, Linux

