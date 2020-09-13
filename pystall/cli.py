# Standard Library Dependencies
import os                            # Path validation
from collections import defaultdict  # Used to make resource setup from a file simpler

# Internal Dependencies
from .core import *                  # Importing all installation functionality from the core module

# Third-Party Dependencies
import yaml                          # Used to parse resource files
from colored import fg               # Used to color output to terminal
from docopt import docopt            # Used for command line input parsing

usage = """
    Usage: 
        pystall [-h] [-v] [-f FILE_PATH] [-l] [-d]

    A system to automate fresh OS installs

    Options:
    -h, --help            show this help message and exit
    -v, --version         show program's version number and exit
    -f FILE_PATH, --file FILE_PATH
                            Specify the path to the JSON file with section
                            information
    -l, --log             If present will output logs to sys.stdout
    -d, --doc             If present will open up the pystall docs
    """

arguments = docopt(usage, version="Pystall V 0.0.1")

def _read_resource(file_path:str) -> dict:
    """Reads a resource file and returns a dict of the resources specified

    Parameters
    ----------
    file_path : str
        The path to the resource file

    Returns
    -------
    dict
        A dictionary where each top-level key is a specified resource

    Raises
    ------
    FileExistsError
        Raised when the file specified is not a valid file path
    """
    if not os.path.isfile(file_path):  # If the file path specified doesn't exist
        raise FileExistsError(f"Specified resource file {file_path} does not exist")

    with open(file_path, "r") as resource_file:  # Load in the resource file
        resources = yaml.safe_load(resource_file)

    resources = resources["Resources"]  # Grab everything under the "Resources" attribute

    return resources

def _validate_resources(resources:dict) -> tuple:
    """Check the required fields for a resource, and validate they are present

    Parameters
    ----------
    resources : dict
        A dictionary containing all the resources to install

    Returns
    -------
    tuple|None
        Returns a tuple of Resource instances, or None if any of the resources are not properly specified
    """
    processed_resources = defaultdict(lambda: False) # Any unspecified keys will be False

    for label in resources:
        # Check required fields for a given resource type
        try:
            resources[label]["type"]  # Checking resource has a type
        except KeyError:
            print(f"{fg('red')}Resource {label} does not specify a type{fg('white')}")
            return
        if not resources[label]["type"] in ["ppa", "apt"]:
            try:
                resources[label]["location"]  # Checking resource has a location specified
            except KeyError:
                print(f"{fg('red')}Resource {label} does not specify a location{fg('white')}")
                return
        elif resources[label]["type"] == "ppa":
            try:
                resources[label]["ppa"]  # Checking resource has a ppa specified
                resources[label]["packages"]  # Checking resource has packages specified
            except KeyError:
                print(f"{fg('red')}Resource {label} does not specify a PPA and/or package{fg('white')}")
                return
        elif resources[label]["type"] == "apt":
            try:
                resources[label]["packages"]  # Checking resource has packages specified
            except KeyError:
                print(f"{fg('red')}Resource {label} does not specify a package{fg('white')}")
                return

        processed_resources = defaultdict(lambda: False) # Any unspecified keys will be False
        for key in resources[label]: # Convert the inner dict of each resource to a defaultdict
            processed_resources[key] = resources[label][key]
        resources[label] = processed_resources 

    resource_instances = () # Instantiate empty tuple to fill with resources

    for resource in resources: # Take resource data and turn them into actual resource instances
        if resources[resource]["type"] == "exe":
            resource_instances = EXEResource(resource,
                resources[resource]["location"],
                resources[resource]["arguments"],
                resources[resource]["downloaded"],
                resources[resource]["remove"],
                resources[resource]["overwrite_agreement"])
        elif resources[resource]["type"] == "zip":
            resource_instances = ZIPResource(resource,
                resources[resource]["location"],
                resources[resource]["arguments"],
                resources[resource]["downloaded"],
                resources[resource]["remove"],
                resources[resource]["overwrite_agreement"])
        elif resources[resource]["type"] == "msi":
            resource_instances = MSIResource(resource,
                resources[resource]["location"],
                resources[resource]["arguments"],
                resources[resource]["downloaded"],
                resources[resource]["remove"],
                resources[resource]["overwrite_agreement"])
        elif resources[resource]["type"] == "static":
            resource_instances = StaticResource(resource,
                resources[resource]["location"],
                resources[resource]["arguments"],
                resources[resource]["downloaded"],
                resources[resource]["remove"],
                resources[resource]["overwrite_agreement"])
        elif resources[resource]["type"] == "deb":
            resource_instances = DEBResource(resource,
                resources[resource]["location"],
                resources[resource]["arguments"],
                resources[resource]["downloaded"],
                resources[resource]["remove"],
                resources[resource]["overwrite_agreement"])
        elif resources[resource]["type"] == "ppa":
            resource_instances = CUSTOMPPAResource(resource,
                resources[resource]["PPA"],
                resources[resource]["packages"],
                resources[resource]["overwrite_agreement"])
        elif resources[resource]["type"] == "tarball":
            resource_instances = TARBALLResource(resource,
                resources[resource]["location"],
                resources[resource]["arguments"],
                resources[resource]["downloaded"],
                resources[resource]["remove"],
                resources[resource]["overwrite_agreement"])
        elif resources[resource]["type"] == "apt":
            resource_instances = CUSTOMPPAResource(resource,
                resources[resource]["packages"],
                resources[resource]["overwrite_agreement"])
    return resource_instances

def build_from_file(*resource_files:str):
    """Takes an arbitrary number of paths to yaml files and builds specifies resources

    Parameters
    ----------
    resource_files: str
        An arbitrary number of file paths

    Examples
    --------
    Read in a file called resources.yml and install the resources
    ```
    from pystall.cli import build_from_file

    resource = build_from_file("C:\\Users\\Kieran\\Desktop\\resource.yml")
    ```
    """
    for resource_file in resource_files:
        resources = _read_resource(resource_file)
        resources = _validate_resources(resources)
        if resources:  # If resource preprocessing succeeds
            build(resources)
        else:  # If resource preprocessing fails
            print(f"{fg('red')}Ran into error preprocessing resources, see above for details{fg('white')}")
