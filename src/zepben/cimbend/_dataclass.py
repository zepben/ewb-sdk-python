#  Copyright 2020 Zeppelin Bend Pty Ltd
# 
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclassy import fields
from dataclassy.dataclass import _generate_new, __repr__, __iter__, __setattr__, __hash__, __eq__, __lt__, DataClassMeta
from types import FunctionType as Function


class DataClassMetaZ(DataClassMeta):
    """The metaclass for a data class."""
    DEFAULT_OPTIONS = dict(init=True, repr=True, eq=True, iter=False, frozen=False, kwargs=False, slots=False,
                           order=False, unsafe_hash=True, hide_internals=True)

    def __new__(mcs, name, bases, dict_, **kwargs):
        # collect annotations, defaults, slots and options from this class' ancestors, in definition order
        all_annotations = {}
        all_defaults = {}
        all_slots = set()
        options = dict(mcs.DEFAULT_OPTIONS)

        dataclass_bases = [vars(b) for b in bases if hasattr(b, '__dataclass__')]
        for b in dataclass_bases + [dict_]:
            all_annotations.update(b.get('__annotations__', {}))
            all_defaults.update(b.get('__defaults__', dict_))
            all_slots.update(b.get('__slots__', set()))
            options.update(b.get('__dataclass__', {}))
        options.update(kwargs)

        # fill out this class' dict and store defaults, annotations and decorator options for future subclasses
        dict_.update(all_defaults)
        dict_['__defaults__'] = all_defaults
        dict_['__annotations__'] = all_annotations
        dict_['__dataclass__'] = options

        # delete what will become stale references so that Python creates new ones
        del dict_['__dict__'], dict_['__weakref__']

        # create/apply generated methods and attributes
        user_init = type(dict_.get('__init__')) is Function

        if options['slots']:
            # values with default values must only be present in slots, not dict, otherwise Python will interpret them
            # as read only
            for d in all_annotations.keys() & all_defaults.keys():
                del dict_[d]
            dict_['__slots__'] = all_annotations.keys() - all_slots
        elif '__slots__' in dict_:
            # if the slots option has been removed from an inheriting dataclass we must remove descriptors and __slots__
            for d in all_annotations.keys() - all_defaults.keys() & dict_.keys():
                del dict_[d]
            del dict_['__slots__']
        if options['init']:
            dict_.setdefault('__new__', _generate_new(all_annotations, all_defaults, user_init,
                                                      options['kwargs'], options['frozen']))
        if options['repr']:
            dict_.setdefault('__repr__', __repr__)
        if options['eq']:
            dict_.setdefault('__eq__', __eq__)
        if options['iter']:
            dict_.setdefault('__iter__', __iter__)
        if options['frozen']:
            dict_['__delattr__'] = dict_['__setattr__'] = __setattr__
        if options['order']:
            dict_.setdefault('__lt__', __lt__)
        if (options['eq'] and options['frozen']) or options['unsafe_hash']:
            dict_.setdefault('__hash__', __hash__)

        return type.__new__(DataClassInit if options["init"] and user_init else mcs, name, bases, dict_)

    def __init__(cls, *args, **kwargs):
        # warn the user if they try to use __post_init__
        if hasattr(cls, '__post_init__'):
            raise TypeError('dataclassy does not use __post_init__. You should rename this method __init__')

        if cls.__dataclass__['eq'] and cls.__dataclass__['order']:
            from functools import total_ordering
            total_ordering(cls)

        # determine a static expression for an instance's fields as a tuple, then evaluate this to create a property
        # allowing efficient representation for internal methods
        tuple_expr = f'({", ".join((*(f"self.{f}" for f in fields(cls)), ""))})'  # "" ensures closing comma
        cls.__tuple__ = property(eval(f'lambda self: {tuple_expr}'))


class DataClassInit(DataClassMetaZ):
    """In the case that a custom __init__ is defined, remove arguments used by __new__ before calling it."""
    def __call__(cls, *args, **kwargs):
        args = iter(args)
        new_kwargs = dict(zip(cls.__annotations__, args))  # convert positional args to keyword for __new__
        instance = cls.__new__(cls, **new_kwargs, **kwargs)

        for parameter in kwargs.keys() & cls.__annotations__.keys():
            del kwargs[parameter]

        instance.__init__(*args, **kwargs)
        return instance

        # if cls.__dataclass__["init"]:
        #     args = iter(args)
        #     new_kwargs = dict(zip(cls.__annotations__, args))  # convert positional args to keyword for __new__
        #     instance = cls.__new__(cls, **new_kwargs, **kwargs)
        #     for parameter in kwargs.keys() & cls.__annotations__.keys():
        #         del kwargs[parameter]
        # else:
        #     instance = cls.__new__(cls)
        #
        # instance.__init__(*args, **kwargs)
        # return instance

    @property
    def __signature__(cls):
        """Defining a __call__ breaks inspect.signature. Lazily generate a Signature object ourselves."""
        import inspect
        parameters = tuple(inspect.signature(cls.__new__).parameters.values())
        return inspect.Signature(parameters[1:])  # remove 'cls' to transform parameters of __new__ into those of class

