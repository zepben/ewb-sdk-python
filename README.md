# Zepben Evolve Python SDK #
The Python Evolve SDK contains everything necessary to communicate with a [Zepben EWB Server](https://github.com/zepben/energy-workbench-server). See the [architecture](docs/architecture.md) documentation for more details.

ote this project is still a work in progress and unstable, and breaking changes may occur prior to 1.0.0. 

# Requirements #

- Python 3.7 or later
- pycryptodome, which requires a C/C++ compiler to be installed.
On Linux, python headers (typically `python-dev`) is also necessary to build pycryptodome.

##### On Windows systems: 

Download and run [Build Tools for Visual Studio 2019](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019)

When in the installer, select and install:
- C++ build tools
- Windows 10 SDK
- The latest version of MSVC v142 x64/x86 build tools.

After this you should be able to `pip install zepben.evolve` without issues.

# Installation #

    pip install zepben.evolve
    
    
# Building #

    python setup.py bdist_wheel
    
# Developing ##

This library depends on protobuf and gRPC for messaging. To set up for developing against this library, clone it first:

    git clone https://github.com/zepben/evolve-sdk-python.git

Install as an editable install. It's recommended to install in a [Python virtualenv](https://virtualenv.pypa.io/en/stable/)

    cd evolve-sdk-python
    pip install -e .[test]

Run the tests: 

    python -m pytest

