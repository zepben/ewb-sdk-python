from typing import Dict

from dataclassy import dataclass


class Reshape(object):
    originalToNew: Dict  # but not really
    newToOriginal: Dict  # but as above

    def __init__(self, originalToNew: Dict, newToOriginal: Dict):
        self.originalToNew = originalToNew
        self.newToOriginal = newToOriginal
