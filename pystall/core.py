"""
This module contains core functionality of Pystall including:
    - Download management
    - Base class
    - Core installation logic


TODO
----
  * Update docstrings
  * Update Module level docstrings
  * Flesh out the quickstart more
  * Be able to set wallpaper from static Resource
  * Remove resource on exit option
  * Add download progress bars
  * Logging
  * Error Catching
  * Installers: .Deb
  * Package managers: Custom PPA's, installs of regular packages
  * Archive files: .zip, .tar.gz, etc.

"""

# Standard lib dependencies
import os
import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass
import logging

# Third party dependencies
import requests 
from tqdm import tqdm


if os.name == "nt":
    DOWNLOAD_FOLDER = f"{os.getenv('USERPROFILE')}\Downloads"

else: # PORT: Assuming variable is there for MacOS and Linux installs
    DOWNLOAD_FOLDER = f"{os.getenv('HOME')}/Downloads" #TODO: Verify this is the right directory

class Resource(ABC):
    def __init__(self, label, extension, location, arguments = False, downloaded = False):
        """Base class to be inherited from and extended.

        Attributes
        ----------

        label : (str)
            Human readable name for resource and used with extension in files name.

        extensions : (str)
            The extension of the filetype being downloaded
        
        location : (str)
            The path or URL to the resource that needs to be downloaded & installed
        
        arguments : (list|bool)
            Specify any arguments to be passed on installation, False indicates no arguments.
        
        downloaded : (bool)
            Placeholder value that gets set during download to ensure file was properly downloaded

        Methods
        -------
        download:
            Used to download files as necessary
        """
        self.label = label
        self.extension = extension
        self.location = location
        self.arguments = arguments
        self.downloaded = downloaded

    def download(self, file_path = False):
        """ Downloads asset from location specified in class instance.

        Attributes
        ----------
        file_path : (str|bool)
            The path to where the resource should download to. 
            Leave as false for download folder + name + extension.
            NOTE: Custom paths MUST include extension.
        """
        logging.info(f"Downloading {self.label}")

        if not file_path:
            file_path = f"{DOWNLOAD_FOLDER}{os.sep}{self.label}{self.extension}"

        if os.path.exists(file_path): # If file already exists
            self.downloaded = True
            self.location = file_path
            return

        logging.info("Starting binary download")
        file_content = requests.get(self.location)
        open(file_path, 'wb').write(file_content.content) # Save file
        # TODO: Error catching
        self.downloaded = True
        self.location = file_path

    @abstractmethod
    def install(self) -> None:
        """installation steps after all necessary downloads are completed"""
        raise NotImplementedError

class EXEResource(Resource):
    def __init__(self, label, location, arguments = False, downloaded = False):
        """Used to download and install .exe files.

        Attributes
        ----------

        label : (str)
            Human readable name for resource and used with extension in files name.
        
        location : (str)
            The path or URL to the resource that needs to be downloaded & installed
        
        arguments : (list|bool)
            Specify any arguments to be passed on installation, False indicates no arguments.
        
        downloaded : (bool)
            Placeholder value that gets set during download to ensure file was properly downloaded
        """
        super().__init__(label, ".exe", location, arguments, downloaded)

    def install(self):
        if self.downloaded:
            logging.info(f"Installing {self.label}")
            subprocess.run(self.location)
        else:
            logging.error(f"{self.name} failed to install")

class MSIResource(Resource):
    def __init__(self, label, location, arguments = False, downloaded = False):
        """Used to download and install .msi files.

        Attributes
        ----------

        label : (str)
            Human readable name for resource and used with extension in files name.
        
        location : (str)
            The path or URL to the resource that needs to be downloaded & installed
        
        arguments : (list|bool)
            Specify any arguments to be passed on installation, False indicates no arguments.
        
        downloaded : (bool)
            Used to deliniate if Resource is downloaded, if using local file set to True, else leave as False.
        """
        super().__init__(label, ".msi", location, arguments, downloaded)

    def install(self):
        logging.info(f"Installing {self.label}")
        if self.downloaded:
            subprocess.Popen(self.location, shell=True)
        else:
            print(f"{self.name} failed to install")

class StaticResource(Resource):
    def __init__(self, label, extension, location, arguments = False, downloaded = False):
        super().__init__(label, extension, location, arguments, downloaded)

    def install(self):
        logging.info("No installation necessary for StaticResources")
        pass

def build(*resources):
    """downloads and installs everything specified"""
    for resource in resources:
        if not resource.downloaded:
            resource.download()
        resource.install()


if __name__ == "__main__":
    import sys
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    
    python = EXEResource("python-installer", "https://www.python.org/ftp/python/3.8.1/python-3.8.1.exe")
    rust = EXEResource("rustup", "https://win.rustup.rs/")
    go = MSIResource("Golang", "https://dl.google.com/go/go1.13.5.windows-amd64.msi")
    logo = StaticResource("Wallpaper", ".png", "https://images.unsplash.com/photo-1541599468348-e96984315921?ixlib=rb-1.2.1&auto=format&fit=crop&w=1600&h=500&q=60", set_wallpaper=True)
    build(logo)