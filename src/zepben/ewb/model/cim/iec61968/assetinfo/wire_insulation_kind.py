#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from enum import Enum

from zepben.ewb import unique


@unique
class WireInsulationKind(Enum):
    """
     * Kind of wire insulation.
     *
     :var UNKNOWN: Unknown insulation kind.
     :var asbestosAndVarnishedCambric: Asbestos and varnished cambric wire insulation.
     :var beltedPilc: Belted pilc wire insulation.
     :var butyl: Butyl wire insulation.
     :var crosslinkedPolyethylene: Crosslinked polyethylene wire insulation.
     :var ethylenePropyleneRubber: Ethylene propylene rubber wire insulation.
     :var highMolecularWeightPolyethylene: High nolecular weight polyethylene wire insulation.
     :var highPressureFluidFilled: High pressure fluid filled wire insulation.
     :var lowCapacitanceRubber: Low capacitance rubber wire insulation.
     :var oilPaper: Oil paper wire insulation.
     :var other: Other kind of wire insulation.
     :var ozoneResistantRubber: Ozone resistant rubber wire insulation.
     :var rubber: Rubber wire insulation.
     :var siliconRubber: Silicon rubber wire insulation.
     :var treeResistantHighMolecularWeightPolyethylene: Tree resistant high molecular weight polyethylene wire insulation.
     :var treeRetardantCrosslinkedPolyethylene: Tree retardant crosslinked polyethylene wire insulation.
     :var unbeltedPilc: Unbelted pilc wire insulation.
     :var varnishedCambricCloth: Varnished cambric cloth wire insulation.
     :var varnishedDacronGlass: Varnished dacron glass wire insulation.
     :var crosslinkedPolyethyleneWithHelicallyWoundCopperScreen: [ZBEX] Cross-Linked Polyethylene (xlpe) with helically wound copper screen
     :var crosslinkedPolyethyleneWithWavewoundAluminiumScreen: [ZBEX] Cross-Linked Polyethylene (xlpe), wavewound aluminium screen
     :var doubleInsulatedNeutralScreened: [ZBEX] Stranded copper conductor, p.v.c. insulated, copper neutral screen, p.v.c.-insulating sheath overall. (Double insulated neutral screened)
     :var doubleWireArmour: [ZBEX] Serving (or bedding) double wire armour
     :var doubleWireArmourWithPolyvinylChlorideSheath: [ZBEX] Double wire armoured PVC outer sheath
     :var ethylenePropyleneRubberStrandedCopperConductor: [ZBEX] Stranded copper, Ethylene Propylene Rubber conductor insulation
     :var ethylenePropyleneRubberWithHelicallyWoundCopperScreen: [ZBEX] Ethylene Propylene Rubber conductor insulation, helically wound copper screen
     :var NONE: [ZBEX] No insulation.
     :var paperWithLeadAlloySheath: [ZBEX] Paper insulated, lead alloy sheath
     :var paperWithLeadAlloySheathAndPvcOuterSheathScreenedHochstadterConstruction: [ZBEX] Paper insulated, lead alloy sheath, P.V.C outer sheath, Screened(Hochstadter) construction
     :var paperWithLeadAlloySheathSingleWireArmoured: [ZBEX] Paper insulated, lead alloy sheath, single wire armoured.
     :var paperWithLeadAlloySheathSingleWireArmouredBeltedConstruction: [ZBEX] Paper insulated, lead alloy sheath, single wire armoured, belted construction
     :var paperWithLeadAlloySheathSingleWireArmouredHessianServed: [ZBEX] Paper insulated, lead alloy sheath, single wire armoured, Hessian served.
     :var paperWithLeadAlloySheathSingleWireArmouredWithHighDensityPoluethyleneScreen: [ZBEX] Paper insulated, lead alloy sheath, single wire armoured, High density polyethylene(& pvc/hdpeh composite) screen
     :var paperWithLeadAlloySheathSingleWireArmouredWithWavewoundAluminiumScreen: [ZBEX] Paper insulated, lead alloy sheath, single wire armoured, wavewound aluminium screen
     :var polyvinylChloride: [ZBEX] p.v.c (Polyvinyl Chloride)
     :var polyvinylChlorideWithPolyvinylChlorideScreen: [ZBEX] p.v.c (Polyvinyl Chloride) with Polyvinyl Chloride screen
     :var polyvinylChlorideWithWavewoundCopperScreen: [ZBEX] p.v.c (Polyvinyl Chloride) with wavewound copper screen
     """

    UNKNOWN = 0
    asbestosAndVarnishedCambric = 1
    beltedPilc = 2
    butyl = 3
    crosslinkedPolyethylene = 4
    ethylenePropyleneRubber = 5
    highMolecularWeightPolyethylene = 6
    highPressureFluidFilled = 7
    lowCapacitanceRubber = 8
    oilPaper = 9
    other = 10
    ozoneResistantRubber = 11
    rubber = 12
    siliconRubber = 13
    treeResistantHighMolecularWeightPolyethylene = 14
    treeRetardantCrosslinkedPolyethylene = 15
    unbeltedPilc = 16
    varnishedCambricCloth = 17
    varnishedDacronGlass = 18
    crosslinkedPolyethyleneWithHelicallyWoundCopperScreen = 19
    crosslinkedPolyethyleneWithWavewoundAluminiumScreen = 20
    doubleInsulatedNeutralScreened = 21
    doubleWireArmour = 22
    doubleWireArmourWithPolyvinylChlorideSheath = 23
    ethylenePropyleneRubberStrandedCopperConductor = 24
    ethylenePropyleneRubberWithHelicallyWoundCopperScreen = 25
    NONE = 26
    paperWithLeadAlloySheath = 27
    paperWithLeadAlloySheathAndPvcOuterSheathScreenedHochstadterConstruction = 28
    paperWithLeadAlloySheathSingleWireArmoured = 29
    paperWithLeadAlloySheathSingleWireArmouredBeltedConstruction = 30
    paperWithLeadAlloySheathSingleWireArmouredHessianServed = 31
    paperWithLeadAlloySheathSingleWireArmouredWithHighDensityPoluethyleneScreen = 32
    paperWithLeadAlloySheathSingleWireArmouredWithWavewoundAluminiumScreen = 33
    polyvinylChloride = 34
    polyvinylChlorideWithPolyvinylChlorideScreen = 35
    polyvinylChlorideWithWavewoundCopperScreen = 36

    @property
    def short_name(self):
        return str(self)[19:]
