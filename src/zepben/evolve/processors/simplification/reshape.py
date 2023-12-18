import time
from typing import Dict, Set


from zepben.evolve import IdentifiedObject

__all__ = ["Reshape"]


class PerfCount:
    def __init__(self):
        self.count = 0
        self.total = 0.0
        self.current = None

    def start(self):
        self.current = time.monotonic()

    def stop(self):
        end = time.monotonic()
        if self.current is not None:
            self.count += 1
            self.total += end - self.current
            self.current = None


class Reshape(object):
    originalToNew: Dict[str, Set[IdentifiedObject]]  # but not really
    newToOriginal: Dict[str, Set[str]]  # but as above

    def __init__(self, originalToNew: Dict[str, Set[IdentifiedObject]], newToOriginal: Dict[str, Set[str]]):
        self.originalToNew = originalToNew
        self.newToOriginal = newToOriginal

    def __add__(self, other):
        self.per_original_to_new = PerfCount()
        self.per_new_to_original = PerfCount()
        self.per_new_ios = PerfCount()
        self.per_original_ios = PerfCount()
        self.new_to_original_by_mrid = PerfCount()

        self.per_other_original_to_new = PerfCount()
        self.per_other_new_to_original = PerfCount()
        self.floating = PerfCount()
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

        totalBackwardMapping: Dict[str, Set[str]] = {}
        newToOriginalByMRID: Dict[str, Set[str]] = {k: v for k, v in self.newToOriginal.items()}

        for newIO, originalMRIDs in other.newToOriginal.items():
            combinedExpansion: Set[str] = set()
            for mRID in originalMRIDs:
                if mRID in newToOriginalByMRID and newToOriginalByMRID[mRID] is not None:
                    combinedExpansion.update(newToOriginalByMRID[mRID])
                else:
                    combinedExpansion.add(mRID)
            self.floating.start()
            totalBackwardMapping[newIO] = combinedExpansion
            self.floating.stop()

        for newIO, originalMRIDs in self.newToOriginal.items():
            if newIO not in intermediateMRIDs:
                totalBackwardMapping[newIO] = originalMRIDs

        for perf in [self.floating]:
            print(f'count: {perf.count}, total: {perf.total}')
        return Reshape(totalForwardMapping, totalBackwardMapping)
