from typing import Dict, Set, TYPE_CHECKING

from dataclassy import dataclass

from zepben.evolve import IdentifiedObject

__all__ = ["Reshape"]
class Reshape(object):
    originalToNew: Dict[str, Set[IdentifiedObject]]  # but not really
    newToOriginal: Dict[IdentifiedObject, Set[str]]  # but as above

    def __init__(self, originalToNew: Dict[str, Set[IdentifiedObject]], newToOriginal: Dict[IdentifiedObject, Set[str]]):
        self.originalToNew = originalToNew
        self.newToOriginal = newToOriginal

    def __add__(self, other):
        other: Reshape
        totalForwardMapping: Dict[str, Set[IdentifiedObject]] = {}
        intermediateMRIDs: Set[str] = set()

        for originalMRID, newIOs in self.originalToNew.items():
            reshapedIOs: Set[IdentifiedObject] = set()

            for io in newIOs:
                if io.mrid in other.originalToNew and other.originalToNew[io.mrid] is not None:
                    reshapedIOs.update(other.originalToNew[io.mrid])
                    intermediateMRIDs.add(io.mrid)
                else:
                    reshapedIOs.add(io)

            totalForwardMapping[originalMRID] = reshapedIOs

        for originalMRID, newIOs in other.originalToNew.items():
            if originalMRID not in intermediateMRIDs:
                totalForwardMapping[originalMRID] = newIOs

        totalBackwardMapping: Dict[IdentifiedObject, Set[str]] = {}
        newToOriginalByMRID: Dict[str, Set[str]] = {k.mrid: v for k, v in self.newToOriginal.items()}

        for newIO, originalMRIDs in other.newToOriginal.items():
            combinedExpansion: Set[str] = set()
            for mRID in originalMRIDs:
                if mRID in newToOriginalByMRID and newToOriginalByMRID[mRID] is not None:
                    combinedExpansion.update(newToOriginalByMRID[mRID])
                else:
                    combinedExpansion.add(mRID)
            totalBackwardMapping[newIO] = combinedExpansion

        for newIO, originalMRIDs in self.newToOriginal.items():
            if newIO.mrid not in intermediateMRIDs:
                totalBackwardMapping[newIO] = originalMRIDs

        return Reshape(totalForwardMapping, totalBackwardMapping)
