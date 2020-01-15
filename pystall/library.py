"""Contains commonly used resources for easy installation.


Variables
---------
python :  EXEResource
    Instance to download and install python language 3.8.1.

go :  MSIResource
    Instance to download and install go language.

vscode :  EXEResource
    Instance to download and install VS Code editor.

git :  EXEResource
    Instance to download and install git version controll.

obs :  EXEResource
    Instance to download and install OBS (open broadcast system).

rust :  EXEResource
    Instance to download and install rust language.

haskell :  EXEResource
    Instance to download and install haskell language.

typora :  EXEResource
    Instance to download and install typora markdown editor.

steam :  EXEResource
    Instance to download and install steam game storefront.

chrome :  EXEResource
    Instance to download and install chrome browser.

firefox :  EXEResource
    Instance to download and install firefox browser.

brave :  EXEResource
    Instance to download and install brave browser.

opera :  EXEResource
    Instance to download and install opera browser.

creative_cloud :  ZIPResource
    Instance to download and install the creative cloud desktop app.
    NOTE: Not yet implemented, just downloads and extracts files.

cmder :  ZIPResource
    Instance to download and install cmder terminal emulator.
    NOTE: Not yet implemented, just downloads and extracts files.

micro :  ZIPResource
    Instance to download and install micro console editor.
    NOTE: Not yet implemented, just downloads and extracts files.


Examples
--------
```
from pystall.core import build, show_logs

from pystall.library import python, go, chrome

show_logs()

build(python, go, chrome)
```
"""

import os

import distro

from .core import *

DEBIAN_BASED = ["ubuntu",
                "zorin",
                "lunixmint",
                "parrot",
                ]

ARCH_BASED = ["manjaro"]


if os.name == "nt": # Windows installers
    python = EXEResource("Python 3", "https://www.python.org/ftp/python/3.8.1/python-3.8.1.exe")

    go = MSIResource("Golang", "https://dl.google.com/go/go1.13.5.windows-amd64.msi")

    vscode = EXEResource("VS Code", "https://aka.ms/win32-x64-user-stable")

    git = EXEResource("git", "https://git-scm.com/download/win")

    obs = EXEResource("OBS", "https://cdn-fastly.obsproject.com/downloads/OBS-Studio-24.0.3-Full-Installer-x64.exe")

    rust = EXEResource("Rust", "https://win.rustup.rs/") # TODO: Broken installer

    haskell = EXEResource("Haskell", "https://get.haskellstack.org/stable/windows-x86_64-installer.exe")

    typora = EXEResource("Typora", "https://www.typora.io/windows/typora-setup-x64.exe?")

    steam = EXEResource("Steam", "https://steamcdn-a.akamaihd.net/client/installer/SteamSetup.exe")

    chrome = EXEResource("Chrome", "https://dl.google.com/tag/s/appguid%3D%7B8A69D345-D564-463C-AFF1-A69D9E530F96%7D%26iid%3D%7BA2B477FB-347D-0D81-0E1D-31E2F9C2938D%7D%26lang%3Den%26browser%3D4%26usagestats%3D1%26appname%3DGoogle%2520Chrome%26needsadmin%3Dprefers%26ap%3Dx64-stable-statsdef_1%26installdataindex%3Dempty/update2/installers/ChromeSetup.exe")

    firefox = EXEResource("FireFox", "https://download.mozilla.org/?product=firefox-stub&os=win&lang=en-CA&attribution_code=c291cmNlPXd3dy5nb29nbGUuY29tJm1lZGl1bT1yZWZlcnJhbCZjYW1wYWlnbj0obm90IHNldCkmY29udGVudD0obm90IHNldCk.&attribution_sig=5d58068ab4ba5299f75ac9c252cf1dc4d489fe60ad5cb511a02222e81f68e2a5")

    brave = EXEResource("Brave", "https://referrals.brave.com/latest/BraveBrowserSetup-INS628.exe")

    opera = EXEResource("Opera", "https://net.geo.opera.com/opera/stable/windows?utm_tryagain=yes&utm_source=google_via_opera_com&utm_medium=ose&utm_campaign=(none)_via_opera_com_https&http_referrer=https%3A%2F%2Fwww.google.com%2F&utm_site=opera_com&utm_lastpage=opera.com/&dl_token=48508072")

    creative_cloud = ZIPResource("Creative Cloud", "http://ccmdl.adobe.com//AdobeProducts/KCCC/CCD/5_0/win64/ACCCx5_0_0_354.zip")

    cmder = ZIPResource("cmder", "https://github.com/cmderdev/cmder/releases/download/v1.3.13/cmder.zip")
    
    micro = ZIPResource("micro editor", "https://github.com/zyedidia/micro/releases/download/v1.4.1/micro-1.4.1-win64.zip")

else: # Mac OS or linux

    if distro.id() in DEBIAN_BASED:
        # TODO: Define debian equivalent resources here

    if distro.id() in ARCH_BASED:
        #TODO: Define arch equivalent resources here

    if "fedora" in distro.id():
        #TODO: Define fedora equivalent resources here

