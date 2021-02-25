![Build Status](https://img.shields.io/github/workflow/status/zepben/evolve-sdk-python/Deploy%20snapshot%20to%20Pypi)
[![Coverage](https://coveralls.io/repos/github/zepben/evolve-sdk-python/badge.svg)](https://coveralls.io/github/zepben/evolve-sdk-python)

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

## Checklist for model changes ##

1. Update `setup.py` to import the correct version of `zepben.protobuf`.
1. Model updating:
   1. Add new classes to the [model package](src/zepben/evolve/model/). 
   1. Descriptions copied from [Evolve CIM Profile documentation](https://zepben.github.io/evolve/docs/cim/evolve) and added as doc comments to new changes (on class, property etc)
1. Update [translator package](src/zepben/evolve/services/network/translator):
   1. Update [```__init__.py```](src/zepben/evolve/services/network/translator/__init__.py):
      * ```from zepben.protobuf...<new_class_name>_pb2 import <new_class_name>```
      * ```<new_class_name>.mrid = lambda self: self...mrid()```
   1. Update [network_cim2proto.py](src/zepben/evolve/services/network/translator/network_cim2proto.py):
      * ```import <new_class_name> as PB<new_class_name>```
      * Add ```def <new_class_name>_to_pb```  
      * Add ```"<new_class_name>_to_pb"``` to ```__all__```
      * Add ```<new_class_name>.to_pb = <new_class_name>_to_pb```
   1. Update  [network_proto2cim.py](src/zepben/evolve/services/network/translator/network_proto2cim.py)
      * ```import <new_class_name> as PB<new_class_name>```
      * Add ```def <new_class_name>_to_pb```  
      * Add ```"<new_class_name>_to_cim"``` to ```__all__```
      * Add ```<new_class_name>_to_cim = <new_class_name>_to_cim```                
1. Update [network_rpc.py](src/zepben/evolve/streaming/put/network_rpc.py)
   * Add ```from zepben.protobuf...<new_class_name>_pb2 import <new_class_name>```
   * Add ```<new_class_name>: ('Create<new_class_name>', Create<new_class_name>),```
1. Add reference resolver(s) to resolvers in [common package](src/zepben/evolve/services/common)  (if new associations).
1. Testing:
   * Add the required creators to:
     - [```pb_creators.py```]()
     - [```cim_creators.py```](test/cim_creators.py)
   * Update [```constructor_validation.py```](test/cim/constructor_validation.py) 
   * Add test for each new class to  [test/cim/...](test/cim) package.
   * Verify that al the test are passing. 
1. Update release notes in [```changelog.md```](changelog.md).
