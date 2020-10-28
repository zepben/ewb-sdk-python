# Zepben cimbend (WIP) #
This library provides Zepben's CIM profile as a python module for simplified interaction with Zepben services. You can find an overview and diagrams of Zepben's profile [here](https://zepben.bitbucket.io/cim/evolve/).

All classes exposed in `zepben.cimbend.cim` can be converted into protobuf messages and sent to/received from Zepben's gRPC services.

Note this project is still a work in progress and unstable, and breaking changes may occur prior to 1.0.0. 

More extensive documentation can be found in the [docs](docs/README.md)

# Basic Usage #

TODO

## Installation ##
Requirements:

1. Python 3.7+

Install straight from Pypi:

    pip install zepben.cimbend
    
## Developing ##

This library depends on protobuf and gRPC for messaging. To set up for developing against this library, clone it first:

    git clone https://github.com/zepben/evolve-sdk-python.git

Install as an editable install. Its recommended to install in a [Python virtualenv](https://virtualenv.pypa.io/en/stable/)

    cd evolve-sdk-python
    pip install -e .[test]

Run the tests: 

    python -m pytest

