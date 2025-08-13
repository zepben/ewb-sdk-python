#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.ewb.dataclassy.dctest import Example

if __name__ == '__main__':
    ex = Example(strings=['a', 'b'])
    ex.strings.add('ccc')
    ex.strings.add('hehe')
    print(ex.strings)