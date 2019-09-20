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


from zepben.cim.IEC61970.diagram_layout_pb2 import DiagramObjectPoint as PBDiagramObjectPoint


class DiagramObjectPoints(object):
    def __init__(self, x, y):
        self.x_position = x
        self.y_position = y

    def __str__(self):
        return f"xPos: {self.x_position}, yPos: {self.y_position}"

    def __repr__(self):
        return f"xPos: {self.x_position}, yPos: {self.y_position}"

    def to_pb(self):
        return PBDiagramObjectPoint(xPosition=self.x_position, yPosition=self.y_position)
