# Resource Library List

As of version 0.3 you can now specify files for resources. This is done through a simple [YAML](https://docs.octoprint.org/en/master/configuration/yaml.html) file that allows you to specify multiple resources. The schema follows the exact same schema as the corresponding resource type. So for example with ```EXEResources``` it would follow the same schema as an ```EXEResource``` instance in python would.

Below is an example of a "fully filled out" resource file with one ```exe``` resource:

```yml
Resources:
  "python":
    type: "exe"
    location: "https://www.python.org/ftp/python/3.8.1/python-3.8.1.exe"
    arguments: ["-a", "-b", "-c"]
    downloaded: false
    remove: true
    overwrite_agreement: false
    # Dependencies are not specified because you can just add them as a resource yourself
```

To then install from a resource file simply install ```pystall``` then run code such as this:

```python
from pystall.cli import build_from_file

resource_file_path = "resource.yml" # Make this the path to your resource file

build_from_file(resource_file_path) # Goes through and gets all the resources from the file and builds them
```

## Multiple resources in one file

It's important to note you can add multiple resources to a single file. The important thing is you need the ```Resources``` top heading, and then each resource is defined with a string representing it's ```label``` (such as "python" above). 

Here is an example of a resource file with multiple resources defined:

```yml
Resources:
  "python":
    type: "exe"
    location: "https://www.python.org/ftp/python/3.8.1/python-3.8.1.exe"
    downloaded: false
    remove: true
    overwrite_agreement: false
  "Micro Zip":
    type: "zip"
    location: "https://github.com/zyedidia/micro/releases/download/v1.4.1/micro-1.4.1-win64.zip"
    remove: true
    overwrite_agreement: true
```

## Minimum setup

The above example is a bit verbose, here is an example of the minimum necessary attributes specified for an ```EXEResource```:
```yml
Resources:
  "python":
    type: "exe"
    location: "https://www.python.org/ftp/python/3.8.1/python-3.8.1.exe"
```

The only two attributes necessary for most resource types, are a **location**, and a **type**. **There are** however **exceptions** to this **with certain types**, so see the [Available Types](#available-types) section below for details about required fields.

## Available Types

Here is a table of the available types, the "YAML type" is the type you would use in the YAML file, and the "Python equivalent" is what it equates to in the python package. Additionally I have included all required fields for each type, be aware that **EVERYTHING is lowercase including the types and required fields**.

| YAML Type | Python Equivalent | Required Fields           |
| --------- | ----------------- | ------------------------- |
| exe       | EXEResource       | type, location            |
| msi       | MSIResource       | type, location            |
| zip       | ZIPResource       | type, location            |
| static    | StaticResource    | type, location, extension |
| deb       | DEBResource       | type, location            |
| ppa       | CUSTOMPPAResource | type, ppa, packages       |
| tarball   | TARBALLResource   | type, location            |
| apt       | CUSTOMPPAResource | type, packages            |

Here is an example of a resource file with various types:

```yml
Resources:
  "python":
    type: "exe"
    location: "https://www.python.org/ftp/python/3.8.1/python-3.8.1.exe"
  "Micro Zip":
    type: "zip"
    location: "https://github.com/zyedidia/micro/releases/download/v1.4.1/micro-1.4.1-win64.zip"
  "Wallpaper":
    type: "static"
    location: "https://images.unsplash.com/photo-1541599468348-e96984315921?ixlib=rb-1.2.1&auto=format&fit=crop&w=1600&h=500&q=60"
    extension: '.png'
  "Open Broadcast System":
    type: "ppa"
    ppa: "obsproject/obs-studio"
    packages: ["obs-studio"]
  "Steam":
    type: "apt"
    packages: ["steam"]
```

