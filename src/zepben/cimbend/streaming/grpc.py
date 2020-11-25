#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Optional, TypeVar, Generic, Callable, List, Union

from dataclassy import dataclass

T = TypeVar("T")


@dataclass(slots=True)
class GrpcResult(Generic[T]):
    result: Optional[Union[T, Exception]]
    was_error_handled: bool = False

    @property
    def was_successful(self):
        return not self.was_failure

    @property
    def was_failure(self):
        return isinstance(self.result, Exception)

    def on_success(self, handler: Callable[[T], None]) -> GrpcResult[T]:
        """Calls `handler` with the `result` if this `was_successful`"""
        if self.was_successful:
            handler(self.result)
        return self

    def on_error(self, handler: Callable[[Exception, bool], GrpcResult[T]]) -> GrpcResult[T]:
        if self.was_failure and self.was_error_handled:
            return handler(self.result, self.was_error_handled)
        return self

    def on_handled_error(self, handler: Callable[[Exception], None]) -> GrpcResult[T]:
        if self.was_failure and self.was_error_handled:
            handler(self.result)
        return self

    def on_unhandled_error(self, handler: Callable[[Exception], None]) -> GrpcResult[T]:
        if self.was_failure and not self.was_error_handled:
            handler(self.result)
        return self

    def throw_on_error(self) -> GrpcResult[T]:
        if self.was_failure:
            raise self.result
        return self

    def throw_on_unhandled_error(self) -> GrpcResult[T]:
        if self.was_failure and not self.was_error_handled:
            raise self.result
        return self


@dataclass(slots=True)
class GrpcClient(object):
    error_handlers: List[Callable[[Exception], bool]] = []

    def try_handle_error(self, e: Exception) -> bool:
        for handler in self.error_handlers:
            if handler(e):
                return True
        return False

    async def try_rpc(self, rpc: Callable[[], IdentifiedObject]) -> GrpcResult:
        try:
            return GrpcResult(await rpc())
        except Exception as e:
            return GrpcResult(e, self.try_handle_error(e))
