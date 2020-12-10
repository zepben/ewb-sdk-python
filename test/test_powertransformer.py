#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import PowerTransformer, BaseVoltage, Terminal, PowerTransformerEnd


class TestPowerTransformer(object):

    def test_powertransformer_voltages(self):
        bv11k = BaseVoltage(nominal_voltage=11000)
        pt = PowerTransformer(base_voltage=bv11k)
        t1 = Terminal(conducting_equipment=pt)
        pte = PowerTransformerEnd(power_transformer=pt, base_voltage=bv11k, terminal=t1)
        pt.add_end(pte)
        assert pt.get_base_voltage(t1) is pte.base_voltage is t1.base_voltage
