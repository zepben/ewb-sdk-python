from __future__ import annotations
from zepben.cim.iec61970 import EnergySourcePhase as PBEnergySourcePhase
from zepben.model.phases import SinglePhaseKind
from zepben.model.power_system_resource import PowerSystemResource
from zepben.model.diagram_layout import DiagramObject
from typing import List


class EnergySourcePhase(PowerSystemResource):
    """
    A single phase of an energy source.

    Attributes:
        phase : A :class:`zepben.model.phases.SinglePhaseKind`
                Phase of this energy source component. If the energy source is wye connected, the connection is from
                the indicated phase to the central ground or neutral point. If the energy source is delta connected,
                the phase indicates an energy source connected from the indicated phase to the next logical
                non-neutral phase.
    """
    def __init__(self, phase: SinglePhaseKind, mrid: str = "", name: str = "", diag_objs: List[DiagramObject] = None):
        """
        Create an EnergySourcePhase. Represents a single phase of an EnergySource. Typically, you are only required
        to create EnergySourcePhases if they are unbalanced, or if it's a single phase EnergySource.

        :param phase: A :class:`zepben.model.phases.SinglePhaseKind`
        :param mrid: mRID for this object (optional)
        :param name: Any free human readable and possibly non unique text naming the object.
        :param diag_objs: An ordered list of :class:`zepben.model.DiagramObject`'s.
        """
        self.phase = phase
        super().__init__(mrid=mrid, name=name, diag_objs=diag_objs)

    def to_pb(self):
        return PBEnergySourcePhase(**self._pb_args())

    @staticmethod
    def from_pb(pb_esp, **kwargs):
        return EnergySourcePhase(phase=SinglePhaseKind.from_pb(pb_esp.phase), mrid=pb_esp.mRID, name=pb_esp.name,
                                 diag_objs=DiagramObject.from_pbs(pb_esp.diagramObjects))


class EnergySourcePhase(PowerSystemResource):
    """
    A single phase of an energy source.

    Attributes:
        phase : A :class:`zepben.model.phases.SinglePhaseKind`
                Phase of this energy source component. If the energy source is wye connected, the connection is from
                the indicated phase to the central ground or neutral point. If the energy source is delta connected,
                the phase indicates an energy source connected from the indicated phase to the next logical
                non-neutral phase.
    """
    def __init__(self, phase: SinglePhaseKind, mrid: str = "", name: str = "", diag_objs: List[DiagramObject] = None):
        """
        Create an EnergySourcePhase. Represents a single phase of an EnergySource. Typically, you are only required
        to create EnergySourcePhases if they are unbalanced, or if it's a single phase EnergySource.

        :param phase: A :class:`zepben.model.phases.SinglePhaseKind`
        :param mrid: mRID for this object (optional)
        :param name: Any free human readable and possibly non unique text naming the object.
        :param diag_objs: An ordered list of :class:`zepben.model.DiagramObject`'s.
        """
        self.phase = phase
        super().__init__(mrid=mrid, name=name, diag_objs=diag_objs)

    def to_pb(self):
        return PBEnergySourcePhase(**self._pb_args())

    @staticmethod
    def from_pb(pb_esp, **kwargs):
        return EnergySourcePhase(phase=SinglePhaseKind.from_pb(pb_esp.phase), mrid=pb_esp.mRID, name=pb_esp.name,
                                 diag_objs=DiagramObject.from_pbs(pb_esp.diagramObjects))

