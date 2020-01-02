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
  * Logging
  * Error Catching
  * Installers: .MSI, .Deb
  * Package managers: Custom PPA's, installs of regular packages
  * Image formats: .png, .jpg etc. (Wallpaper downloader)
  * Video downloads
  * Archive files: .zip, .tar.gz, etc.

"""

# Standard lib dependencies
import os
import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass

# Third party dependencies
import requests 


if os.name == "nt":
    DOWNLOAD_FOLDER = f"{os.getenv('USERPROFILE')}\Downloads"

else: # PORT: Assuming variable is there for MacOS and Linux installs
    DOWNLOAD_FOLDER = f"{os.getenv('HOME')}/Downloads" #TODO: Verify this is the right directory

@dataclass
class Resource:
    name: str
    location: str
    arguments: list
    downloaded: bool = False
    file_path: str=""
    

class Assets(ABC):
    """Base class to be inherited by different assets.

    Attributes
    ----------
    type : (str)
        The string representation of the type
    
    extension: (str)
        what extension this type applies to.
    
    label: (str)
        A human-readable label for the asset instance.
    
    resources: (resource)
        The object of resources to download
        NOTE: Accepts more than one instance

    Methods
    -------
    download: (list)
        Download resources specified in location variable
    
    install: (None)
        Runs any necessary steps after downloading resources.

    """
    def __init__(self, asset_type, extension, label, *resources):
        self.asset_type = asset_type
        self.extension = extension
        self.label = label
        self.resources = resources
    
    @abstractmethod
    def download(self) -> None:
        """Download required files from location specified in instance"""
        raise NotImplementedError

    @abstractmethod
    def install(self) -> None:
        """installation steps after all necessary downloads are completed"""
        raise NotImplementedError

    def get(self):
        """downloads and installs everything specified"""
        self.download()
        self.install()


class EXEAssets(Assets):
    def __init__(self, label, *resources):
        super().__init__("Windows Binary", ".exe", label, resources)
        self.resources = self.resources[0] # Flatten the unpacked tuple

    def download(self):
        resource_locations = [] # List of resource paths after they have been downloaded
        for resource in self.resources:
            resource_path = f"{DOWNLOAD_FOLDER}{os.sep}{resource.name}.exe"
            
            file_content = requests.get(resource.location)
            open(resource_path, 'wb').write(file_content.content) # Save file
            # TODO: Error catching
            resource.downloaded = True
            resource.file_path = resource_path
        

    def install(self):
        for resource in self.resources:
            if resource.downloaded:
                subprocess.run(resource.file_path)
            else:
                print(f"{resource.name} failed to install")


if __name__ == "__main__":
    python_install = EXEAssets("python-install", Resource("python-install", "https://www.python.org/ftp/python/3.8.1/python-3.8.1.exe", None), Resource("rustup", "https://win.rustup.rs/", None))
    python_install.get()