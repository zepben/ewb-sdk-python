#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import TypeVar, Generic, Callable, List, Union, Coroutine

from dataclassy import dataclass

__all__ = ["GrpcResult", "GrpcClient"]

T = TypeVar("T")


@dataclass(slots=True)
class GrpcResult(Generic[T]):
    result: Union[T, Exception]
    was_error_handled: bool = False

    @property
    def value(self) -> T:
        if self.result is not None and isinstance(self.result, Exception):
            raise TypeError("You can only call value on a successful result.")
        return self.result

    @property
    def thrown(self) -> Exception:
        if self.result is None or not isinstance(self.result, Exception):
            raise TypeError("You can only call thrown on an unsuccessful result.")
        return self.result

    @property
    def was_successful(self):
        return not self.was_failure

    @property
    def was_failure(self):
        return isinstance(self.result, Exception)

    @property
    def was_error_unhandled(self):
        return not self.was_error_handled

    def on_success(self, handler: Callable[[T], None]) -> GrpcResult[T]:
        """Calls `handler` with the `result` if this `was_successful`"""
        if self.was_successful:
            handler(self.result)
        return self

    def on_error(self, handler: Callable[[Exception, bool], GrpcResult[T]]) -> GrpcResult[T]:
        """Calls `handler` with the `thrown` exception and `self.was_error_handled` if `self.was_failure`."""
        if self.was_failure and self.was_error_handled:
            return handler(self.result, self.was_error_handled)
        return self

    def on_handled_error(self, handler: Callable[[Exception], None]) -> GrpcResult[T]:
        """Calls `handler` with the `thrown` exception if `self.was_failure` only if `self.was_error_handled`."""
        if self.was_failure and self.was_error_handled:
            handler(self.result)
        return self

    def on_unhandled_error(self, handler: Callable[[Exception], None]) -> GrpcResult[T]:
        """Calls `handler` with the `thrown` exception if `self.was_failure` only if not `self.was_error_handled`."""
        if self.was_failure and not self.was_error_handled:
            handler(self.result)
        return self

    def throw_on_error(self) -> GrpcResult[T]:
        """Throws `self.result` if `self.was_failure`"""
        if self.was_failure:
            raise self.result
        return self

    def throw_on_unhandled_error(self) -> GrpcResult[T]:
        """Throws `self.result` only if `self.was_failure` and not `self.was_error_handled`"""
        if self.was_failure and not self.was_error_handled:
            raise self.result
        return self


@dataclass(init=False, slots=True)
class GrpcClient(object):
    error_handlers: List[Callable[[Exception], bool]] = []

    timeout: int = 0
    '''Timeout for client gRPC requests'''

    def __init__(self, error_handlers: List[Callable[[Exception], bool]] = None, timeout: int = 60):
        if error_handlers:
            self.error_handlers = error_handlers.copy()
        else:
            self.error_handlers = list()
        self.timeout = timeout

    def try_handle_error(self, e: Exception) -> bool:
        for handler in self.error_handlers:
            if handler(e):
                return True
        return False

    async def try_rpc(self, rpc: Callable[[], Coroutine[None, None, T]]) -> GrpcResult[T]:
        try:
            return GrpcResult(await rpc())
        except Exception as e:
            return GrpcResult(e, self.try_handle_error(e))
