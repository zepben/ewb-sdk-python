# Developing ##

This library depends on protobuf and gRPC for messaging. To set up for developing against this library, clone it first:

```
git clone https://github.com/zepben/evolve-sdk-python.git
```

Install as an editable install. It's recommended to install in a [Python virtualenv](https://virtualenv.pypa.io/en/stable/)

```
cd evolve-sdk-python
pip install -e .[test]
```

Run the tests: 

```
python -m pytest
```

You can generate the [coverage report](htmlcov/index.html) using the following options:

```
 pytest --cov=zepben.evolve --cov-report=html --cov-branch
 ```

If you need to debug a test, you will need to annotate the test with the following
to prevent the test from timing out while you step through the code:

```
# todo remove timeout before commit
@pytest.mark.timeout(100000)
```

## Checklist for model changes ##

1. Update [`setup.py`](setup.py) to import the correct version of `zepben.protobuf`.
1. Model updating:
   1. Add new classes to the [cim model package](src/zepben/evolve/model/cim).
   1. Descriptions copied from [Evolve CIM Profile documentation](https://zepben.github.io/evolve/docs/cim/evolve) and added as doc comments to new changes (on class, property etc)
1. Add comparisons to [service packages](src/zepben/evolve/services).
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
1. Add reference resolver(s) to resolvers in [common package](src/zepben/evolve/services/common)  (if new associations).
1. Update database schema:
   1. In the [tables package](src/zepben/evolve/database/sqlite/tables), add table class for each new CIM class and many-to-many association,
      and update any with field changes.
   1. Add new tables to `_create_tables()` in [database_tables.py](src/zepben/evolve/database/sqlite/tables/database_tables.py)
   1. In the [readers package](src/zepben/evolve/database/sqlite/readers), update `*CIMReader` for new CIM classes/associations and field updates.
      Then, update `*ServiceReader` to load from any new tables.
   1. In the [writers package](src/zepben/evolve/database/sqlite/writers), update `*CIMWriter` for new CIM classes/associations and field updates.
      Then, update `*ServiceWriter` to write to any new tables.
1. Update [```__init__.py```](src/zepben/evolve/__init__.py) to import every new public name (classes, functions, constants, extension methods):
   * ```from zepben.evolve...<new_module_name> import *```
1. Testing:
   * Import public names via ```from zepben.evolve import <name>``` when writing/updating tests. This ensures that
     [```__init__.py```](src/zepben/evolve/__init__.py) was updated correctly.
   * Test for model classes.
   * Added new classes to corresponding service translator test. [```test/services/...```](test/services)
   * Add the required creators to:
     - [```pb_creators.py```](test/pb_creators.py)
     - [```cim_creators.py```](test/cim_creators.py)
   * Add test for each new comparison to  [test/services/...](test/services) package.
   * Add test for each new class to  [test/cim/...](test/cim) package.
   * Test database schema:
     - Add cases for all new associations in `_add_with_references()`: [schema_utils.py](test/database/sqlite/schema_utils.py)
     - Update [```test_database_sqlite.py```](test/database/sqlite/test_database_sqlite.py) for new concrete CIM classes.
   * Verify that all the tests are passing. 
1. Update release notes in [```changelog.md```](changelog.md).
