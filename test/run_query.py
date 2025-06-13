#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import asyncio
import platform
import shlex
from typing import List, Callable, Any

from zepben.evolve import connect_insecure, NetworkService, IdentifiedObject
from zepben.evolve.streaming.get.network_consumer import NetworkConsumerClient

rpc_port = 9100


async def run_queries():
    async with connect_insecure(rpc_port=rpc_port) as channel:
        print("created channel.")
        client = NetworkConsumerClient(channel=channel)
        print("created client.")

        await run_query(client, "with FNS022 select where is powertransformer")
        await run_query(client, "with FNS022 select where name like A")
        await run_query(client, "with FNS022 select where length < 10")


async def run_query(client: NetworkConsumerClient, query: str):
    print()
    print(f"running query: {query}...")
    try:
        tokens = shlex.split(query)
        command = tokens.pop(0).lower()

        if command == "with":
            await EquipmentContainerCommand(tokens.pop(0), tokens).run(client)
        else:
            raise ValueError(f"unknown command '{command}'")

    except Exception as ex:
        show_help(ex)


def show_help(ex: Exception):
    print(f"Failed to execute query: {str(ex)}")
    print(f"you gots ya query wrong, it shoulda bin like....")


class EquipmentContainerCommand:

    def __init__(self, name_or_mrid: str, additional_args: List[str]):
        self.name_or_mrid = name_or_mrid
        self.additional_args = additional_args

    async def run(self, client: NetworkConsumerClient):
        result = await client.get_equipment_container(self.name_or_mrid)
        result.throw_on_error()

        sub_command = self.additional_args.pop(0).lower()
        if sub_command == "select":
            where_check = self.additional_args.pop(0).lower()
            assert where_check == "where", "missing keyword 'WHERE' after 'SELECT'"
            await SelectCommand(self.additional_args).run(client.service)
        else:
            raise ValueError(f"unknown sub-command '{sub_command}'")


class SelectCommand:

    def __init__(self, additional_args: List[str]):
        self.additional_args = additional_args

    async def run(self, service: NetworkService):
        condition_check = self.additional_args.pop(0)

        if condition_check.lower() == "is":
            class_check = self.additional_args.pop(0).lower()
            print([it.mrid for it in service.objects() if it.__class__.__name__.lower() == class_check])
        else:
            # assume it is an attribute name
            comparison = self.additional_args.pop(0).lower()
            value = self.additional_args.pop(0)
            if comparison == "<":
                print([it.mrid for it in service.objects() if self._check_attr(it, condition_check, lambda attr: float(attr) < float(value))])
                pass
            elif comparison == "<=":
                print([it.mrid for it in service.objects() if self._check_attr(it, condition_check, lambda attr: float(attr) <= float(value))])
                pass
            elif comparison == "=" or comparison == "==":
                print([it.mrid for it in service.objects() if self._check_attr(it, condition_check, lambda attr: attr == value)])
                pass
            elif comparison == ">=":
                print([it.mrid for it in service.objects() if self._check_attr(it, condition_check, lambda attr: float(attr) >= float(value))])
                pass
            elif comparison == ">":
                print([it.mrid for it in service.objects() if self._check_attr(it, condition_check, lambda attr: float(attr) > float(value))])
                pass
            elif comparison.lower() == "like":
                print([it.mrid for it in service.objects() if self._check_attr(it, condition_check, lambda attr: value in attr)])
                pass
            else:
                raise ValueError(f"unknown select condition operator '{comparison}'")

        if self.additional_args:
            remaining_condition = " ".join(self.additional_args)
            raise ValueError(f"unexpected remaining tokens: '{remaining_condition}'")

    @staticmethod
    def _check_attr(io: IdentifiedObject, attr: str, compare: Callable[[Any], bool]) -> bool:
        try:
            return compare(getattr(io, attr))
        except:
            return False


if __name__ == "__main__":
    print(platform.architecture())

    asyncio.run(run_queries())
