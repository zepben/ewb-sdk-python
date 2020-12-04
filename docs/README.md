# Zepben Evolve Python SDK #
The Python Evolve SDK contains everything necessary to communicate with a [Zepben EWB Server](https://github.com/zepben/energy-workbench-server). See the [architecture](docs/architecture.md) documentation for more details.

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

After this you should be able to `pip install zepben.cimbend` without issues.

# Installation #

    pip install zepben.cimbend
    
    
# Building #

    python setup.py bdist_wheel
