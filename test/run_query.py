#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import asyncio
import json
import platform
import shlex
from typing import List, Callable, Any, Optional

from geojson import FeatureCollection, Feature, LineString, Point
from zepben.eas import EasClient, Study, Result, GeoJsonOverlay

from zepben.evolve import connect_insecure, NetworkService, Equipment, Tracing, downstream, upstream, stop_at_open, NetworkTrace, IdentifiedObject
from zepben.evolve.streaming.get.network_consumer import NetworkConsumerClient

rpc_port = 9100
eas_port = 7654


async def run_queries():
    async with connect_insecure(rpc_port=rpc_port) as channel:
        ewb_client = NetworkConsumerClient(channel=channel)
        print("created EWB client.")
        eas_client = EasClient(
            host="localhost",
            port=eas_port,
            # username=args.username,
            # password=args.password,
            # client_id=args.client_id,
            verify_certificate=False,
            # client_secret=args.client_secret
        )
        print("created EAS client.")
        try:
            query = "with FNS022 select where is powertransformer"
            await upload_study(eas_client, "select is PowerTransformer", query, await run_query(ewb_client, query))
            query = "with FNS022 select where name like [BC]"
            await upload_study(eas_client, "select like [BC]", query, await run_query(ewb_client, query))
            query = "with FNS022 select where length < 10"
            await upload_study(eas_client, "select length < 10", query, await run_query(ewb_client, query))

            query = "with FNS022 trace downstream from 19404384"
            await upload_study(eas_client, "trace downstream", query, await run_query(ewb_client, query))
            query = "with FNS022 trace upstream from 19404384"
            await upload_study(eas_client, "trace upstream", query, await run_query(ewb_client, query))
            query = "with FNS022 trace from 19404384 stopping at is switch"
            await upload_study(eas_client, "trace between switches", query, await run_query(ewb_client, query))
        finally:
            await eas_client.aclose()

async def run_query(client: NetworkConsumerClient, query: str) -> Optional[List[IdentifiedObject]]:
    print()
    print(f"running query: {query}...")
    try:
        tokens = shlex.split(query)
        command = tokens.pop(0).lower()

        if command == "with":
            return await EquipmentContainerCommand(tokens.pop(0), tokens).run(client)
        else:
            raise ValueError(f"unknown command '{command}'")

    except Exception as ex:
        show_help(ex)
        return None


async def upload_study(client: EasClient, name: str, query: str, objects: Optional[List[Equipment]]):
    if not objects:
        print(f"No results for {name}, skipping study creation: {query}")
        return

    print("Uploading Study")
    with open(f"study_style.json", "r") as file:
        json_style = json.load(file)
    await client.async_upload_study(
        Study(
            name=name,
            description=query,
            tags=["FNS022"],
            results=[
                *[
                    Result(
                        name=f"test",
                        geo_json_overlay=GeoJsonOverlay(
                            data=as_features(objects),
                            styles=["query-style-line", "query-style-point"]
                        )
                    )
                ]
            ],
            styles=json_style
        )
    )
    print('Upload Complete')


def as_features(objects: List[IdentifiedObject]) -> FeatureCollection:
    features = []
    for it in objects:
        if isinstance(it, Equipment):
            points = list(it.location.points)
            geometry = None
            if len(points) == 1:
                geometry = Point((points[0].x_position, points[0].y_position))
            elif len(points) > 1:
                geometry = LineString([(pp.x_position, pp.y_position) for pp in points])

            if geometry:
                features.append(Feature(id=it.mrid, geometry=geometry))

    return FeatureCollection(features)


def show_help(ex: Exception):
    print(f"Failed to execute query: {str(ex)}")
    print(f"you gots ya query wrong, it shoulda bin like....")


class EquipmentContainerCommand:

    def __init__(self, name_or_mrid: str, additional_args: List[str]):
        self.name_or_mrid = name_or_mrid
        self.additional_args = additional_args

    async def run(self, client: NetworkConsumerClient) -> Optional[List[IdentifiedObject]]:
        result = await client.get_equipment_container(self.name_or_mrid)
        result.throw_on_error()

        sub_command = self.additional_args.pop(0).lower()
        if sub_command == "select":
            return await SelectCommand(self.additional_args).run(client.service)
        elif sub_command == "trace":
            return await TraceCommand(self.additional_args).run(client.service)
        else:
            raise ValueError(f"unknown sub-command '{sub_command}'")


class BaseCommand:

    @staticmethod
    def _check_attr(io: Equipment, attr: str, compare: Callable[[Any], bool]) -> bool:
        try:
            return compare(getattr(io, attr))
        except:
            return False

    @staticmethod
    def has_class(obj: Any, class_name: str):
        return any(cls.__name__.lower() == class_name.lower() for cls in obj.__class__.__mro__)


class SelectCommand(BaseCommand):

    def __init__(self, additional_args: List[str]):
        super().__init__()
        self.additional_args = additional_args

    async def run(self, service: NetworkService) -> Optional[List[IdentifiedObject]]:
        where_check = self.additional_args.pop(0).lower()
        assert where_check == "where", "missing keyword 'WHERE' after 'SELECT'"

        condition_check = self.additional_args.pop(0)

        if condition_check.lower() == "is":
            class_check = self.additional_args.pop(0)
            selected = [it for it in service.objects() if self.has_class(it, class_check)]
        else:
            # assume it is an attribute name
            comparison = self.additional_args.pop(0).lower()
            value = self.additional_args.pop(0)
            if comparison == "<":
                selected = [it for it in service.objects() if self._check_attr(it, condition_check, lambda attr: float(attr) < float(value))]
                pass
            elif comparison == "<=":
                selected = [it for it in service.objects() if self._check_attr(it, condition_check, lambda attr: float(attr) <= float(value))]
                pass
            elif comparison == "=" or comparison == "==":
                selected = [it for it in service.objects() if self._check_attr(it, condition_check, lambda attr: attr == value)]
                pass
            elif comparison == ">=":
                selected = [it for it in service.objects() if self._check_attr(it, condition_check, lambda attr: float(attr) >= float(value))]
                pass
            elif comparison == ">":
                selected = [it for it in service.objects() if self._check_attr(it, condition_check, lambda attr: float(attr) > float(value))]
                pass
            elif comparison.lower() == "like":
                selected = [it for it in service.objects() if self._check_attr(it, condition_check, lambda attr: value in attr)]
                pass
            else:
                raise ValueError(f"unknown select condition operator '{comparison}'")

        print([it.mrid for it in selected])

        if self.additional_args:
            remaining_condition = " ".join(self.additional_args)
            raise ValueError(f"unexpected remaining tokens: '{remaining_condition}'")

        return selected


class TraceCommand(BaseCommand):

    def __init__(self, additional_args: List[str]):
        super().__init__()
        self.additional_args = additional_args

    async def run(self, service: NetworkService) -> Optional[List[Equipment]]:
        trace_type = self.additional_args.pop(0).lower()

        traced = []
        trace: NetworkTrace[None] = \
            Tracing.network_trace() \
                .add_condition(stop_at_open()) \
                .add_step_action(lambda step, context: traced.append(step.path.to_equipment))

        if trace_type == "downstream":
            from_check = self.additional_args.pop(0).lower()
            assert from_check == "from", "missing keyword 'FROM' after 'DOWNSTREAM'"
            trace.add_condition(downstream())
        elif trace_type == "upstream":
            from_check = self.additional_args.pop(0).lower()
            assert from_check == "from", "missing keyword 'FROM' after 'UPSTREAM'"
            trace.add_condition(upstream())
        elif trace_type != "from":
            raise ValueError(f"unknown trace '{trace_type}'")

        start_point = self.additional_args.pop(0)

        if self.additional_args:
            stopping_check = self.additional_args.pop(0).lower()
            remaining_condition = " ".join(self.additional_args)
            assert stopping_check == "stopping", f"unexpected remaining tokens: '{stopping_check} {remaining_condition}'"

            at_check = self.additional_args.pop(0).lower()
            assert at_check == "at", "missing keyword 'AT' after 'STOPPING'"

            condition_check = self.additional_args.pop(0)

            if condition_check.lower() == "is":
                class_check = self.additional_args.pop(0)
                trace.add_stop_condition(lambda step, context: self.has_class(step.path.to_equipment, class_check))
            else:
                # assume it is an attribute name
                comparison = self.additional_args.pop(0).lower()
                value = self.additional_args.pop(0)
                if comparison == "<":
                    trace.add_stop_condition(
                        lambda step, context: self._check_attr(step.path.to_equipment, condition_check, lambda attr: float(attr) < float(value)))
                    pass
                elif comparison == "<=":
                    trace.add_stop_condition(
                        lambda step, context: self._check_attr(step.path.to_equipment, condition_check, lambda attr: float(attr) <= float(value)))
                    pass
                elif comparison == "=" or comparison == "==":
                    trace.add_stop_condition(lambda step, context: self._check_attr(step.path.to_equipment, condition_check, lambda attr: attr == value))
                    pass
                elif comparison == ">=":
                    trace.add_stop_condition(
                        lambda step, context: self._check_attr(step.path.to_equipment, condition_check, lambda attr: float(attr) >= float(value)))
                    pass
                elif comparison == ">":
                    trace.add_stop_condition(
                        lambda step, context: self._check_attr(step.path.to_equipment, condition_check, lambda attr: float(attr) > float(value)))
                    pass
                elif comparison.lower() == "like":
                    trace.add_stop_condition(lambda step, context: self._check_attr(step.path.to_equipment, condition_check, lambda attr: value in attr))
                    pass
                else:
                    raise ValueError(f"unknown select condition operator '{comparison}'")

        await trace.run(service[start_point])
        print([it.mrid for it in traced])

        if self.additional_args:
            remaining_condition = " ".join(self.additional_args)
            raise ValueError(f"unexpected remaining tokens: '{remaining_condition}'")

        return traced


if __name__ == "__main__":
    print(platform.architecture())

    asyncio.run(run_queries())
