# Zepben cimbend (WIP) #
This library provides Zepben's CIM profile as a python module for simplified interaction with Zepben services. You can find an overview and diagrams of Zepben's profile [here](https://zepben.bitbucket.io/docs/cim/zepben/).

All classes exposed in `zepben.model` can be converted into protobuf messages and sent to/received from Zepben's gRPC services.

Note this project is still a work in progress and intended for development use only, and thus should be considered unstable. however the framework of `zepben.model` should mostly stay the same.

More extensive documentation can be found in the [docs](docs/README.md)

# Basic Usage #

## Installation ##
Requirements:
    Python 3.7+

This library depends on protobuf and gRPC for messaging. To set up for developing against this library, clone it first:

    git clone git@bitbucket.org:zepben/cimbend.git

Install as an editable install. Its recommended to install in a [Python virtualenv](https://virtualenv.pypa.io/en/stable/)
    cd cimbend
    pip install -e .




# Testing #

Install pytest: `pip install pytest`
Run the tests: `python -m pytest`
Run only one test file: `python -m pytest test/test_abc.py`
