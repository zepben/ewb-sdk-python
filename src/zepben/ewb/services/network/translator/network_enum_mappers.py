#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = []

from zepben.protobuf.cim.extensions.iec61970.base.protection.PowerDirectionKind_pb2 import PowerDirectionKind as PBPowerDirectionKind
from zepben.protobuf.cim.extensions.iec61970.base.protection.ProtectionKind_pb2 import ProtectionKind as PBProtectionKind
from zepben.protobuf.cim.extensions.iec61970.base.wires.BatteryControlMode_pb2 import BatteryControlMode as PBBatteryControlMode
from zepben.protobuf.cim.extensions.iec61970.base.wires.TransformerCoolingType_pb2 import TransformerCoolingType as PBTransformerCoolingType
from zepben.protobuf.cim.extensions.iec61970.base.wires.VectorGroup_pb2 import VectorGroup as PBVectorGroup
from zepben.protobuf.cim.iec61968.assetinfo.WireMaterialKind_pb2 import WireMaterialKind as PBWireMaterialKind
from zepben.protobuf.cim.iec61968.infiec61968.infassetinfo.TransformerConstructionKind_pb2 import TransformerConstructionKind as PBTransformerConstructionKind
from zepben.protobuf.cim.iec61968.infiec61968.infassetinfo.TransformerFunctionKind_pb2 import TransformerFunctionKind as PBTransformerFunctionKind
from zepben.protobuf.cim.iec61968.infiec61968.infassets.StreetlightLampKind_pb2 import StreetlightLampKind as PBStreetlightLampKind
from zepben.protobuf.cim.iec61968.metering.EndDeviceFunctionKind_pb2 import EndDeviceFunctionKind as PBEndDeviceFunctionKind
from zepben.protobuf.cim.iec61970.base.auxiliaryequipment.PotentialTransformerKind_pb2 import PotentialTransformerKind as PBPotentialTransformerKind
from zepben.protobuf.cim.iec61970.base.core.PhaseCode_pb2 import PhaseCode as PBPhaseCode
from zepben.protobuf.cim.iec61970.base.domain.UnitSymbol_pb2 import UnitSymbol as PBUnitSymbol
from zepben.protobuf.cim.iec61970.base.generation.production.BatteryStateKind_pb2 import BatteryStateKind as PBBatteryStateKind
from zepben.protobuf.cim.iec61970.base.wires.PhaseShuntConnectionKind_pb2 import PhaseShuntConnectionKind as PBPhaseShuntConnectionKind
from zepben.protobuf.cim.iec61970.base.wires.RegulatingControlModeKind_pb2 import RegulatingControlModeKind as PBRegulatingControlModeKind
from zepben.protobuf.cim.iec61970.base.wires.SVCControlMode_pb2 import SVCControlMode as PBSVCControlMode
from zepben.protobuf.cim.iec61970.base.wires.SinglePhaseKind_pb2 import SinglePhaseKind as PBSinglePhaseKind
from zepben.protobuf.cim.iec61970.base.wires.SynchronousMachineKind_pb2 import SynchronousMachineKind as PBSynchronousMachineKind
from zepben.protobuf.cim.iec61970.base.wires.WindingConnection_pb2 import WindingConnection as PBWindingConnection
from zepben.protobuf.network.model.FeederDirection_pb2 import FeederDirection as PBFeederDirection

from zepben.ewb.model.cim.extensions.iec61970.base.protection.power_direction_kind import PowerDirectionKind
from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_kind import ProtectionKind
from zepben.ewb.model.cim.extensions.iec61970.base.wires.battery_control_mode import BatteryControlMode
from zepben.ewb.model.cim.extensions.iec61970.base.wires.transformer_cooling_type import TransformerCoolingType
from zepben.ewb.model.cim.extensions.iec61970.base.wires.vector_group import VectorGroup
from zepben.ewb.model.cim.iec61968.assetinfo.wire_material_kind import WireMaterialKind
from zepben.ewb.model.cim.iec61968.infiec61968.infassetinfo.transformer_construction_kind import TransformerConstructionKind
from zepben.ewb.model.cim.iec61968.infiec61968.infassetinfo.transformer_function_kind import TransformerFunctionKind
from zepben.ewb.model.cim.iec61968.infiec61968.infassets.streetlight_lamp_kind import StreetlightLampKind
from zepben.ewb.model.cim.iec61968.metering.end_device_function_kind import EndDeviceFunctionKind
from zepben.ewb.model.cim.iec61970.base.auxiliaryequipment.potential_transformer_kind import PotentialTransformerKind
from zepben.ewb.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.ewb.model.cim.iec61970.base.domain.unit_symbol import UnitSymbol
from zepben.ewb.model.cim.iec61970.base.generation.production.battery_state_kind import BatteryStateKind
from zepben.ewb.model.cim.iec61970.base.wires.phase_shunt_connection_kind import PhaseShuntConnectionKind
from zepben.ewb.model.cim.iec61970.base.wires.regulating_control_mode_kind import RegulatingControlModeKind
from zepben.ewb.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.ewb.model.cim.iec61970.base.wires.svc_control_mode import SVCControlMode
from zepben.ewb.model.cim.iec61970.base.wires.synchronous_machine_kind import SynchronousMachineKind
from zepben.ewb.model.cim.iec61970.base.wires.winding_connection import WindingConnection
# noinspection PyProtectedMember
from zepben.ewb.services.common.enum_mapper import EnumMapper
from zepben.ewb.services.network.tracing.feeder.feeder_direction import FeederDirection

#
# NOTE: These are deliberately excluded from the module export, as they aren't part of the public api.
#

_map_battery_control_mode = EnumMapper(BatteryControlMode, PBBatteryControlMode)
_map_battery_state_kind = EnumMapper(BatteryStateKind, PBBatteryStateKind)
_map_end_device_function_kind = EnumMapper(EndDeviceFunctionKind, PBEndDeviceFunctionKind)
_map_feeder_direction = EnumMapper(FeederDirection, PBFeederDirection)
_map_phase_code = EnumMapper(PhaseCode, PBPhaseCode)
_map_phase_shunt_connection_kind = EnumMapper(PhaseShuntConnectionKind, PBPhaseShuntConnectionKind)
_map_potential_transformer_kind = EnumMapper(PotentialTransformerKind, PBPotentialTransformerKind)
_map_power_direction_kind = EnumMapper(PowerDirectionKind, PBPowerDirectionKind)
_map_protection_kind = EnumMapper(ProtectionKind, PBProtectionKind)
_map_regulating_control_mode_kind = EnumMapper(RegulatingControlModeKind, PBRegulatingControlModeKind)
_map_single_phase_kind = EnumMapper(SinglePhaseKind, PBSinglePhaseKind)
_map_streetlight_lamp_kind = EnumMapper(StreetlightLampKind, PBStreetlightLampKind)
_map_svc_control_mode = EnumMapper(SVCControlMode, PBSVCControlMode)
_map_synchronous_machine_kind = EnumMapper(SynchronousMachineKind, PBSynchronousMachineKind)
_map_transformer_construction_kind = EnumMapper(TransformerConstructionKind, PBTransformerConstructionKind)
_map_transformer_cooling_type = EnumMapper(TransformerCoolingType, PBTransformerCoolingType)
_map_transformer_function_kind = EnumMapper(TransformerFunctionKind, PBTransformerFunctionKind)
_map_unit_symbol = EnumMapper(UnitSymbol, PBUnitSymbol)
_map_vector_group = EnumMapper(VectorGroup, PBVectorGroup)
_map_winding_connection = EnumMapper(WindingConnection, PBWindingConnection)
_map_wire_material_kind = EnumMapper(WireMaterialKind, PBWireMaterialKind)
