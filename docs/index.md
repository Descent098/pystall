# Welcome to the Pystall Docs

<img src="https://raw.githubusercontent.com/Descent098/pystall/master/docs/img/pystall-logo.png" alt="pystall logo" style="zoom:100%;  margin-left: auto; margin-right: auto; display: block;"/>

Pystall is a utility to help download & install resources on your system. Unlike regular configuration utilities pystall is designed to be run-and-done without leaving any daemons or obscure monitoring services running on your machine.



If you just want to dive in check out the [quick-start](/quick-start) for the basic usage and installation details.

## Features

- Pull from a [built in resource library](https://pystall.readthedocs.io/en/latest/resource-library-list/) for quick installation
- Define your own [custom local and remote resources](https://pystall.readthedocs.io/en/latest/quick-start/#custom-defined-resources)
- Built in [logging](#logging)
- The ability to build scrips into a [no dependency binary](https://pystall.readthedocs.io/en/latest/creating-binary-distributions/)
- Specification of [resources in files](https://pystall.readthedocs.io/en/latest/file-resources/)
- And more

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

