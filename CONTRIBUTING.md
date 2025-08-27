# Developing ##

This library depends on protobuf and gRPC for messaging. To set up for developing against this library, clone it first:

```
git clone https://github.com/zepben/evolve-sdk-python.git
```

Install grpc updates locally as an editable install.

```
cd evolve-grpc
pip install -e .
```

Install as an editable install. It's recommended to install in a [Python virtualenv](https://virtualenv.pypa.io/en/stable/)

```
cd evolve-sdk-python
pip install -e .[test]

#If the above pip install doesn't work.
python -m pip install --editable '.[test]'
```

Run the tests:

```
python -m pytest
```

You can generate the [coverage report](htmlcov/index.html) using the following options:

```
 pytest --cov=zepben.ewb --cov-report=html --cov-branch
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
1. Add new classes to the [cim model package](src/zepben/ewb/model/cim).
1. Descriptions copied from [Evolve CIM Profile documentation](https://zepben.github.io/evolve/docs/cim/evolve) and added as doc comments to new changes (on
   class, property etc)
1. Add comparators to [service packages](src/zepben/ewb/services).
  1. [network](src/zepben/ewb/services/network/network_service_comparator.py)
  1. [customer](src/zepben/ewb/services/customer/customer_service_comparator.py)
  1. [diagram](src/zepben/ewb/services/diagram/diagram_service_comparator.py)
1. Update [translator package](src/zepben/ewb/services/network/translator):
1. Update [```__init__.py```](src/zepben/ewb/services/network/translator/__init__.py):
   * ```from zepben.protobuf...<new_class_name>_pb2 import <new_class_name>```
   * ```<new_class_name>.mrid = lambda self: self...mrid()```
1. Update [network_cim2proto.py](src/zepben/ewb/services/network/translator/network_cim2proto.py):
   * ```import <new_class_name> as PB<new_class_name>```
   * Add ```def <new_class_name>_to_pb```
   * Add ```"<new_class_name>_to_pb"``` to ```__all__```
   * Annotate ```<new_class_name>_to_pb``` with the ```@bind_to_pb``` decorator
1. Update  [network_proto2cim.py](src/zepben/ewb/services/network/translator/network_proto2cim.py)
   * ```import <new_class_name> as PB<new_class_name>```
   * Add ```def <new_class_name>_to_pb```
   * Add ```"<new_class_name>_to_cim"``` to ```__all__```
   * Annotate ```<new_class_name>_to_cim``` with the ```@bind_to_cim``` decorator
1. Add reference resolver(s) to resolvers in [common package](src/zepben/ewb/services/common)  (if new associations).
1. Update database schema:
1. Increment `TablesVersion.SUPPORTED_VERSION` by 1 in [table_version.py](src/zepben/ewb/database/sqlite/tables/table_version.py)
1. In the [tables package](src/zepben/ewb/database/sqlite/tables), add a table class for each new CIM class and many-to-many association.
   Update any previously-existing table classes whose CIM classes have field changes.
1. Register new tables into `_included_tables()`
  1. [network](src/zepben/ewb/database/sqlite/network/network_database_tables.py)
  1. [customer](src/zepben/ewb/database/sqlite/customer/customer_database_tables.py)
  1. [diagram](src/zepben/ewb/database/sqlite/diagram/diagram_database_tables.py)
1. Update `*CIMReader` for new CIM classes/associations and field updates.
  1. [network](src/zepben/ewb/database/sqlite/network/network_cim_reader.py)
  1. [customer](src/zepben/ewb/database/sqlite/customer/customer_cim_reader.py)
  1. [diagram](src/zepben/ewb/database/sqlite/diagram/diagram_cim_reader.py)
     Then, update `*ServiceReader` to load from each new tables.
  1. [network](src/zepben/ewb/database/sqlite/network/network_service_reader.py)
  1. [customer](src/zepben/ewb/database/sqlite/customer/customer_service_reader.py)
  1. [diagram](src/zepben/ewb/database/sqlite/diagram/diagram_service_reader.py)
1. Update `*CIMWriter` for new CIM classes/associations and field updates.
  1. [network](src/zepben/ewb/database/sqlite/network/network_cim_writer.py)
  1. [customer](src/zepben/ewb/database/sqlite/customer/customer_cim_writer.py)
  1. [diagram](src/zepben/ewb/database/sqlite/diagram/diagram_cim_writer.py)
     Then, update `*ServiceWriter` to write to each new table.
  1. [network](src/zepben/ewb/database/sqlite/network/network_service_writer.py)
  1. [customer](src/zepben/ewb/database/sqlite/customer/customer_service_writer.py)
  1. [diagram](src/zepben/ewb/database/sqlite/diagram/diagram_service_writer.py)
1. Update [```__init__.py```](src/zepben/ewb/__init__.py) to import every new public name (classes, functions, constants, extension methods):


* ```from zepben.ewb...<new_module_name> import *```


1. Testing:


* Import public names via ```from zepben.ewb import <name>``` when writing/updating tests. This ensures that
  [```__init__.py```](src/zepben/ewb/__init__.py) was updated correctly.
* Test for model classes.
* Add new classes to corresponding service translator test. [```test/services/.../translator```](test/services)
* Add the required creators to:
  - [```pb_creators.py```](test/streaming/get/pb_creators.py)
  - [```cim_creators.py```](test/cim/cim_creators.py)
    - If a relationship involving a branch class has been introduced. Add an entry in SAMPLE SET to ensure the correct leaf class is created for testing.
* Add test for each new comparator to  [test/services/...](test/services) package.
  * [network](test/services/network/test_network_service_comparator.py)
  * [customer](test/services/customer/test_customer_service_comparator.py)
  * [diagram](test/services/diagram/test_diagram_service_comparator.py)
* Add test for each new class to  [test/cim/...](test/cim) package.
* Test database schema:
  - Handle each new direct association in `_add_with_references()`: [schema_utils.py](test/database/sqlite/schema_utils.py)
  - Include new concrete CIM classes in [```test_database_sqlite.py```](test/database/sqlite/test_database_sqlite.py).
* Verify that all the tests are passing.


1. Update release notes in [```changelog.md```](changelog.md).
1. Update _nio_type_to_cim in [```network_consumer.py```](src/zepben/ewb/streaming/get/network_consumer.py) to include newly added classes.

## Adding support for new services ##

Include new grpc services in the list of services ```GrpcChannelBuilder._test_connection()``` uses when attempting to confirm the connectivity of newly created
grpc channels.
