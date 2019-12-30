"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""


from zepben.cim.iec61970 import PhaseShuntConnectionKind, SinglePhaseKind, EnergyConsumer as PBEnergyConsumer, EnergyConsumerPhase as PBEnergyConsumerPhase
from zepben.model.terminal import Terminal
from zepben.model.equipment import ConductingEquipment, PowerSystemResource
from zepben.model.base_voltage import BaseVoltage, UNKNOWN as BV_UNKNOWN
from zepben.model.diagram_layout import DiagramObject
from zepben.model.common import Location
from typing import List


class EnergyConsumerPhase(PowerSystemResource):
    """
    A single phase of an energy consumer.

    Attributes:
        pfixed : Active power of the load that is a fixed quantity. Load sign convention is used,
                 i.e. positive sign means flow out from a node.
        qfixed : Reactive power of the load that is a fixed quantity. Load sign convention is used,
                 i.e. positive sign means flow out from a node.
        phase : A :class:`zepben.cim.iec61970.base.wires.SinglePhaseKind`
                Phase of this energy consumer component. If the energy consumer is wye connected, the connection is from
                the indicated phase to the central ground or neutral point. If the energy consumer is delta connected,
                the phase indicates an energy consumer connected from the indicated phase to the next logical
                non-neutral phase.
    """
    def __init__(self, pfixed: float, qfixed: float, phase: SinglePhaseKind, mrid: str = "", name: str = "",
                 diag_objs: List[DiagramObject] = None):
        """
        Create an EnergyConsumerPhase. Represents a single phase of an EnergyConsumer. Typically, you are only required
        to create EnergyConsumerPhases if they are unbalanced, or if it's a single phase EnergyConsumer.

        :param pfixed: Active power of the load that is a fixed quantity. Load sign convention is used,
                       i.e. positive sign means flow out from a node.
        :param qfixed: Reactive power of the load that is a fixed quantity. Load sign convention is used,
                       i.e. positive sign means flow out from a node.
        :param phase: A :class:`zepben.cim.iec61970.base.wires.SinglePhaseKind`
        :param mrid: mRID for this object (optional)
        :param name: Any free human readable and possibly non unique text naming the object.
        :param diag_objs: An ordered list of :class:`zepben.model.DiagramObject`'s.
        """
        self.pfixed = pfixed
        self.qfixed = qfixed
        self.phase = phase
        super().__init__(mrid=mrid, name=name, diag_objs=diag_objs)

    def to_pb(self):
        return PBEnergyConsumerPhase(**self._pb_args())

    @staticmethod
    def from_pb(pb_ecp, **kwargs):
        return EnergyConsumerPhase(pfixed=pb_ecp.pfixed, qfixed=pb_ecp.qfixed, phase=pb_ecp.phase)


class EnergyConsumer(ConductingEquipment):
    """
    Generic user of energy - a point of consumption on the power system model. May also represent a pro-sumer with
    negative p/q values.

    Attributes:
        p : Active power of the load. Load sign convention is used, i.e. positive sign means flow out from a node.
            For voltage dependent loads the value is at rated voltage.
            Starting value for a steady state solution.
        q : Reactive power of the load. Load sign convention is used, i.e. positive sign means flow out from a node.
            For voltage dependent loads the value is at rated voltage.
            Starting value for a steady state solution.
        phaseConnection : :class:`zepben.cim.iec61970.base.wires.PhaseShuntConnectionKind` - The type of phase
                          connection, such as wye, delta, I (single phase).
    """
    def __init__(self, mrid: str, p: float = None, q: float = None, in_service: bool = True, base_voltage: BaseVoltage = BV_UNKNOWN,
                 phs_shunt_conn_kind: PhaseShuntConnectionKind = None, ecp: List[EnergyConsumerPhase] = None, name: str = "",
                 terminals: List = None, diag_objs: List[DiagramObject] = None, location: Location = None):
        """
        Create an EnergyConsumer
        :param mrid: mRID for this object
        :param p: Active power of the load. Load sign convention is used, i.e. positive sign means flow out from a node.
                  For voltage dependent loads the value is at rated voltage.
                  Starting value for a steady state solution.
        :param q: Reactive power of the load. Load sign convention is used, i.e. positive sign means flow out from a node.
                  For voltage dependent loads the value is at rated voltage.
                  Starting value for a steady state solution.
        :param in_service: If True, the equipment is in service.
        :param base_voltage: A :class:`zepben.model.BaseVoltage`.
        :param phs_shunt_conn_kind: :class:`zepben.cim.iec61970.base.wires.PhaseShuntConnectionKind` - The type of phase
                                    connection, such as wye, delta, I (single phase).
        :param ecp: The :class:`EnergyConsumerPhase` if this is a single phase EnergyConsumer or if the phases are
                    unbalanced.
        :param name: Any free human readable and possibly non unique text naming the object.
        :param terminals: An ordered list of :class:`zepben.model.Terminal`'s. The order is important and the index of
                          each Terminal should reflect each Terminal's `sequenceNumber`.
        :param diag_objs: An ordered list of :class:`zepben.model.DiagramObject`'s.
        :param location: :class:`zepben.model.Location` of this resource.
        """
        self.p = p
        self.q = q
        self.phaseConnection = phs_shunt_conn_kind
        self.energy_consumer_phases = ecp if ecp is not None else []
        super().__init__(mrid=mrid, in_service=in_service, base_voltage=base_voltage, name=name, terminals=terminals, diag_objs=diag_objs, location=location)

    def __str__(self):
        return f"{super().__str__()} p: {self.p}, q: {self.q}"

    def __repr__(self):
        return f"{super().__repr__()} p: {self.p}, q: {self.q}"

    def to_pb(self):
        args = self._pb_args()
        return PBEnergyConsumer(**args)

    @staticmethod
    def from_pb(pb_ec, network, **kwargs):
        """
        Convert a protobuf EnergyConsumer to a :class:`zepben.model.EnergyConsumer`
        :param pb_ec: :class:`zepben.cim.iec61970.base.wires.EnergyConsumer`
        :param network: EquipmentContainer to extract pb_ec.baseVoltageMRID
        :raises: NoBaseVoltageException when pb_ec.baseVoltageMRID isn't found in network
        :return: A :class:`zepben.model.EnergyConsumer`
        """
        terms = Terminal.from_pbs(pb_ec.terminals, network)
        location = Location.from_pb(pb_ec.location)
        diag_objs = DiagramObject.from_pbs(pb_ec.diagramObjects)
        base_voltage = network.get_base_voltage(pb_ec.baseVoltageMRID) if pb_ec.baseVoltageMRID else None
        ecp = EnergyConsumerPhase.from_pbs(pb_ec.energyConsumerPhases)

        return EnergyConsumer(mrid=pb_ec.mRID,
                              p=pb_ec.p,
                              q=pb_ec.q,
                              name=pb_ec.name,
                              base_voltage=base_voltage,
                              phs_shunt_conn_kind=pb_ec.phaseConnection,
                              in_service=pb_ec.inService,
                              terminals=terms,
                              ecp=ecp,
                              diag_objs=diag_objs,
                              location=location)
