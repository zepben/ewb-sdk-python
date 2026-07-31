# CIM dataclass Manifesto

Yes, this is not your usual manifest

## Why does this exist

We have removed the dataclassy library from the SDK, migrating to using the actual Python dataclass decorator. This was motivated by lack of ongoing support for dataclassy, as well as no-one on the team wanting to deal with its mess of magic code.

Our Python version of CIM has some very specific requirements leading to some unorthodox decisions (eg custom inits). Whatever your "why does it work this way" is, it has likely been considered, and many are answered below.

This document is to serve as a guide in case you need to modify the SDK and are unfamiliar with how things are implemented around here. The following are some major decisions we have made and how they influence your potential contribution.

## Slots

Due to the immense size of grid models we are dealing with, every byte of memory matters, lest you fry your RAM with 120% load. By default, Python stores instance values as a dictionary, which takes up hella space. Slots exist to fix that - a `__slots__` class variable describes the fixed attribute layout of a class, and through some dark magic (static instance-hashed attribute dictionaries) removes a lot of the memory overhead. Every single one of our CIM classes uses slots, and all the new ones should too. `@dataclass` with slots enabled saves us specifying them explicitly at the cost of transparency - every field of such a class is a descriptor, and overwrites don't always work the way you expect them to. (For example, `@property` overwrite of a static field in a superclass is completely ignored by Python).

Our chosen approach is delegating as much functionality as we can to the native Python `@dataclass`, which lets you rely on its documentation and AI's knowledge of its quirks. It might be weird, but it is weird in consistent ways. No more reading a random biologist's library to figure out why your ConnectivityNode just did a barrel roll! 

## Dataclass

We have chosen to use dataclasses simply because we have a lot of attributes, and any non-dataclass Python init requires a ridiculous amount of code duplication. This allows us to make use of its slot construction, as well as default values for fields that don't need to be passed in the init.

Unfortunately, dataclass generates custom `__init__` functions for the classes, but ONLY if you don't have an existing init already. That's why slightly tweaking class instantiation is quite complicated (requiring a custom decorator to rebuild the class from the original and the dataclass combined - I tried this). Instead, we went for a "clean slate" base class init approach (explained below), which, while stripping some of the dataclass functionality, is a lot more transparent when it explodes in your face.

## Instantiation

We have a lot of `@property` custom fields which are completely ignored by the dataclass constructor. We need our inits to allow such fields to be passed at instantiation time for backwards compatibility reasons. Hence we have a `DataclassBase` class which simply has an init that calls `setattr` on the `**kwargs` that are passed into it. This trips the `__set__` method for properties and custom descriptors, which is functionality we CANNOT give up.

The base init also sets unset values to defaults (and default factories) as would a normal dataclass. If a field has no default (aka it needs to be set at creation time), the appropriate error is raised. Note that this needs to happen after the aforementioneed `**kwarg` application loop.

We don't need init type hinting (technically we want the user to not use kwargs at all), except for `mrid` - which is why it's declared in the `Identifiable` constructor explicitly. 

In order to make sure that custom inits don't mess with the base init, every subclass needs to take `**kwargs` and pass them up to `super`. We also do the same for *args at the start of the function call, because at the very least `mrid` is often passed as positional.

Since `@dataclass` generates an init for every subclass without one, the `@zb_dataclas` sets `init=False` to disable all inits we have not specified ourselves.

## (Positional) Args are not a thing

Positional args are very hard to get consistent with the use of `@dataclass` - to know the order, you must parse the inheritance tree. `@property` values are not included in dataclass inits by default, meaning that adding them as an argument would create arbitrary ordering, and that is a readability nightmare. Moreover, we have custom inits in subclasses, making maintaining the arg order functionally impossible.

That is why, from this version onwards, any argument that is not the object's `mrid` (or equivalent identifier) must be passed as a keyword argument (`MyClass("mrid", 42)` bad, `MyClass("mrid", thing=42)` good).

While it would be possible to bring args back if all subclass inits are removed (probable future feature), it is a terrible idea. Do not do it unless you are very sure of yourself.

## Eq, Hash, Str, Repr

CIM classes need to be homogenous in their behaviour. Normally, dataclasses define these four methods on subclass level, but we need them to be propagated all the way up to `Identifiable` (or any overriding children such as `NameType`), where `__eq__` and `__hash__` both asses memory reference equality, and `__str__` and `__repr__` represent the class as `<ClassName>{<mrid>}` eg `Terminal{terminal_mrid}`. 

## Descriptors

Properties are bulky and limited in functionality. There is a more general python concept called a Descriptor. This is any class implementing `__get__` and/or (usually and) `__set__` methods, which overwrite accessing a class member (provided they are attached to the class and not its instance). This allows us to, for example, implement internally nullable fields.

These fields technically require no space in the object, since they access other values internally, but `@dataclass` assigns a slot to anything with a type. Obviously, if you want type hinting on member access, descriptor fields need to be typed. `@remove_descriptor_annotations` decorator (ordinarily part of `@zb_dataclass`) takes care of that by stripping the types off of anything defining the aforementioned methods before it gets passed to a dataclass. Since this happens at runtime, IDE type-checking still gets the types, and `@dataclass` is no longer confused about which fields should be created.

## Lists

Since CIM is UML-based, there are a lot of one-to-many and many-to-many class relationships, represented with lists. Most such relationships are usually empty. Python empty list is 56 bytes, whereas `None` is 16, so we want the lists to be nullable.

Consequently, we have created a hierarchy of nullable descriptors backed by private fields. Each descriptor implements a list-like interface, allowing the user to interact with the relations normally, blissfully unaware of the nullable insanity going on under the hood.

Due to the high diversity of the relationship behaviours, there is a lot of optional functionality shared by some these lists:

- *mRID collision checks*: for mrid collections, we perform an mRID lookup when an item is added. If another item comes back, we check if the identities match. If they do, we disregard the addition. If they don't, we throw an appropriate error.
- *backfill*: some items contained in lists link back to the owner item. In that case, we perform a backfill to do this automatically. We also ensure that the item is not already linked to another owner. 
- *validation*: some lists are create with validation lambdas, calling a validator function on the owner itself. This is useful when additional validation is required, eg sequence number matching.
- *sorting*: passing a sorting lambda to ordered collections automatically re-sorts the list after an item is added. 

Here are the concrete implementations of the lists that are used in the SDK:

- `LazyList`: A nullable list of non-`Identifiable` objects that has validation and sorting built in.
- `LazyIndexList`: `LazyList` with index-based insertion and deletion, for strictly ordered relationships such as diagram points.

The remaining collections all implement `MridCollection` - an interface that declares functionality of interaction with a collection of `Identifiable` objects, mainly focusing on `get_by_mrid`, `append`, `remove`, and `clear` methods. This allows us to have a common way of interacting with inter-object relationships, while hiding the underlying implementation (eg `list` vs `dict`)

- `LazyMridList`: A `LazyList` with an mrid check and backfill added. `O(N)` mRID lookup.
- `MridList`: An mRID collection backed by a non-nullable list. Useful for relationships that are most likely to be filled (eg `ConnectivityNode.terminals`). `O(N)` mRID lookup.
- `LazyMridMap`: A nullable map of Identifiable objects keyed on their mRID. Supports mRID checks and `O(1)` mRID lookup. Does not support sorting (duh). Useful fot large-scale collections (for which the lookup speedup is significant) 
